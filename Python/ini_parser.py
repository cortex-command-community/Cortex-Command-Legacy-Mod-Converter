import pprint
from collections import OrderedDict


def parse(input_file_path):
	rough_parsed = OrderedDict()
	with open(input_file_path) as f:
		rough_parse_recursive(rough_parsed, f)
	pprint.pprint(rough_parsed)


# CC and CCCP use a custom INI-inspired file format, so that's why this code spaghetti is necessary.
# TODO: Handle // comments.
# TODO: Check if CCCP allows improper combinations of tabs/spaces.
def rough_parse_recursive(rough_parsed, f, depth_tab_count=0):
	"""
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
			])
		)
	])
	"""

	is_comment = False
	start_file_position = f.tell()

	for line in iter(f.readline, ""): # This is a workaround of "line in f" due to .tell() being disabled during such a for-loop.
		tab_count = len(line) - len(line.lstrip("\t"))

		line = line.strip()

		if line == "/*":
			is_comment = True
		elif line == "*/":
			is_comment = False
			continue

		if is_comment or line == "":
			continue

		# TODO: What if there are two or more tabs?
		if tab_count == depth_tab_count:
			rough_parsed[line] = None # Placeholder for a potential OrderedDict.
		elif tab_count == depth_tab_count + 1:
			rough_parsed[prev_line] = OrderedDict()
			rough_parsed[prev_line][line] = None # Placeholder for a potential OrderedDict.

			previous_file_position = rough_parse_recursive(rough_parsed[prev_line], f, depth_tab_count+1)
			if previous_file_position != None:
				f.seek(previous_file_position) # Recycles an unused line.
		elif tab_count < depth_tab_count: # Note that this elif statement won't be reached if the line is totally empty, which is desired behavior.
			return start_file_position

		prev_line = line
		start_file_position = f.tell()