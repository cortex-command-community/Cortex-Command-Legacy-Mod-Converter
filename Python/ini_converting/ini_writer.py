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
					get_lines_from_dicts_recursively(section, lines)
				f.write("\n".join(lines))


def get_lines_from_dicts_recursively(line_tokens, lines):
	# This function loops twice through line_tokens so the lines can be appended in the correct order.

	line = ""
	for dictionary in line_tokens:
		if dictionary["type"] != "lines_tokens":
			line += dictionary["content"]
	lines.append(line)

	for dictionary in line_tokens:
		if dictionary["type"] == "lines_tokens":
			for line_tokens in dictionary["content"]:
				get_lines_from_dicts_recursively(line_tokens, lines)