from Python.ini_converting import ini_rules_utils

from Python import thumbnail_generator
from Python.ini_converting import ini_fix_duplicate_scripts
from Python import shared_globals as cfg


"""
{
	"foo.rte": {
		"Foo.ini": ini_cst,
		"FolderName": {
			"Bar.ini": ini_cst,
		}
	}
}
"""


def apply_rules_on_ini_cst(ini_cst, output_folder_path):
	apply_rules_on_ini_cst_recursively(ini_cst, output_folder_path)
	ini_fix_duplicate_scripts.run(ini_cst)


def apply_rules_on_ini_cst_recursively(parsed_subset, output_folder_path):
	for key, value in parsed_subset.items():
		if isinstance(value, dict):
			apply_rules_on_ini_cst_recursively(value, output_folder_path)
		else: # If it's a list of the sections of a file.
			apply_rules_on_sections(value, output_folder_path)


def apply_rules_on_sections(parsed_subset, output_folder_path):
	for section in parsed_subset:
		for token in section:
			if token["type"] == "children":
				children = token["content"]

				if ini_rules_utils.children_contain_property_shallowly(children, "MaxMass"):
					max_mass_to_max_inventory_mass(children)

				iconfile_path_to_thumbnail_generator(children, output_folder_path)

				for line_tokens in children:
					replace_property_and_value(line_tokens, "MinThrottleRange", "NegativeThrottleMultiplier", min_throttle_range_to_negative_throttle_multiplier)
					replace_property_and_value(line_tokens, "MaxThrottleRange", "PositiveThrottleMultiplier", max_throttle_range_to_positive_throttle_multiplier)

				shovel_flash_fix(children)

		if ini_rules_utils.line_contains_property_and_value(section, "AddActor", "Leg"):
			for token in section:
				if token["type"] == "children":
					children = token["content"]

					max_length_to_offsets(children)

		add_grip_strength_if_missing(section)


def max_mass_to_max_inventory_mass(children):
	""" MaxInventoryMass = MaxMass - Mass """

	mass = 0 # The Mass is optionally defined in the INI file.

	# TODO: Find a way to split these into subfunctions.
	for line_tokens in children:
		for token in line_tokens:
			if token["type"] == "property":
				if token["content"] == "Mass":
					for token_2 in line_tokens:
						if token_2["type"] == "value":
							mass = float(token_2["content"])
							break

				if token["content"] == "MaxMass":
					for token_2 in line_tokens:
						if token_2["type"] == "value":
							max_mass = float(token_2["content"])
							break

	max_inventory_mass = remove_excess_zeros(max_mass - mass)

	for line_tokens in children:
		for token in line_tokens:
			if token["type"] == "property":
				if token["content"] == "MaxMass":
					token["content"] = "MaxInventoryMass"

					for token_2 in line_tokens:
						if token_2["type"] == "value":
							token_2["content"] = max_inventory_mass
							return


def remove_excess_zeros(string):
	return f"{string:g}"


def replace_property_and_value(line_tokens, old_property, new_property, new_value_function):
	for token in line_tokens:
		if token["type"] == "property":
			if token["content"] == old_property:
				token["content"] = new_property
				for token_2 in line_tokens:
					if token_2["type"] == "value":
						token_2["content"] = new_value_function(token_2["content"])
						return


def min_throttle_range_to_negative_throttle_multiplier(old_value):
	new_value = abs(1 - abs(float(old_value)))
	return remove_excess_zeros(new_value)


def max_throttle_range_to_positive_throttle_multiplier(old_value):
	new_value = abs(1 + abs(float(old_value)))
	return remove_excess_zeros(new_value)


# TODO: Refactor max_length_to_offsets and max_length_to_offsets_2
def max_length_to_offsets(children):
	"""
	If the parent line is AddActor = Leg:
	MaxLength = old_value
	->
	ContractedOffset = Vector
		X = old_value / 2
		Y = 0
	ExtendedOffset = Vector
		X = old_value
		Y = 0
	"""

	for index, line_tokens in enumerate(children):
		old_value = max_length_to_offsets_2(line_tokens)

		if old_value != None:
			# print(index, old_value)

			# TODO: Can this be done with .append() instead of .insert() ?
			children.insert(index + 1, [
				{ "type": "extra", "content": "\t" },
				{ "type": "property", "content": "ExtendedOffset" },
				{ "type": "extra", "content": " "}, {"type": "extra", "content": "="}, {"type": "extra", "content": " "},
				{ "type": "value", "content": "Vector" },
				{ "type": "extra", "content": "\n" },
				{ "type": "children", "content": [
					[
						{ "type": "extra", "content": "\t\t" },
						{ "type": "property", "content": "X" },
						{ "type": "extra", "content": " "}, {"type": "extra", "content": "="}, {"type": "extra", "content": " "},
						{ "type": "value", "content": remove_excess_zeros(old_value) },
						{ "type": "extra", "content": "\n" },
					],
					[
						{ "type": "extra", "content": "\t\t" },
						{ "type": "property", "content": "Y" },
						{ "type": "extra", "content": " "}, {"type": "extra", "content": "="}, {"type": "extra", "content": " "},
						{ "type": "value", "content": remove_excess_zeros(0) },
						{ "type": "extra", "content": "\n" },
					]
				]}
			])


