def write_converted_ini_recursively(parsed_portion, output_folder_path):
	# pprint.pprint(parsed_portion)
	for name, dict_or_list in parsed_portion.items():
		if isinstance(dict_or_list, dict): # If dict_or_list contains a dictionary of more filenames.
			write_converted_ini_recursively(dict_or_list, output_folder_path / name)
		else: # If dict_or_list contains a list of the sections of a file.
			# pprint.pprint(dict_or_list)
			with open(str(output_folder_path / name), mode="w") as f:
				lines = []
				for section in dict_or_list:
					get_lines_from_dicts_recursively(section, lines, 0)
				f.write("\n".join(lines))


def get_lines_from_dicts_recursively(line_data, lines, depth_tab_count):
	# This function loops twice through line_data so the lines can be appended in the correct order.

	line = depth_tab_count * "\t"
	for dictionary in line_data:
		if dictionary["type"] != "children":
			line += dictionary["value"]
	lines.append(line)

	for dictionary in line_data:
		if dictionary["type"] == "children":
			for line_data in dictionary["value"]:
				get_lines_from_dicts_recursively(line_data, lines, depth_tab_count+1)