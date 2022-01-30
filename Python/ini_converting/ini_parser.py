import os, re
import pprint
from pathlib import Path
from enum import Enum, auto

from Python.reading_types import ReadingTypes

from Python.ini_converting import ini_rules
from Python.ini_converting import ini_writer


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

	ini_rules.apply_rules_on_parsed(parsed)
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


def parse_file_recursively(parsed_portion, f, depth_tab_count=0):
	"""
	# CC and CCCP use a custom INI format, so the configparser library can't be used to parse the INI files.
	# TODO: Check if the first line can be tabbed, because then prev_line_index needs to be initialized to 0.
	"""

	for line_number, line in enumerate(f, start=1):
		# print(repr(line))
		line = line.strip("\n")

		line_data, tab_count = get_line_data(line, depth_tab_count)
		print(line_data)

		if tab_count == depth_tab_count:
			parsed_portion.append(line_data)
		elif tab_count == depth_tab_count + 1:
			if parsed_portion == []:
				file_path = f.name
				raise TabError(f"\nWrong tabbing on line {line_number} in file {file_path} on line '{line}'")

			previous_appended_line_data = parsed_portion[-1]

			previous_appended_line_data.append( { "type": "children", "content": [ line_data ] } )

			child_line_data = previous_appended_line_data[-1]["content"]

			child_return_values = parse_file_recursively(child_line_data, f, depth_tab_count+1)

			if child_return_values != None and child_return_values["tab_count"] == depth_tab_count:
				parsed_portion.append(child_return_values["line_data"])
			else:
				return child_return_values
		elif tab_count < depth_tab_count:
			child_return_values = { "line_data": line_data, "tab_count": tab_count }
			return child_return_values


# This global variable is necessary due to how a deep function call needs to be able to also change this variable for the less deep function calls.
# Passing it as a function argument would copy it by value instead of by reference.
# multiline = False

def get_line_data(line, depth_tab_count):
	"""
	The returned line_data looks like this:
	[
		{ "type": "extra", "content": "\t" },
		{ "type": "property", "content": "Mass" },
		{ "type": "value", "content": "2400" },
		{ "type": "extra", "content": " /* */ foo /*" },
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
	"""

	line_data = []

	comment = False

	string = ""
	unidentified_string = ""

	seen_equals = False

	"""
	a b  =  c d
	"""

	for char in line:
		if char.isspace():
			unidentified_string += char
		elif char == "=":
			seen_equals = True
			unidentified_string += char
		else:
			if unidentified_string != "":
				if seen_equals:
					line_data.append({ "type": ReadingTypes.PROPERTY, "content": string })
					string = ""
					line_data.append({ "type": ReadingTypes.EXTRA, "content": unidentified_string })
					unidentified_string = ""

				string += unidentified_string + char
				unidentified_string = ""
			else:
				string += char

	line_data.append({ "type": ReadingTypes.VALUE, "content": string })

	tab_count = depth_tab_count

	return line_data, tab_count
