import os, re
from pathlib import Path
import pprint

from Python.ini_parser import ini_rules


def parse_and_convert(input_folder_path, output_folder_path):
	mod_names = get_mod_names(input_folder_path)
	parsed = initialize_parsed(output_folder_path, mod_names)

	convert(parsed)
	# pprint.pprint(parsed)

	write_converted_ini_recursively(parsed, Path(output_folder_path))


def get_mod_names(input_folder_path):
	return [p.name for p in Path(input_folder_path).iterdir() if p.suffix == ".rte" and p.is_dir()]


def initialize_parsed(subfolder_path, mod_names):
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
			parsed[name] = initialize_parsed(p, mod_names)
	return parsed


def part_of_mod(p, mod_names):
	return any(mod_name in str(p) for mod_name in mod_names)


def parse_file(file_path):
	# print(file_path)
	with open(file_path) as f:
		parsed = []
		rough_parse_file_recursive(parsed, f)
		parsed_file = clean_rough_parsed(parsed)
		return parsed_file


# This global variable is only used by the function below.
# It is necessary due to how a deep function call needs to be able to also change this variable for the less deep function calls.
# Passing it as a function argument makes a copy of the boolean instead of being a reference to the original variable, so that's why a global variable is needed.
is_multiline_comment = False

def rough_parse_file_recursive(parsed, f, depth_tab_count=0):
	"""
	# CC and CCCP use a custom INI format, so the configparser library can't be used to parse the INI files.
	# TODO: Check if the first line can be tabbed, because then prev_line_index needs to be initialized to 0.
	"""

	global is_multiline_comment

	for line in iter(f.readline, ""): # This is a workaround of "line in f" due to .tell() being disabled during such a for-loop.
		# print(repr(line))
		tab_count = len(line) - len(line.lstrip("\t"))

		tab_string, line, comment = split_comment(line)
		# print(repr(tab_string), repr(line), repr(comment))

		line_dict, is_multiline_comment = get_line_dict(tab_string, line, comment, is_multiline_comment)

		if tab_count == depth_tab_count:
			parsed.append(line_dict)
		elif tab_count == depth_tab_count + 1:
			prev_line_index = len(parsed) - 1
			parsed[prev_line_index]["value"] = []
			parsed[prev_line_index]["value"].append(line_dict)

			child_values = rough_parse_file_recursive(parsed[prev_line_index]["value"], f, depth_tab_count+1)
			if child_values != None and child_values["tab_count"] == depth_tab_count:
				parsed.append(child_values["line_dict"])
			else:
				return child_values
		elif tab_count < depth_tab_count:
			return { "line_dict": line_dict, "tab_count": tab_count }


def split_comment(line):
	line = line.rstrip("\n")

	tab_string = get_tab_string(line)

	"""
	Example split_by_comment values:
	['']
	['AddEffect = MOSRotating', '    //    foo // bar ///', '']
	['\tPresetName = Screen Gib']
	['', '\t//Mass = 15', '']
	['\tHitsMOs = 0']
	"""
	split_by_comment = re.split("(\s*\/\/.*)", line)
	# print(split_by_comment)

	split_by_comment[0] = split_by_comment[0].lstrip("\t")

	# Transforms ['', '\t//Mass = 15', ''] to ['', '//Mass = 15', '']
	if split_by_comment[0] == "" and len(split_by_comment) > 1:
		split_by_comment[1] = split_by_comment[1].lstrip("\t")

	if len(split_by_comment) > 1: # If there is a comment it'll always be at index 1.
		line = split_by_comment[0]
		comment = split_by_comment[1]
	else:
		line = split_by_comment[0]
		comment = ""

	return tab_string, line, comment


def get_tab_string(line):
	"""
	Returns the string of tabs before the INI property, else it returns an empty string.
	TODO: Replace with regex.
	"""
	for tab_count, string in enumerate(line.split("\t")):
		if string != "":
			return tab_count * "\t"
	return len(line) * "\t"


def get_line_dict(tab_string, line, comment, is_multiline_comment):
	# print(repr(tab_string), repr(line), repr(comment), repr(is_multiline_comment))
	line_dict = { "tab_string": tab_string }

	# TODO: Can't assume that /* means the entire line is a comment, and vice versa with */ !

	# TODO: What if the string is "\t//*"? What if it's "\t///*"?

	if "/*" in line:
		is_multiline_comment = True

	if is_multiline_comment:
		line_dict["comment"] = line

		if comment:
			line_dict["comment"] += comment

		if "*/" in line:
			is_multiline_comment = False
	else:
		if comment:
			line_dict["comment"] = comment
		if line:
			line_dict["property"] = line

	return line_dict, is_multiline_comment


# TODO: Maybe rough_parse_file_recursive() can do everything this function does?
def clean_rough_parsed(parsed):
	"""
	{ "property": "AddEffect = MOSRotating", "comment": " // foo", "value": [
		{ "property": "PresetName = Screen Gib" },
	->
	{ "property": "AddEffect = MOSRotating", "comment": " // foo", "value": [
		{ "property": "PresetName", "value": "Screen Gib" },
	"""
	for line in parsed:
		if "value" in line:
			clean_rough_parsed(line["value"])
		elif "property" in line:
			prop, value = line["property"].split(" = ")
			line["property"] = prop
			line["value"] = value
	return parsed


####


def convert(parsed):
	ini_rules.apply_rules(parsed)


####


def write_converted_ini_recursively(parsed_portion, output_folder_path):
	for name, dict_or_list in parsed_portion.items():
		if isinstance(dict_or_list, dict): # If dict_or_list contains a dictionary of more filenames.
			write_converted_ini_recursively(dict_or_list, output_folder_path / name)
		else: # If dict_or_list contains a list of the lines of a file.
			with open(str(output_folder_path / name), mode="w") as f:
				lines = []
				get_lines_from_dicts_recursively(dict_or_list, lines)
				f.write("\n".join(lines))


def get_lines_from_dicts_recursively(dict_list, lines):
	# TODO: Refactor this function.
	for line_dict in dict_list:
		line = ""

		line += line_dict["tab_string"]

		if "property" in line_dict:
			line += line_dict["property"]

		if "value" in line_dict:
			value = line_dict["value"]

			if isinstance(value, str):
				line += " = " + value

				if "comment" in line_dict:
					line += line_dict["comment"]

				lines.append(line)
			else: # If the next line is tabbed, value is a dictionary.
				if "comment" in line_dict:
					line += line_dict["comment"]

				lines.append(line)

				get_lines_from_dicts_recursively(value, lines)
		elif "comment" in line_dict:
			line += line_dict["comment"]
			lines.append(line)
		elif "tab_string" in line_dict:
			lines.append(line)