import pprint


"""
The structure of the "parsed" variable that's passed to the apply_rules function looks like this,
where the "v" character is used to point down:

{
	"foo.rte": {
		"FolderName": {
			"Bar.ini": [ < holds sections of a file
				section and also line_data
				v   token
				[   v
					{ "type": "extra", "value": "// foo" }
				],

				section and also line_data
				v   token
				[   v
					{ "type": "children", "value": [
						line_data
						v   token
						[   v
							{ "type": "property", "value": "PresetName" },
							{ "type": "value", "value": "foo" }
						]
					]}
				]
			]
		}
	}
}
"""


def apply_rules(parsed_subset):
	# print(pprint.pprint(parsed_subset))
	for key, value in parsed_subset.items():
		if isinstance(value, dict):
			apply_rules(value)
		else: # If it's a list of the sections of a file.
			for children in [token["value"] for section in value for token in section if token["type"] == "children"]:
				if children_contain_property_shallowly(children, "Mass") and children_contain_property_shallowly(children, "MaxMass"):
					max_mass_to_max_inventory_mass(children)

				# TODO: Uncomment this!!!
				# for line_data in children:
				# 	replace_property_and_value(line_data, "MinThrottleRange", "NegativeThrottleMultiplier", min_throttle_range_to_negative_throttle_multiplier)
				# 	replace_property_and_value(line_data, "MaxThrottleRange", "PositiveThrottleMultiplier", max_throttle_range_to_positive_throttle_multiplier)

				max_length_to_offsets(children)


def children_contain_property_shallowly(children, prop):
	""" This function deliberately doesn't check the section's contents recursively. """
	return [True for line_data in children for token in line_data if token["type"] == "property" and token["value"] == prop] != []


def max_mass_to_max_inventory_mass(children):
	""" MaxInventoryMass = MaxMass - Mass """
	# TODO: Find a way to split these into subfunctions.
	for line_data in children:
		for token in line_data:
			if token["type"] == "property":
				if token["value"] == "Mass":
					for token_2 in line_data:
						if token_2["type"] == "value":
							mass = float(token_2["value"])
							break

				if token["value"] == "MaxMass":
					for token_2 in line_data:
						if token_2["type"] == "value":
							max_mass = float(token_2["value"])
							break

	max_inventory_mass = remove_excess_zeroes(max_mass - mass)

	for line_data in children:
		for token in line_data:
			if token["type"] == "property":
				if token["value"] == "MaxMass":
					token["value"] = "MaxInventoryMass"
					for token_2 in line_data:
						if token_2["type"] == "value":
							token_2["value"] = max_inventory_mass
							return


def remove_excess_zeroes(string):
	return f"{string:g}"


def replace_property_and_value(line_data, old_property, new_property, value_function):
	for token in line_data:
		if token["type"] == "property":
			if token["value"] == old_property:
				token["value"] = new_property
				for token_2 in line_data:
					if token_2["type"] == "value":
						token_2["value"] = value_function(token_2["value"])
						return


def min_throttle_range_to_negative_throttle_multiplier(old_value):
	new_value = abs(1 - abs(float(old_value)))
	return remove_excess_zeroes(new_value)


def max_throttle_range_to_positive_throttle_multiplier(line_data):
	new_value = abs(1 + abs(float(old_value)))
	return remove_excess_zeroes(new_value)


def max_length_to_offsets(children):
	"""
	MaxLength = old_value
	->
	ContractedOffset = Vector
		X = old_value / 2
		Y = 0
	ExtendedOffset = Vector
		X = old_value
		Y = 0
	"""
	for index, line_data in enumerate(children):
		old_value = max_length_to_offsets_2(line_data)

		if old_value != None:
			# print(index, old_value)

			children.insert(index + 1, [
				{
					"type": "property", "value": "ExtendedOffset"
				},
				{
					"type": "value", "value": "Vector"
				},
				{
					"type": "children", "value": [
						[
							{ "type": "property", "value": "X" },
							{ "type": "extra", "value": " "}, {"type": "extra", "value": "="}, {"type": "extra", "value": " "},
							{ "type": "value", "value": remove_excess_zeroes(old_value) }
						],
						[
							{ "type": "property", "value": "Y" },
							{ "type": "extra", "value": " "}, {"type": "extra", "value": "="}, {"type": "extra", "value": " "},
							{ "type": "value", "value": remove_excess_zeroes(0) }
						]
					]
				}
			])



def max_length_to_offsets_2(line_data):
	for token in line_data:
		if token["type"] == "property":
			if token["value"] == "MaxLength":
				token["value"] = "ContractedOffset"
				for token_2 in line_data:
					if token_2["type"] == "value":
						old_value = float(token_2["value"])
						token_2["value"] = "Vector"

						line_data.append( { "type": "children", "value": [
							[
								{ "type": "property", "value": "X" },
								{ "type": "extra", "value": " "}, {"type": "extra", "value": "="}, {"type": "extra", "value": " "},
								{ "type": "value", "value": remove_excess_zeroes(old_value / 2) }
							],
							[
								{ "type": "property", "value": "Y" },
								{ "type": "extra", "value": " "}, {"type": "extra", "value": "="}, {"type": "extra", "value": " "},
								{ "type": "value", "value": remove_excess_zeroes(0) }
							]
						] } )

						return old_value


def duplicate_script_path(parsed_subset):
	pass