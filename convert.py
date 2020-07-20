import os

replace_variables_list = {
	"= Sound"    : "= SoundContainer", # ReloadEndSound *= Sound* -> ReloadEndSound *= SoundContainer*
	"= AddSample": "= AddSound",
}

replace_folders_list = {

}

def replace_variables(line):
	for old_str, new_str in replace_variables_list.items():
		line = line.replace(old_str, new_str)
	return line

path = "mario-b33-manual-conversion.rte\Mario.rte\Items\Feather\Feather.ini"
input_path = os.path.join("input", path)
output_path = os.path.join("output", path)

with open(input_path, "r") as file_in:
	text = file_in.read()
	text = replace_variables(text)

	folder_path = os.path.dirname(output_path)
	print(folder_path)
	os.makedirs(folder_path)

	with open(output_path, "w") as file_out:
		file_out.write(text)