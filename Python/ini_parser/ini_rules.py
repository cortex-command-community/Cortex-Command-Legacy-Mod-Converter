import pprint, math


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
				# 	min_throttle_range_to_negative_throttle_multiplier(line_data)
				# 	max_throttle_range_to_positive_throttle_multiplier(line_data)


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


def min_throttle_range_to_negative_throttle_multiplier(line_data):
	""" NegativeThrottleMultiplier = 1 - abs(MinThrottleRange) """
	for token in line_data:
		if token["type"] == "property":
			if token["value"] == "MinThrottleRange":
				token["value"] = "NegativeThrottleMultiplier"
				for token_2 in line_data:
					if token_2["type"] == "value":
						new_value = 1 - abs(float(token_2["value"]))
						token_2["value"] = remove_excess_zeroes(new_value)
						return


def max_throttle_range_to_positive_throttle_multiplier(line_data):
	""" PositiveThrottleMultiplier = 1 + abs(MaxThrottleRange) """
	for token in line_data:
		if token["type"] == "property":
			if token["value"] == "MaxThrottleRange":
				token["value"] = "PositiveThrottleMultiplier"
				for token_2 in line_data:
					if token_2["type"] == "value":
						new_value = 1 + abs(float(token_2["value"]))
						token_2["value"] = remove_excess_zeroes(new_value)
						return


def duplicate_script_path(parsed_subset):
	pass