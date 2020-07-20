import os
import pathlib
import shutil

replace_variables_list = {
	"= Sound"    : "= SoundContainer", # ReloadEndSound *= Sound* -> ReloadEndSound *= SoundContainer*
	"= AddSample": "= AddSound",
}

replace_folders_list = {

}

text_file_extensions = {
	".ini"
}

def replace_variables(line):
	for old_str, new_str in replace_variables_list.items():
		line = line.replace(old_str, new_str)
	return line

for input_folder, input_subfolders, full_filenames in os.walk("input"):
	# print(input_folder, input_subfolders, full_filenames)
	output_folder = os.path.join("output", pathlib.Path(*pathlib.Path(input_folder).parts[1:]))
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
				text = replace_variables(text)
				with open(output_file_path, "w") as file_out:
					file_out.write(text)
		else:
			shutil.copyfile(input_file_path, output_file_path)

dir_name = "output/mario-b33-manual-conversion.rte"
shutil.make_archive(dir_name, "zip", dir_name)

shutil.rmtree(dir_name)