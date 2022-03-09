import pprint

from Python import thumbnail_generator


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


def apply_rules_on_ini_cst(parsed_subset):
	# print(pprint.pprint(parsed_subset))
	for key, value in parsed_subset.items():
		if isinstance(value, dict):
			apply_rules_on_ini_cst(value)
		else: # If it's a list of the sections of a file.
			apply_rules_on_sections(value)


def apply_rules_on_sections(parsed_subset):
	for section in parsed_subset:
		for token in section:
			if token["type"] == "children":
				children = token["content"]

				# TODO: Remove contains_property_shallowly() and write out what they do in this function
				if contains_property_shallowly(children, "MaxMass"):
					max_mass_to_max_inventory_mass(children)

				iconfile_path = iconfile_path_to_thumbnail_generator(children)

				for line_tokens in children:
					replace_property_and_value(line_tokens, "MinThrottleRange", "NegativeThrottleMultiplier", min_throttle_range_to_negative_throttle_multiplier)
					replace_property_and_value(line_tokens, "MaxThrottleRange", "PositiveThrottleMultiplier", max_throttle_range_to_positive_throttle_multiplier)

		# TODO: Remove contains_property_and_value_shallowly() and write out what it does in this function
		# TODO: I don't remember whether this one works
		if contains_property_and_value_shallowly(section, "AddActor", "Leg"):
			for token in section:
				if token["type"] == "children":
					children = token["content"]

					max_length_to_offsets(children)


def contains_property_shallowly(children, prop):
	""" This function deliberately doesn't check the section's contents recursively. """
	return [True for line_tokens in children for token in line_tokens if token["type"] == "property" and token["content"] == prop] != []


def contains_property_and_value_shallowly(section, prop, value):
	contains_property = contains_value = False

	for token in section:
		if token["type"] == "property" and token["content"] == prop:
			contains_property = True
		if token["type"] == "value" and token["content"] == value:
			contains_value = True

	return contains_property and contains_value


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


def iconfile_path_to_thumbnail_generator(children):
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
									thumbnail_generator.generate_thumbnail(iconfile_path)


def duplicate_script_path(parsed_subset):
	pass