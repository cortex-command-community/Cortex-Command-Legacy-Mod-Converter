import os, re
from pathlib import Path
from inspect import getmembers, isfunction
import pprint

from Python.ini_parser import ini_rules


def parse_and_convert(input_folder_path, output_folder_path):
	mod_names = get_mod_names(input_folder_path)
	parsed = parse(output_folder_path, mod_names)
	# pprint.pprint(parsed)
	convert(parsed)
	write_converted_ini_recursively(parsed, Path(output_folder_path))


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
		rough_parsed = []
		rough_parse_file_recursive(rough_parsed, f)
		parsed_file = clean_rough_parsed(rough_parsed)
		return parsed_file


# This global variable is only used by the function below.
# It is necessary due to how a deep function call needs to be able to also change this variable for the less deep function calls.
# Passing it as a function argument makes a copy of the boolean instead of being a reference to the original variable, so that's why a global variable is needed.
is_multiline_comment = False

def rough_parse_file_recursive(rough_parsed, f, depth_tab_count=0):
	"""
	# CC and CCCP use a custom INI format, so the configparser library can't be used here.
	# TODO: Handle // comments.
	# TODO: Check if CCCP allows improper combinations of tabs/spaces.
	# TODO: Check if the first line can be tabbed, because then prev_line_index needs to be initialized to 0.
	# TODO: Check if nested single-line comments in multi-line comments work.
	# TODO: What if there are two or more tabs?

	rough_parsed data structure format:

	[
		{ "property": "AddEffect = MOSRotating", "comment": " // foo", "value": [
			{ "property": "PresetName = Screen Gib" },
			{ "property": "SpriteFile = ContentFile", "value": [
				{ "property": "FilePath = Base.rte/Effects/Gibs/BoneSmallA.png" }
			]
		]}
	]
	"""
	global is_multiline_comment

	previous_file_position = f.tell() # Tracks the file position of a line that needs to be read again.

	for line in iter(f.readline, ""): # This is a workaround of "line in f" due to .tell() being disabled during such a for-loop.
		# print(repr(line))
		tab_count = len(line) - len(line.lstrip("\t"))

		tab_string, line, comment = split_comment(line)
		# print(repr(tab_string), repr(line), repr(comment))

		if tab_count == depth_tab_count:
			line_dict, is_multiline_comment = get_line_dict(tab_string, line, comment, is_multiline_comment)

			rough_parsed.append(line_dict)
		elif tab_count == depth_tab_count + 1:
			line_dict, is_multiline_comment = get_line_dict(tab_string, line, comment, is_multiline_comment)

			prev_line_index = len(rough_parsed) - 1 # - 1 because lists are 0-indexed.
			rough_parsed[prev_line_index]["value"] = []
			rough_parsed[prev_line_index]["value"].append(line_dict)

			rough_parse_file_recursive(rough_parsed[prev_line_index]["value"], f, depth_tab_count+1)
		elif tab_count < depth_tab_count: # Note that this elif statement won't be reached if the line is totally empty, which is desired behavior.
			f.seek(previous_file_position) # Undoes the reading of this line.
			break # Steps back up to the caller so it can try to use the undone line.

		previous_file_position = f.tell()


def split_comment(line):
	line = line.rstrip("\n")

	tab_string = get_tab_string(line)

	"""
	Example split values:
	['']
	['AddEffect = MOSRotating', '    //    foo // bar ///', '']
	['\tPresetName = Screen Gib']
	['', '\t//Mass = 15', '']
	['\tHitsMOs = 0']
	"""
	split = re.split("(\s*\/\/.*)", line)
	# print(split)

	split[0] = split[0].lstrip("\t")

	# Fixes ['', '\t//Mass = 15', ''] -> ['', '//Mass = 15', '']
	if split[0] == "" and len(split) > 1:
		split[1] = split[1].lstrip("\t")

	if len(split) > 1: # If there is a comment it's always at index 1.
		line = split[0]
		comment = split[1]
	else:
		line = split[0]
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


def clean_rough_parsed(rough_parsed):
	"""
	{ "property": "AddEffect = MOSRotating", "comment": " // foo", "value": [
		{ "property": "PresetName = Screen Gib" },
	->
	{ "property": "AddEffect = MOSRotating", "comment": " // foo", "value": [
		{ "property": "PresetName", "value": "Screen Gib" },
	"""
	for line in rough_parsed:
		if "value" in line:
			clean_rough_parsed(line["value"])
		elif "property" in line:
			prop, value = line["property"].split(" = ")
			line["property"] = prop
			line["value"] = value
	return rough_parsed


####


def convert(parsed):
	for _, function in getmembers(ini_rules, isfunction):
		function(parsed)


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