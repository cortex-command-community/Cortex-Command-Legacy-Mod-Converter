import os, time, pathlib, shutil, math, re, sys, shutil, winsound, zipfile
import config

from conversion_rules import conversion_rules


def main():
	time_start = time.time()

	unzip()

	for input_folder_path, input_subfolders, full_filename_list in os.walk("input"):
		output_folder = get_output_folder_path(input_folder_path)

		try_print_mod_name(input_folder_path)
		create_folder(input_folder_path, output_folder)
		process_file(full_filename_list, input_folder_path, output_folder)

	if config.output_zips:
		create_zips()

	elapsed = math.floor(time.time() - time_start)
	if config.play_finish_sound:
		winsound.MessageBeep()
	print("Finished in {} {}".format(elapsed, pluralize("second", elapsed)))


def unzip():
	for f in os.listdir("input"):
		zip_path = os.path.join("input/", f)
		if zipfile.is_zipfile(zip_path):
			with zipfile.ZipFile(zip_path) as item:
				item.extractall("input")
			os.remove(zip_path)


def get_output_folder_path(input_folder_path):
	return os.path.join(config.output_path, pathlib.Path(*pathlib.Path(input_folder_path).parts[1:]))


def try_print_mod_name(input_folder_path):
	input_folder_path_tuple = pathlib.Path(input_folder_path).parts
	
	if len(input_folder_path_tuple) == 2:
		print("Converting '{}'".format(input_folder_path_tuple[1]))


def create_folder(input_folder_path, output_folder):
	# Prevents putting the "input" folder itself into the config.output_path folder.
	if input_folder_path != "input":
		try:
			os.makedirs(output_folder)
		except FileExistsError:
			pass


def process_file(full_filename_list, input_folder_path, output_folder):
	for full_filename in full_filename_list:
		filename, file_extension = os.path.splitext(full_filename)

		# The ".empty" file exists so otherwise empty folders can be added to Git.
		if filename == ".empty":
			continue

		input_file_path  = os.path.join(input_folder_path, full_filename)
		output_file_path = os.path.join(output_folder, full_filename)

		if file_extension in (".ini", ".lua"):
			create_converted_file(input_file_path, output_file_path)
		else:
			shutil.copyfile(input_file_path, output_file_path)


def create_converted_file(input_file_path, output_file_path):
	try:
		with open(input_file_path, "r") as file_in:
			with open(output_file_path, "w") as file_out:
				all_lines = regex_replace(file_in.read())
				for old_str, new_str in conversion_rules.items():
					all_lines = all_lines.replace(old_str, new_str)
				all_lines = regex_replace_bmps_and_wavs(all_lines)
				file_out.write(all_lines)
	except:
		shutil.copyfile(input_file_path, output_file_path)


def regex_replace(all_lines):
	all_lines = simple_replace(all_lines, "Framerate = (.*)", "SpriteAnimMode = 7")
	all_lines = simple_replace(all_lines, "\tPlayerCount = (.*)\n", "")
	all_lines = simple_replace(all_lines, "\tTeamCount = (.*)\n", "")

	all_lines = specific_replace(all_lines, regex_replace_particle, False, "ParticleNumberToAdd = (.*)\n\tAddParticles = (.*)\n\t\tCopyOf = (.*)\n", "AddGib = Gib\n\t\tGibParticle = {}\n\t\t\tCopyOf = {}\n\t\tCount = {}\n")
	all_lines = specific_replace(all_lines, regex_replace_sound_priority, True, " Sound(((?! Sound).)*)Priority", " Sound{}// Priority")
	all_lines = specific_replace(all_lines, regex_use_capture, False, "FundsOfTeam(.*) =", "Team{}Funds =")
	# all_lines = specific_replace(all_lines, regex_replace_playsound, False, "", "")

	return all_lines


def simple_replace(all_lines, pattern, replacement):
	matches = re.findall(pattern, all_lines)
	if len(matches) > 0:
		return re.sub(pattern, replacement, all_lines)
	return all_lines


def specific_replace(all_lines, fn, dotall, pattern, replacement):
	# TODO: Refactor so .findall can take dotall as an argument directly.
	if dotall:
		matches = re.findall(pattern, all_lines, re.DOTALL)
	else:
		matches = re.findall(pattern, all_lines)
	if len(matches) > 0:
		return fn(all_lines, pattern, replacement, matches)
	return all_lines


def regex_replace_particle(all_lines, pattern, replacement, matches):
	# matches == [(4, "foo", "bar"), (2, "baz", "bee")]
	new = [item for tup in matches for item in tup]
	# new == [4, "foo", "bar", 2, "baz", "bee"]

	# 0, 1, 2 -> 1, 2, 0
	new[0::3], new[1::3], new[2::3] = \
	new[1::3], new[2::3], new[0::3]
	
	# new == ["foo", "bar", 4, "baz", "bee", 2]
	return re.sub(pattern, replacement, all_lines).format(*new)


def regex_replace_sound_priority(all_lines, pattern, replacement, matches):
	# TODO: This pattern returns two items in each tuple, while we only need the first. Create a better pattern.
	# https://stackoverflow.com/a/406408/13279557
	# https://regex101.com/r/NdKaWs/2

	# matches == [(4, "foo"), (2, "bar")]
	new = [item for tup in matches for item in tup][::2]
	# new == [4, 2]
	return re.sub(pattern, replacement, all_lines, flags=re.DOTALL).format(*new)


def regex_use_capture(all_lines, pattern, replacement, matches):
	return re.sub(pattern, replacement, all_lines).format(*matches)


# def regex_replace_playsound(all_lines, pattern, replacement, matches):
# 	return all_lines
# 	# TODO:
# 	# AudioMan:PlaySound("ModName.rte/Folder/SoundName.wav", SceneMan:TargetDistanceScalar(self.Pos), false, true, -1)
# 	# to
#	# AudioMan:PlaySound("ModName.rte/Folder/SoundName.wav", self.Pos)	-- Cut everything and leave the thing inside the brackets after SceneMan:TargetDistanceScalar


def regex_replace_bmps_and_wavs(all_lines):
	all_lines = specific_replace(all_lines, regex_use_capture, False, "Base\.rte(.*?)\.bmp", "Base.rte{}.png")
	all_lines = specific_replace(all_lines, regex_use_capture, False, "base\.rte(.*?)\.bmp", "Base.rte{}.png")
	all_lines = specific_replace(all_lines, regex_use_capture, False, "Base\.rte(.*?)\.wav", "Base.rte{}.flac")
	all_lines = specific_replace(all_lines, regex_use_capture, False, "base\.rte(.*?)\.wav", "Base.rte{}.flac")
	return all_lines


def create_zips():
	# Get mod folder names from the input folder.
	folder_names = [f for f in os.listdir("input") if os.path.isdir(os.path.join(config.output_path, f))]

	for f in folder_names:
		print("Zipping '{}'".format(f))
		folder_path = os.path.join(config.output_path, f)
		shutil.make_archive(folder_path, "zip", root_dir=config.output_path, base_dir=f)
		shutil.rmtree(folder_path)


def pluralize(word, count):
	return word + "s" if count != 1 else word


if __name__ == "__main__":
    main()