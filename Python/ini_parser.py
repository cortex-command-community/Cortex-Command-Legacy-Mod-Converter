import os
from pathlib import Path
# import pprint
from collections import OrderedDict


def parse(subfolder_path):
	parsed = {}
	for name in os.listdir(subfolder_path):
		p = subfolder_path / Path(name)
		if p.is_file() and p.suffix == ".ini" and p.name != "desktop.ini": # Skip the desktop.ini Windows metadata file.
			parsed[name] = parse_file(str(p))
		if p.is_dir():
			parsed[name] = parse(p)
	return parsed


def parse_file(file_path):
	rough_parsed = OrderedDict()
	with open(file_path) as f:
		rough_parse_recursive(rough_parsed, f)
	parsed_file = clean_rough_parsed(rough_parsed)
	# pprint.pprint(parsed_file)
	return parsed_file


def rough_parse_recursive(rough_parsed, f, depth_tab_count=0):
	"""
	# CC and CCCP use a custom INI-inspired file format, so the configparser library wouldn't help here.
	# TODO: Handle // comments.
	# TODO: Check if CCCP allows improper combinations of tabs/spaces.

	rough_parsed data structure format:

	OrderedDict([
		('AddEffect = MOSRotating', OrderedDict([
			('PresetName = Screen Gib', None),
			('SpriteFile = ContentFile', OrderedDict([
				('FilePath = Base.rte/Effects/Gibs/BoneSmallA.png', None)
			])),
			('AtomGroup = AtomGroup', OrderedDict([
				('Material = Material', OrderedDict([
					('CopyOf = Metal', None)
				])),
				('Resolution = 6', None),
			])),
		]))
	])
	"""

	is_comment = False
	previous_file_position = f.tell() # This variable's purpose is to track the file position of an unused line.

	for line in iter(f.readline, ""): # This is a workaround of "line in f" due to .tell() being disabled during such a for-loop.
		tab_count = len(line) - len(line.lstrip("\t"))

		line = line.split("//")[0] # Removes single line comments.
		line = line.strip() # Removes whitespace.

		if line == "/*":
			is_comment = True
		elif line == "*/":
			is_comment = False
			continue # TODO: Is it possible for a multiline to end on the same line as an INI line statement?

		if is_comment or line == "":
			continue

		# TODO: What if there are two or more tabs?
		if tab_count == depth_tab_count:
			rough_parsed[line] = None # Placeholder for a potential OrderedDict.
		elif tab_count == depth_tab_count + 1:
			rough_parsed[prev_line] = OrderedDict()
			rough_parsed[prev_line][line] = None # Placeholder for a potential OrderedDict.

			rough_parse_recursive(rough_parsed[prev_line], f, depth_tab_count+1)
		elif tab_count < depth_tab_count: # Note that this elif statement won't be reached if the line is totally empty, which is desired behavior.
			f.seek(previous_file_position) # Undoes the reading of this line.
			break # Steps back up to the caller so it can try to use the undone line.

		prev_line = line
		previous_file_position = f.tell()


def clean_rough_parsed(rough_parsed):
	"""
	OrderedDict([
		('AddEffect = MOSRotating', OrderedDict([
			('PresetName = Screen Gib', None),
	->
	OrderedDict([
		('AddEffect = MOSRotating', OrderedDict([
			('PresetName', 'Screen Gib'),
	"""
	for k, v in list(rough_parsed.items()): # list() is to get around the "OrderedDict mutated during iteration" error.
		if v == None:
			rough_parsed[k.split(" = ")[0]] = k.split(" = ")[1] # Replaces the None value with the right side of the equality in the key, and replaces the key with the left side of the equality in the key.
			del rough_parsed[k]
		else:
			rough_parsed[k] = rough_parsed.pop(k) # This is solely to preserve the order of values in the OrderedDictionary.
			clean_rough_parsed(v)
	return rough_parsed