def max_length_to_offsets_2(line_tokens):
	for token in line_tokens:
		if token["type"] == "property":
			if token["content"] == "MaxLength":
				token["content"] = "ContractedOffset"

				for token_2 in line_tokens:
					if token_2["type"] == "value":
						old_value = float(token_2["content"])
						token_2["content"] = "Vector"

						line_tokens.append( { "type": "children", "content": [
							[
								{ "type": "extra", "content": "\t\t" },
								{ "type": "property", "content": "X" },
								{ "type": "extra", "content": " "}, {"type": "extra", "content": "="}, {"type": "extra", "content": " "},
								{ "type": "value", "content": remove_excess_zeros(old_value / 2) },
								{ "type": "extra", "content": "\n" },
							],
							[
								{ "type": "extra", "content": "\t\t" },
								{ "type": "property", "content": "Y" },
								{ "type": "extra", "content": " "}, {"type": "extra", "content": "="}, {"type": "extra", "content": " "},
								{ "type": "value", "content": remove_excess_zeros(0) },
								{ "type": "extra", "content": "\n" },
							]
						] } )

						return old_value


def iconfile_path_to_thumbnail_generator(children, output_folder_path):
	for line_tokens in children:
		if {"type": "property", "content": "IconFile"} in line_tokens and {"type": "value", "content": "ContentFile"} in line_tokens:
			for token in line_tokens:
				if token["type"] == "children":
					subchildren = token["content"]
					# print(subchildren)

					for subline_tokens in subchildren:
						if {"type": "property", "content": "FilePath"} in subline_tokens:
							# print(subline_tokens)
							for subtoken in subline_tokens:
								if subtoken["type"] == "value":
									# print(subtoken)
									iconfile_path = subtoken["content"]
									thumbnail_generator.generate_thumbnail(iconfile_path, output_folder_path)


def duplicate_script_path(parsed_subset):
	pass


def shovel_flash_fix(children):
	"""
	SpriteFile = ContentFile
		FilePath = Ronin.rte/Effects/Pyro/Flashes/ShovelFlash.png
	FrameCount = 2
	->
	SpriteFile = ContentFile
		FilePath = Ronin.rte/Devices/Tools/Shovel/Effects/ShovelFlash.png
	FrameCount = 1
	"""

	# TODO: Make this recursive somehow.
	for line_tokens in children:
		for token in line_tokens:
			if token["type"] == "property":
				if token["content"] == "SpriteFile":
					# TODO: Check if the value "ContentFile" is also used, because "SpriteFile" might be able to have other values in the future!

					for token_2 in line_tokens:
						if token_2["type"] == "children":
							for subline_tokens in token_2["content"]:
								for subtoken in subline_tokens:
									if subtoken["type"] == "property" and subtoken["content"] == "FilePath":
										for subtoken in subline_tokens:
											if subtoken["type"] == "value" and subtoken["content"] in ("Ronin.rte/Devices/Sprites/ShovelFlash.bmp", "Ronin.rte/Effects/Pyro/Flashes/ShovelFlash.png"):
												subtoken["content"] = "Ronin.rte/Devices/Tools/Shovel/Effects/ShovelFlash.png"

												shovel_flash_fix_change_frame_count(children)


def shovel_flash_fix_change_frame_count(children):
	for line_tokens2 in children:
		for token2 in line_tokens2:
			if token2["type"] == "property":
				if token2["content"] == "FrameCount":
					for token3 in line_tokens2:
						if token3["type"] == "value":
							if token3["content"] == "2":
								token3["content"] = "1"


def add_grip_strength_if_missing(section):
	"""
	TODO: Check if this description is accurate to what *actually* was decided between me and Gacyr regarding the future behavior of GripStrength.

	GripStrength was added in pre4 as an optional property to Arms.
	It defaulted to JointStrength if it wasn't defined for an Arm, but this suddenly caused a lot of actors in old mods to throw their HeldDevices away.
	In response, pre4.1 made JointStrength a non-optional property, with the idea being that this function could then fix old mods by adding GripStrength = <high_value> to them.
	"""

	# TODO: Make this recursive somehow.
	if ini_rules_utils.line_contains_property_and_value(section, "AddActor", "Arm"):
		for token in section:
			if token["type"] == "children":
				children = token["content"]

				# The second condition will make sure that GripStrength isn't added to an Arm without a GripStrength
				# that CopyOfs an Arm that *does* have a GripStrength.
				if (
					not ini_rules_utils.children_contain_property_shallowly(children, "GripStrength") and
					not ini_rules_utils.children_contain_property_shallowly(children, "CopyOf")
					):
					children.append([
						{ "type": "extra", "content": "\t" },
						{ "type": "property", "content": "GripStrength" },
						{ "type": "extra", "content": " "}, {"type": "extra", "content": "="}, {"type": "extra", "content": " "},
						{ "type": "value", "content": str(cfg.ARBITRARILY_HIGH_DEFAULT_GRIP_STRENGTH) },
						{ "type": "extra", "content": "\n" },
					])
