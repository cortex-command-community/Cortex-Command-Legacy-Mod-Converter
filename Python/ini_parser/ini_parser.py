import os, re
import pprint
from pathlib import Path
from enum import Enum, auto

from Python.ini_parser import ini_rules


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

	convert(parsed)
	# pprint.pprint(parsed)

	write_converted_ini_recursively(parsed, Path(output_folder_path))


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


# This global variable is only used by the function below.
# It is necessary due to how a deep function call needs to be able to also change this variable for the less deep function calls.
# Passing it as a function argument makes a copy of the boolean instead of being a reference to the original variable, so that's why a global variable is needed.
multiline = False

def parse_file_recursively(parsed_portion, f, depth_tab_count=0):
	"""
	# CC and CCCP use a custom INI format, so the configparser library can't be used to parse the INI files.
	# TODO: Check if the first line can be tabbed, because then prev_line_index needs to be initialized to 0.
	"""

	global multiline

	for line in f:
		# print(repr(line))
		line = line.strip("\n")

		tab_count = get_tab_count(depth_tab_count, multiline, line)

		line_data, multiline = get_line_data(line, multiline)
		# print(line_data)
		# return # TODO: Remove this!

		if tab_count == depth_tab_count:
			parsed_portion.append(line_data)
		elif tab_count == depth_tab_count + 1:
			a = parsed_portion[-1]
			a.append( { "type": "children", "value": [] } )
			b = a[-1]["value"]
			b.append(line_data)

			child_values = parse_file_recursively(b, f, depth_tab_count+1)
			if child_values != None and child_values["tab_count"] == depth_tab_count:
				parsed_portion.append(child_values["line_data"])
			else:
				return child_values
		elif tab_count < depth_tab_count:
			return { "line_data": line_data, "tab_count": tab_count }


def get_tab_count(depth_tab_count, multiline, line):
	# depth_tab_count prevents multi-line comments from starting a new section.
	return depth_tab_count if multiline else len(line) - len(line.lstrip("\t"))


# This global string is used so append_token() can clear its value in get_line_data().
value_str = ""

def get_line_data(line, multiline):
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

	global value_str

	line_data = []

	# parsing_property_or_value = "property" # TODO: Can this be used instead?
	parsing_property_or_value = "extra" if multiline else "property"

	seen_equals = False
	was_prev_char_special = True # "special" meaning whitespace, / or *

	comment_state = State.INSIDE_MULTI_COMMENT if multiline else State.NOT_IN_A_COMMENT

	# print(repr(line))
	for char in line:
		if comment_state in (State.INSIDE_SINGLE_COMMENT, State.INSIDE_MULTI_COMMENT, State.POSSIBLE_MULTI_ENDING):
			value_str += char
		elif char != "=" and not (was_prev_char_special and (char in ("/", "*"))):
			value_str += char

		if comment_state == State.INSIDE_SINGLE_COMMENT: # TODO: Necessary?
			continue

		if char == "=" and not seen_equals and comment_state not in (State.INSIDE_SINGLE_COMMENT, State.INSIDE_MULTI_COMMENT):
			seen_equals = True

			append_token("property", value_str, line_data, 1)
			append_token("extra", "=", line_data, 2)
			parsing_property_or_value = "value"

		if comment_state == State.POSSIBLE_MULTI_ENDING and char == "/":
			comment_state = State.NOT_IN_A_COMMENT
			append_token("extra", value_str, line_data, 3)
		elif comment_state == State.INSIDE_MULTI_COMMENT and char == "*":
			comment_state = State.POSSIBLE_MULTI_ENDING
		elif comment_state == State.READ_FIRST_SLASH:
			if char == "/":
				comment_state = State.INSIDE_SINGLE_COMMENT
				append_token(parsing_property_or_value, value_str, line_data, 4)
				value_str += "//"
			elif char == "*":
				comment_state = State.INSIDE_MULTI_COMMENT
				append_token(parsing_property_or_value, value_str, line_data, 5)
				value_str += "/*"
			else:
				comment_state = State.NOT_IN_A_COMMENT
		elif comment_state == State.NOT_IN_A_COMMENT and char == "/":
			comment_state = State.READ_FIRST_SLASH

		was_prev_char_special = char.isspace() or char in ("/", "*")

	if comment_state in (State.INSIDE_SINGLE_COMMENT, State.INSIDE_MULTI_COMMENT):
		append_token("extra", value_str, line_data, 6)
	else:
		append_token(parsing_property_or_value, value_str, line_data, 7)

	multiline = comment_state == State.INSIDE_MULTI_COMMENT
	return line_data, multiline


def append_token(typ, passed_str, line_data, debug):
	global value_str
	value_str = ""

	# print(debug, typ)

	# Transforms "\t Mass  " to ['\t ', 'Mass', '  '] and appends all of the tokens.
	# TODO: Combine tokens of the same type, like [{'type': 'extra', 'value': ' '}, {'type': 'extra', 'value': '//'}]
	for string in re.findall(r"\S+|\s+", passed_str):
		token = { "type": "extra" if string.isspace() else typ, "value": string }
		line_data.append(token)


####


def convert(parsed):
	ini_rules.apply_rules(parsed)


####


def write_converted_ini_recursively(parsed_portion, output_folder_path):
	# pprint.pprint(parsed_portion)
	for name, dict_or_list in parsed_portion.items():
		if isinstance(dict_or_list, dict): # If dict_or_list contains a dictionary of more filenames.
			write_converted_ini_recursively(dict_or_list, output_folder_path / name)
		else: # If dict_or_list contains a list of the lines of a file.
			# pprint.pprint(dict_or_list)
			with open(str(output_folder_path / name), mode="w") as f:
				lines = []
				for section in dict_or_list:
					get_lines_from_dicts_recursively(section, lines)
				f.write("\n".join(lines))


def get_lines_from_dicts_recursively(line_data, lines):
	# This function loops twice through line_data so the lines can be appended in the correct order.

	line = ""
	for dictionary in line_data:
		if dictionary["type"] != "children":
			line += dictionary["value"]
	lines.append(line)

	for dictionary in line_data:
		if dictionary["type"] == "children":
			for line_data in dictionary["value"]:
				get_lines_from_dicts_recursively(line_data, lines)