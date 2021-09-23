import os, re
from pathlib import Path
import pprint

from Python.ini_parser import ini_rules


def parse_and_convert(input_folder_path, output_folder_path):
	mod_names = get_mod_names(input_folder_path)
	parsed = parse(output_folder_path, mod_names)

	# convert(parsed)
	# pprint.pprint(parsed)

	# write_converted_ini_recursively(parsed, Path(output_folder_path))


def get_mod_names(input_folder_path):
	return [p.name for p in Path(input_folder_path).iterdir() if p.suffix == ".rte" and p.is_dir()]


def parse(subfolder_path, mod_names):
	parsed = {}
	for name in os.listdir(subfolder_path):
		p = subfolder_path / Path(name)

		if ".rte" not in str(p):
			continue
		elif not part_of_mod(p, mod_names): # TODO: Remove this once CCCP has a Mods folder that can be iterated over.
			continue

		if p.is_file() and p.suffix == ".ini" and p.stem != "desktop": # Skip the desktop.ini Windows metadata file.
			parsed[name] = parse_file(str(p))

		if p.is_dir():
			parsed[name] = parse(p, mod_names)
	return parsed


def part_of_mod(p, mod_names):
	return any(mod_name in str(p) for mod_name in mod_names)


def parse_file(file_path):
	# print(file_path)
	with open(file_path) as f:
		parsed = []
		rough_parse_file_recursive(parsed, f)
		# parsed = clean_rough_parsed(parsed)
		return parsed


# This global variable is only used by the function below.
# It is necessary due to how a deep function call needs to be able to also change this variable for the less deep function calls.
# Passing it as a function argument makes a copy of the boolean instead of being a reference to the original variable, so that's why a global variable is needed.
multiline = False

def rough_parse_file_recursive(parsed, f, depth_tab_count=0):
	"""
	# CC and CCCP use a custom INI format, so the configparser library can't be used to parse the INI files.
	# TODO: Check if the first line can be tabbed, because then prev_line_index needs to be initialized to 0.
	"""

	global multiline

	for line in f:
		# print(repr(line))
		line = line.strip("\n")
		tab_count = len(line) - len(line.lstrip("\t"))

		line_data, multiline = get_line_data(line, multiline)
		print(line_data)
		# return # TODO: Remove this!

		if tab_count == depth_tab_count:
			parsed.append(line_data)
		elif tab_count == depth_tab_count + 1:
			a = parsed[-1]
			a.append( { "type": "children", "value": [] } )
			b = a[-1]["value"]
			b.append(line_data)

			child_values = rough_parse_file_recursive(b, f, depth_tab_count+1)
			if child_values != None and child_values["tab_count"] == depth_tab_count:
				parsed.append(child_values["line_data"])
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

	parsing_type = "multi_comment" if multiline else "property"
	prev_parsing_type = "property" # Used so parsing_type can be set back when a multiline comment ends.

	seen_equals = False
	was_prev_char_special = True # "special" meaning whitespace, / or *

	comment_state = 3 if multiline else 0

	# print(repr(line))
	# TODO: Find a way to have every value_str = "" call done by append_token()
	for char in line:
		# TODO: Clean this messy if-statement up.
		# if (char != "=" or parsing_type == "single_comment") and not (was_prev_char_special and (char == "/" or char == "*") and parsing_type != "single_comment"):
		# 	value_str += char

		if parsing_type == "single_comment" or parsing_type == "multi_comment":
			value_str += char
		elif char != "=" and not (was_prev_char_special and (char == "/" or char == "*")):
			value_str += char

		if parsing_type == "single_comment": # TODO: Necessary?
			continue

		if char == "=" and not seen_equals:
			seen_equals = True
			value_str = append_token("property", value_str, line_data, 1)
			parsing_type = "value"

		if comment_state == 4 and char == "/":
			comment_state = 0
			value_str = append_token("extra", value_str, line_data, 2)
			parsing_type = prev_parsing_type
		elif comment_state == 3 and char == "*":
			comment_state = 4
		elif comment_state == 1:
			if char == "/":
				comment_state = 2
				value_str = append_token(parsing_type, value_str, line_data, 3)
				# value_str += "//"
				parsing_type = "single_comment"
			elif char == "*":
				comment_state = 3
				value_str = append_token(parsing_type, value_str, line_data, 4)
				value_str += "/*"
				prev_parsing_type = parsing_type
				parsing_type = "multi_comment"
		elif comment_state == 0 and char == "/":
			comment_state = 1

		was_prev_char_special = char.isspace() or char == "/" or char == "*"

	if parsing_type == "single_comment" or parsing_type == "multi_comment":
		append_token("extra", value_str, line_data, 5)
	elif parsing_type == "value": # TODO: Can this be moved into the above for-loop?
		append_token(parsing_type, value_str, line_data, 6)

	multiline = comment_state == 3
	return line_data, multiline


def append_token(typ, value_str, line_data, debug):
	print(debug)
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


# TODO: Maybe rough_parse_file_recursive() can do everything this function does?
# def clean_rough_parsed(parsed):
# 	"""
# 	{ "property": "AddEffect = MOSRotating", "comment": " // foo", "value": [
# 		{ "property": "PresetName = Screen Gib" },
# 	->
# 	{ "property": "AddEffect = MOSRotating", "comment": " // foo", "value": [
# 		{ "property": "PresetName", "value": "Screen Gib" },
# 	"""
# 	for line in parsed:
# 		if "value" in line:
# 			clean_rough_parsed(line["value"])
# 		elif "property" in line:
# 			prop, value = line["property"].split(" = ")
# 			line["property"] = prop
# 			line["value"] = value
# 	return parsed


####


# def convert(parsed):
# 	ini_rules.apply_rules(parsed)


####


# def write_converted_ini_recursively(parsed_portion, output_folder_path):
# 	for name, dict_or_list in parsed_portion.items():
# 		if isinstance(dict_or_list, dict): # If dict_or_list contains a dictionary of more filenames.
# 			write_converted_ini_recursively(dict_or_list, output_folder_path / name)
# 		else: # If dict_or_list contains a list of the lines of a file.
# 			with open(str(output_folder_path / name), mode="w") as f:
# 				lines = []
# 				get_lines_from_dicts_recursively(dict_or_list, lines)
# 				f.write("\n".join(lines))


# def get_lines_from_dicts_recursively(dict_list, lines):
# 	# TODO: Refactor this function.
# 	for line_data in dict_list:
# 		line = ""

# 		line += line_data["tab_string"]

# 		if "property" in line_data:
# 			line += line_data["property"]

# 		if "value" in line_data:
# 			value = line_data["value"]

# 			if isinstance(value, str):
# 				line += " = " + value

# 				if "comment" in line_data:
# 					line += line_data["comment"]

# 				lines.append(line)
# 			else: # If the next line is tabbed, value is a dictionary.
# 				if "comment" in line_data:
# 					line += line_data["comment"]

# 				lines.append(line)

# 				get_lines_from_dicts_recursively(value, lines)
# 		elif "comment" in line_data:
# 			line += line_data["comment"]
# 			lines.append(line)
# 		elif "tab_string" in line_data:
# 			lines.append(line)