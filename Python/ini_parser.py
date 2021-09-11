import pprint
from collections import OrderedDict


def parse(input_file_path):
	"""
	Parsed data structure format:

	["DataModule"] = None

	["AddEffect = MOSRotating"] = {
		["PresetName = Screen Gib"] = None,
		["SpriteFile = ContentFile"] = {
			["FilePath = Base.rte/Effects/Gibs/BoneSmallA.png"] = None,
		}
	},
	"""

	parsed = OrderedDict()
	with open(input_file_path) as f:
		parse_recursive(parsed, f)
	pprint.pprint(parsed)


# CC and CCCP use a custom INI-inspired file format, so there's probably no Python library out there that can parse it.
# TODO: Handle // comments.
# TODO: Handle (nested) /* */ comments.
# TODO: Check if CCCP allows improper combinations of tabs/spaces.
def parse_recursive(parsed, f, depth_tab_count=0):
	is_comment = False

	for line in f:
		tab_count = len(line) - len(line.lstrip("\t"))

		line = line.strip()

		# TODO: Replace this with a proper way to handle multiline comments.
		if line == "/*":
			is_comment = True
		elif line == "*/":
			is_comment = False

		if is_comment or line == "":
			continue

		# TODO: This part assumes that comments have already been removed due to it assuming " = " only returns two values.
		# if line == "DataModule":
		# 	key = "DataModule"
		# else:
		# 	key = tuple(line.split(" = "))

		# TODO: What if there are two or more tabs?
		if tab_count == depth_tab_count:
			parsed[line] = None # Placeholder for a potential OrderedDict.
		elif tab_count == depth_tab_count + 1:
			parsed[prev_line] = OrderedDict()
			parsed[prev_line][line] = None # Placeholder for a potential OrderedDict.
			parse_recursive(parsed[prev_line], f, depth_tab_count+1)
		elif tab_count < depth_tab_count: # Note that this elif statement won't be reached if the line is blank, which is desired behavior.
			break

		prev_line = line