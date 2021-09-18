import pprint, math


"""
The initial parsed_subset structure passed to the apply_rules function:
{
	foo.rte: {
		FolderName {
			Bar.ini: [
				{
					value: [
						{
							value: [
								{
									value: ""
								}
							]
						}
					]
				}
			]	
		}
	}
}
"""


def apply_rules(parsed_subset):
	# print(pprint.pprint(parsed_subset))
	# print(repr(parsed_subset))
	for key, value in parsed_subset.items():
		if isinstance(value, dict):
			apply_rules(value)
		else: # If it's a list of lines in the form of dictionaries.
			for section_dictionary in value:
				if "value" in section_dictionary:
					section_properties_list = section_dictionary["value"]

					# TODO: Replace with contains_shallowly(section_properties_list, ("Mass", "MaxMass"))
					if contains_shallowly(section_properties_list, "Mass") and contains_shallowly(section_properties_list, "MaxMass"):
						max_mass_to_max_inventory_mass(section_properties_list)
						# print(pprint.pprint(parsed_subset))
			# print(type(value), value, "\n")
			# if contains(value, "Mass"):
			# print('bar')
			# max_mass_to_max_inventory_mass(value)


def contains_shallowly(section_properties_list, checked):
	"""
	This function deliberately doesn't check the section's contents recursively.
	"""
	return any((checked in line_dictionary.values() for line_dictionary in section_properties_list))


# def contains_recursively(section_dictionary, checked):
# 	for line_dictionary in section_dictionary:
# 		subvalue = line_dictionary["value"]
# 		if "value" in line_dictionary and isinstance(subvalue, list):
# 			contains(subvalue)
# 		else:
# 			subproperty = line_dictionary["property"]
# 			if subproperty == "Mass":
# 				print('foo')


def max_mass_to_max_inventory_mass(section_properties_list):
	"""
	MaxInventoryMass = MaxMass - Mass
	"""
	# print(section_properties_list)
	# TODO: Move this in read_properties()
	for line_dictionary in section_properties_list:
		if "property" in line_dictionary and "value" in line_dictionary:
			prop = line_dictionary["property"]
			value = line_dictionary["value"]

			if prop == "Mass":
				mass = float(value)
			elif prop == "MaxMass":
				max_mass = float(value)

	# TODO: Move this in write_properties()
	for line_dictionary in section_properties_list:
		if "property" in line_dictionary and "value" in line_dictionary:
			prop = line_dictionary["property"]
			value = line_dictionary["value"]

			# print(prop)
			if prop == "MaxMass":
				line_dictionary["property"] = "MaxInventoryMass"

				max_inventory_mass = f"{(max_mass - mass):g}" # :g removes excess zeros.
				# print(max_inventory_mass)
				line_dictionary["value"] = max_inventory_mass

# 	for line_dictionary in value:
# 		subvalue = line_dictionary["value"]
# 		if "value" in line_dictionary and isinstance(subvalue, list):
# 			max_mass_to_max_inventory_mass(subvalue)
# 		else:
# 			subproperty = line_dictionary["property"]
# 			if subproperty == "Mass":
# 				print('foo')


def duplicate_script_path(parsed_subset):
	pass