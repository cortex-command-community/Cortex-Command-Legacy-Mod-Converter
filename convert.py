import os, time, pathlib, shutil, math, re

from conversion_rules import conversion_rules


def get_output_folder_path(input_folder_path):
	return os.path.join("output", pathlib.Path(*pathlib.Path(input_folder_path).parts[1:]))


def try_print_mod_name(input_folder_path):
	input_folder_path_tuple = pathlib.Path(input_folder_path).parts
	
	if len(input_folder_path_tuple) == 2:
		print("Converting '{}'".format(input_folder_path_tuple[1]))


def create_folder(input_folder_path, output_folder):
	# Prevents putting the "input" folder itself into the "output" folder,
	# while copying the rest of the folder structure inside of "inputs" to "outputs".
	if input_folder_path != "input":
		os.makedirs(output_folder)


def create_converted_file(input_file_path, output_file_path):
	with open(input_file_path, "r") as file_in:
		with open(output_file_path, "w") as file_out:
			all_lines = do_complex_replacements(file_in.read())
			for old_str, new_str in conversion_rules.items():
				all_lines = all_lines.replace(old_str, new_str)
			file_out.write(all_lines)


def process_file(full_filename_list, input_folder_path, output_folder):
	for full_filename in full_filename_list:
		filename, file_extension = os.path.splitext(full_filename)

		# The ".empty" file exists so otherwise empty folders can be added to Git.
		if filename == ".empty":
			continue

		input_file_path  = os.path.join(input_folder_path, full_filename)
		output_file_path = os.path.join(output_folder, full_filename)

		if file_extension in ('.ini', '.lua'):
			create_converted_file(input_file_path, output_file_path)
		else:
			shutil.copyfile(input_file_path, output_file_path)


def do_complex_replacements(all_lines):
	# TODO:
	# AudioMan:PlaySound("ModName.rte/Folder/SoundName.wav", SceneMan:TargetDistanceScalar(self.Pos), false, true, -1)
	# to
	# AudioMan:PlaySound("ModName.rte/Folder/SoundName.wav", self.Pos)	-- Cut everything and leave the thing inside the brackets after SceneMan:TargetDistanceScalar

	# TODO: MOPixel vs MOSParticle can be found with Regexing part after MO till first \n.
	particle_number_to_add_variants = {
		'ParticleNumberToAdd = (.*?)\n\tAddParticles = MOPixel\n\t\tCopyOf = (.*?)\n': 'AddGib = Gib\n\t\tGibParticle = MOPixel\n\t\t\tCopyOf = {}\n\t\tCount = {}\n',
		'ParticleNumberToAdd = (.*?)\n\tAddParticles = MOSParticle\n\t\tCopyOf = (.*?)\n': 'AddGib = Gib\n\t\tGibParticle = MOSParticle\n\t\t\tCopyOf = {}\n\t\tCount = {}\n',
	}

	for searched, replaced in particle_number_to_add_variants.items():
		moved_values = re.findall(searched, all_lines) # Returns list of tuples, with each tuple containing two values.
		
		if len(moved_values) > 0:
			# TODO: Use two .append() calls or one .extend() call instead, for readability.

			# Combines list of tuples into a single tuple.
			moved_values_tuple = ()
			for value_pair in moved_values:
				# Switches values in tuple around.
				moved_values_tuple += (value_pair[1], value_pair[0])
			
			all_lines = re.sub(searched, replaced, all_lines).format(*moved_values_tuple)
	
	return all_lines


def pluralize(word, count):
	return word + "s" if count != 1 else word


def main():
	time_start = time.time()

	for input_folder_path, input_subfolders, full_filename_list in os.walk("input"):
		output_folder = get_output_folder_path(input_folder_path)

		try_print_mod_name(input_folder_path)
		create_folder(input_folder_path, output_folder)
		process_file(full_filename_list, input_folder_path, output_folder)

	elapsed = math.floor(time.time() - time_start)
	print("Finished in {} {}".format(elapsed, pluralize("second", elapsed)))


if __name__ == "__main__":
    main()