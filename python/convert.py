import os, time, shutil, math, re, sys, shutil, zipfile, json, pathlib
from pathlib import Path
from jsoncomment import JsonComment
from playsound import playsound

from Python import shared_globals as cfg


progress = 0
total_progress = 0
conversion_rules = {}


# TODO: Move to shared_globals.py
def resource_path(relative_path):
	if hasattr(sys, '_MEIPASS'):
		return os.path.join(sys._MEIPASS, relative_path)
	return os.path.join(os.path.abspath("."), relative_path)


finishSoundPath = resource_path("Media/finish.wav")


# If an exe executes this program then sys is frozen.
output_folder = ".." if getattr(sys, 'frozen', False) else "Output"


def	load_conversion_rules():
	json_parser = JsonComment(json)

	for name in os.listdir(resource_path("ConversionRules")):
		if name.endswith(".json"):
			path = os.path.join(resource_path("ConversionRules"), name)
			with open(path) as f:
				conversion_rules.update(json_parser.load(f))

load_conversion_rules()


def convert():
	global progress, total_progress, output_folder

	time_start = time.time()

	input_folder = cfg.sg.user_settings_get_entry("input_folder")

	unzip(input_folder)

	total_progress = get_total_progress(input_folder)
	
	for input_folder_path, input_subfolders, full_filename_list in os.walk(input_folder):
		mod_subfolder = get_mod_subfolder(input_folder, input_folder_path)
		output_subfolder = os.path.join(output_folder, mod_subfolder)

		try_print_mod_name(mod_subfolder)
		create_folder(input_folder_path, output_subfolder)
		process_file(full_filename_list, input_folder_path, output_subfolder)

	if cfg.sg.user_settings_get_entry("output_zips"):
		create_zips(input_folder, output_folder)

	progress = 0
	total_progress = 0

	elapsed = math.floor(time.time() - time_start)
	if cfg.sg.user_settings_get_entry("play_finish_sound"):
		playsound(finishSoundPath)
	print("Finished in {} {}".format(elapsed, pluralize("second", elapsed)))


def unzip(input_folder):
	for f in os.listdir(input_folder):
		zip_path = os.path.join(input_folder, f)
		if zipfile.is_zipfile(zip_path):
			with zipfile.ZipFile(zip_path) as item:
				item.extractall(input_folder)
			os.remove(zip_path)


def get_total_progress(input_folder):
	if input_folder.endswith(".rte"):
		mod_count = 1
	else:
		mod_count = len([name for name in os.listdir(input_folder) if os.path.isdir(os.path.join(input_folder, name))])
	
	return mod_count * 2 if cfg.sg.user_settings_get_entry("output_zips") else mod_count


def get_mod_subfolder(input_folder, input_folder_path):
	if input_folder.endswith(".rte"):
		return os.path.relpath(input_folder_path, os.path.join(input_folder, os.pardir))
	else:
		return os.path.relpath(input_folder_path, input_folder)


def try_print_mod_name(mod_subfolder):
	input_folder_path_tuple = pathlib.Path(mod_subfolder).parts

	if len(input_folder_path_tuple) == 1:
		print("Converting '{}'".format(input_folder_path_tuple[0]))
		update_progress()


def update_progress():
	global progress, total_progress
	progress += 1
	cfg.progress_bar.UpdateBar(progress % total_progress, total_progress)


def create_folder(input_folder_path, output_subfolder):
	# Prevents putting the input_folder itself into the output_subfolder.
	# if input_folder_path != cfg.sg.user_settings_get_entry("input_folder"):

	try:
		os.makedirs(output_subfolder)
	except FileExistsError:
		pass


def process_file(full_filename_list, input_folder_path, output_subfolder):
	for full_filename in full_filename_list:
		filename, file_extension = os.path.splitext(full_filename)

		# The ".empty" file exists so otherwise empty folders can be added to Git.
		if filename == ".empty":
			continue

		input_file_path  = os.path.join(input_folder_path, full_filename)
		output_file_path = os.path.join(output_subfolder, full_filename)

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


def create_zips(input_folder, output_folder):
	if input_folder.endswith(".rte"):
		create_single_zip(Path(input_folder).name, output_folder)
	else:
		# TODO: Move check if it's a directory out of this loop. 
		folder_names = [f for f in os.listdir(cfg.sg.user_settings_get_entry("input_folder")) if os.path.isdir(os.path.join(output_folder, f))]
		for mod_name in folder_names:
			create_single_zip(mod_name, output_folder)


def create_single_zip(mod_name, output_folder):
	print("Zipping '{}'".format(mod_name))
	folder_path = os.path.join(output_folder, mod_name)
	shutil.make_archive(folder_path, "zip", root_dir=output_folder, base_dir=mod_name)
	shutil.rmtree(folder_path)
	update_progress()


def pluralize(word, count):
	return word + "s" if count != 1 else word