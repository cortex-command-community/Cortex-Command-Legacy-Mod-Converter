import os
from pathlib import Path
from shutil import copyfile

replace_variables_list = {
	"= Sound"    : "= SoundContainer",
	"AddSample =": "AddSound =",
}

manually_replace_variables_list = {
	"Priority =": "// Priority =",
}

# replace_folders_list = {

# }

text_file_extensions = {
	".ini"
}

line_number = 69

with open("output/manually-edit-these-lines.txt", "w") as file_manual:
	for input_folder, input_subfolders, full_filenames in os.walk("input"):
		# print(input_folder, input_subfolders, full_filenames)
		output_folder = os.path.join("output", Path(*Path(input_folder).parts[1:]))
		if input_folder != "input":
			os.makedirs(output_folder)
		for full_filename in full_filenames:
			filename, file_extension = os.path.splitext(full_filename)
			if filename == ".empty":
				continue
			input_file_path  = os.path.join(input_folder , full_filename)
			output_file_path = os.path.join(output_folder, full_filename)
			if file_extension in text_file_extensions:
				with open(input_file_path, "r") as file_in:
					text = file_in.read()
					# replace variables
					for old_str, new_str in replace_variables_list.items():
						text = text.replace(old_str, new_str)
					# replace variables that need to be manually edited afterwards
					for old_str, new_str in manually_replace_variables_list.items():
						text = text.replace(old_str, new_str)
						# TODO: Add file line numbers to this as well.
						file_manual.write("file: {} | line: {} | edit this: {}\n".format(output_file_path, line_number, new_str))
					with open(output_file_path, "w") as file_out:
						file_out.write(text)
			else:
				copyfile(input_file_path, output_file_path)