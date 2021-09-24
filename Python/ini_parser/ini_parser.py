import os, re
from pathlib import Path
import pprint

from Python.ini_parser import ini_rules


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

		if multiline:
			tab_count = depth_tab_count # Prevents multi-line comments from starting a new section.
		else:
			tab_count = len(line) - len(line.lstrip("\t"))

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


	# TODO: Use an enum for this.
	0 = not in a comment
	1 = read the first / of a single-/multi-line comment
	2 = inside a single-line comment
	3 = inside a multi-line comment
	4 = read * which is possibly the ending of a multi-line comment
	"""

	line_data = []

	value_str = ""
	space_str = ""

	# parsing_property_or_value = "property" # TODO: Can this be used instead?
	parsing_property_or_value = "extra" if multiline else "property"

	seen_equals = False
	was_prev_char_special = True # "special" meaning whitespace, / or *

	comment_state = 3 if multiline else 0

	# print(repr(line))
	for char in line:
		if comment_state == 2 or comment_state == 3 or comment_state == 4:
			value_str += char
		elif char != "=" and not (was_prev_char_special and (char == "/" or char == "*")):
			value_str += char

		if comment_state == 2: # TODO: Necessary?
			continue

		if char == "=" and not seen_equals and comment_state != 2 and comment_state != 3:
			seen_equals = True
			value_str = append_token("property", value_str, line_data, 1)
			parsing_property_or_value = "value"

		if comment_state == 4 and char == "/":
			comment_state = 0
			value_str = append_token("extra", value_str, line_data, 2)
		elif comment_state == 3 and char == "*":
			comment_state = 4
		elif comment_state == 1:
			if char == "/":
				comment_state = 2
				value_str = append_token(parsing_property_or_value, value_str, line_data, 3)
				value_str += "//"
			elif char == "*":
				comment_state = 3
				value_str = append_token(parsing_property_or_value, value_str, line_data, 4)
				value_str += "/*"
			else:
				comment_state = 0
		elif comment_state == 0 and char == "/":
			comment_state = 1

		was_prev_char_special = char.isspace() or char == "/" or char == "*"

	if comment_state == 2 or comment_state == 3:
		append_token("extra", value_str, line_data, 5)
	else:
		append_token(parsing_property_or_value, value_str, line_data, 6)

	multiline = comment_state == 3
	return line_data, multiline


def append_token(typ, value_str, line_data, debug):
	# print(debug)
	# print(typ)

	if value_str.strip() != "":
		if typ == "property" or typ == "value":
			token = { "type": typ, "value": value_str.strip() }
		else:
			token = { "type": typ, "value": value_str.rstrip() }

		line_data.append(token)

	return get_whitespace_on_right(value_str)


def get_whitespace_on_right(string):
	return string.replace(string.rstrip(), "")


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
	""" The function needs to loop twice through line_data to have lines written in the correct order. """

	line = ""
	for dictionary in line_data:
		if dictionary["type"] != "children":
			line += dictionary["value"]
	lines.append(line)

	for dictionary in line_data:
		if dictionary["type"] == "children":
			for line_data in dictionary["value"]:
				get_lines_from_dicts_recursively(line_data, lines)