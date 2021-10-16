import os, re
import pprint
from pathlib import Path
from enum import Enum, auto

from Python.ini_parser import ini_rules
from Python.ini_parser import ini_writer


class State(Enum):
	NOT_IN_A_COMMENT      = auto()
	READ_FIRST_SLASH      = auto()
	INSIDE_SINGLE_COMMENT = auto()
	INSIDE_MULTI_COMMENT  = auto()
	POSSIBLE_MULTI_ENDING = auto()


def parse_and_convert(input_folder_path, output_folder_path):
	mod_names = get_mod_names(input_folder_path)
	parsed = parse(output_folder_path, mod_names)
	# pprint.pprint(parsed)

	ini_rules.apply_rules(parsed)
	# pprint.pprint(parsed)

	ini_writer.write_converted_ini_recursively(parsed, Path(output_folder_path))


def get_mod_names(input_folder_path):
	return [p.name for p in Path(input_folder_path).iterdir() if p.suffix == ".rte" and p.is_dir()]


def parse(subfolder_path, mod_names):
	parsed_portion = {}
	for name in os.listdir(subfolder_path):
		p = subfolder_path / Path(name)

		if ".rte" not in str(p):
			continue
		elif not part_of_mod(p, mod_names): # TODO: Remove this once CCCP has a Mods folder that can be iterated over.
			continue

		if p.is_file() and p.suffix == ".ini" and p.stem != "desktop": # Skip the desktop.ini Windows metadata file.
			parsed_portion[name] = parse_file(str(p))

		if p.is_dir():
			parsed_portion[name] = parse(p, mod_names)
	return parsed_portion


def part_of_mod(p, mod_names):
	return any(mod_name in str(p) for mod_name in mod_names)


def parse_file(file_path):
	# print(file_path)
	with open(file_path) as f:
		parsed_file = []
		parse_file_recursively(parsed_file, f)
		return parsed_file


# This global variable is necessary due to how a deep function call needs to be able to also change this variable for the less deep function calls.
# Passing it as a function argument makes a copy of the boolean instead of being a reference to the original variable.
multiline = False

def parse_file_recursively(parsed_portion, f, depth_tab_count=0):
	"""
	# CC and CCCP use a custom INI format, so the configparser library can't be used to parse the INI files.
	# TODO: Check if the first line can be tabbed, because then prev_line_index needs to be initialized to 0.
	"""

	global multiline

	for line_number, line in enumerate(f, start=1):
		# print(repr(line))
		line = line.strip("\n")

		line_data, tab_count = get_line_data(line, depth_tab_count)
		# print(line_data)

		if tab_count == depth_tab_count:
			parsed_portion.append(line_data)
		elif tab_count == depth_tab_count + 1:
			if parsed_portion == []:
				file_path = f.name
				raise TabError(f"\nWrong tabbing on line {line_number} in file {file_path} on line '{line}'")

			previous_appended_line_data = parsed_portion[-1]

			previous_appended_line_data.append( { "type": "children", "value": [ line_data ] } )

			child_line_data = previous_appended_line_data[-1]["value"]
			child_return_values = parse_file_recursively(child_line_data, f, depth_tab_count+1)

			if child_return_values != None and child_return_values["tab_count"] == depth_tab_count:
				parsed_portion.append(child_return_values["line_data"])
			else:
				return child_return_values
		elif tab_count < depth_tab_count:
			child_return_values = { "line_data": line_data, "tab_count": tab_count }
			return child_return_values


# This string is global so append_token() can clear its value for get_line_data()
value_str = ""

def get_line_data(line, depth_tab_count):
	"""
	line_data consists of a list of dictionary tokens:
	[
		{ "type": "extra", "value": "\t" },
		{ "type": "property", "value": "Mass" },
		{ "type": "value", "value": "2400" },
		{ "type": "extra", "value": " /* */ foo /*" },
	]


	CCCP INI parser quirks to keep in mind:
	1.
		This works:
			Mass = 2400 /*
		foo
			*/ MaxInventoryMass = 3200

		while this crashes the game:
			Mass = 2400 // /*
		foo
			*/ MaxInventoryMass = 3200
	2.
		This works:
			/*
		foo
			// */ Mass = 2400
		
		while this crashes the game:
			/*
		foo
			// */ bar
	So a multi-line comment can't start during a single-line comment, and vice versa.
	"""

	global multiline, value_str

	line_data = []

	seen_equals = False
	was_prev_char_special = True # "special" meaning whitespace, / or *

	comment_state = State.INSIDE_MULTI_COMMENT if multiline else State.NOT_IN_A_COMMENT

	# parsing_state = "property" # TODO: Can this be used instead?
	parsing_state = "extra" if multiline else "property"

	tab_count = depth_tab_count if multiline else 0
	counting_tabs = not multiline

	# print(repr(line))
	for char in line:
		if comment_state in (State.INSIDE_SINGLE_COMMENT, State.INSIDE_MULTI_COMMENT, State.POSSIBLE_MULTI_ENDING):
			value_str += char
		elif char != "=":
			value_str += char

		# TODO: See what happens when this check and continue are removed.
		if comment_state == State.INSIDE_SINGLE_COMMENT:
			continue

		if counting_tabs and char.isspace():
			if char == "\t":
				tab_count += 1
		else:
			counting_tabs = False

		if char == "=" and not seen_equals and comment_state not in (State.INSIDE_SINGLE_COMMENT, State.INSIDE_MULTI_COMMENT):
			seen_equals = True

			append_token("property", value_str, line_data, 1)
			append_token("extra", "=", line_data, 2)
			parsing_state = "value"

		if comment_state == State.POSSIBLE_MULTI_ENDING and char == "/":
			comment_state = State.NOT_IN_A_COMMENT
			append_token("extra", value_str, line_data, 3)
		elif comment_state == State.INSIDE_MULTI_COMMENT and char == "*":
			comment_state = State.POSSIBLE_MULTI_ENDING
		elif comment_state == State.READ_FIRST_SLASH:
			if char == "/":
				comment_state = State.INSIDE_SINGLE_COMMENT
				append_token(parsing_state, value_str[:-2], line_data, 4)
				value_str = "//"
			elif char == "*":
				comment_state = State.INSIDE_MULTI_COMMENT
				append_token(parsing_state, value_str[:-2], line_data, 5)
				value_str = "/*"
			else:
				comment_state = State.NOT_IN_A_COMMENT
				value_str[:-1] + "/" + char
		elif comment_state == State.NOT_IN_A_COMMENT and char == "/":
			comment_state = State.READ_FIRST_SLASH

		was_prev_char_special = char.isspace() or char in ("/", "*")

	if comment_state in (State.INSIDE_SINGLE_COMMENT, State.INSIDE_MULTI_COMMENT):
		append_token("extra", value_str, line_data, 6)
	else:
		append_token(parsing_state, value_str, line_data, 7)

	multiline = comment_state == State.INSIDE_MULTI_COMMENT

	if parsing_state != "value": # If no = sign was encountered then the entire line was a comment.
		tab_count = depth_tab_count

	return line_data, tab_count


def append_token(typ, passed_str, line_data, debug_id):
	global value_str
	value_str = ""

	# print(debug_id, typ)

	# Transforms "\t Mass  " into ['\t ', 'Mass', '  '] and appends all of the tokens.
	# TODO: Combine consecutive tokens of the same type, like [{'type': 'extra', 'value': ' '}, {'type': 'extra', 'value': '//'}]
	for string in re.findall(r"\S+|\s+", passed_str):
		token = { "type": "extra" if string.isspace() else typ, "value": string.split("\t")[-1] }
		line_data.append(token)