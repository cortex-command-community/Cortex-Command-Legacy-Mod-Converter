import os, time, shutil, math, re, sys, shutil, zipfile, json, pathlib, webbrowser
from pathlib import Path
from jsoncomment import JsonComment
from playsound import playsound

from Python import shared_globals as cfg

progress = 0
total_progress = 0

warnings_file_name = "Warnings.json"
warnings_path = os.path.join("ConversionRules", warnings_file_name)
warnings_available = os.path.isfile(warnings_path)

conversion_rules = {}
warning_rules = {}
warnings = []


# TODO: Move to shared_globals.py
def resource_path(relative_path):
	if hasattr(sys, '_MEIPASS'):
		return os.path.join(sys._MEIPASS, relative_path)
	return os.path.join(os.path.abspath("."), relative_path)


finishSoundPath = resource_path("Media/finish.wav")


# If an exe executes this program then sys is frozen.
output_folder = ".." if getattr(sys, 'frozen', False) else "Output"


def	load_conversion_and_warning_rules():
	json_parser = JsonComment(json)

	json_files_found = 0
	try:
		for name in os.listdir("ConversionRules"):
			if name.endswith(".json") and name != warnings_file_name:
				json_files_found += 1
				with open(os.path.join("ConversionRules", name)) as f:
					conversion_rules.update(json_parser.load(f)) 
		if warnings_available:
			with open(warnings_path) as f:
				warning_rules.update(json_parser.load(f))
	except:
		check_github_button_clicked_and_exit(cfg.sg.Popup("The 'ConversionRules' folder wasn't found next to this executable. You can get the missing folder from the Legacy Mod Converter GitHub repo.", title="Missing ConversionRules folder", custom_text="Go to GitHub"))

	if json_files_found == 0:
		check_github_button_clicked_and_exit(cfg.sg.Popup("The 'ConversionRules' folder didn't contain any JSON files. You can get the JSON files from the Legacy Mod Converter GitHub repo.", title="Missing JSON files", custom_text="Go to GitHub"))



def check_github_button_clicked_and_exit(clicked_github_button):
	if clicked_github_button:
		webbrowser.open("https://github.com/cortex-command-community/Cortex-Command-Legacy-Mod-Converter")
	sys.exit()


def convert():
	global progress, total_progress, output_folder, warnings

	time_start = time.time()

	input_folder_path = cfg.sg.user_settings_get_entry("input_folder")
	true_input_folder_path = os.path.join(input_folder_path, os.pardir) # TODO: Better variable name.

	unzip(input_folder_path)

	total_progress = get_total_progress(input_folder_path)
	
	for input_subfolder_path, input_subfolders, input_subfiles in os.walk(input_folder_path):
		mod_subfolder = get_mod_subfolder(input_folder_path, input_subfolder_path, true_input_folder_path)

		mod_subfolder_parts = pathlib.Path(mod_subfolder).parts
		if len(mod_subfolder_parts) > 0 and mod_subfolder_parts[0].endswith(".rte"):
			output_subfolder = os.path.join(output_folder, mod_subfolder)
			try_print_mod_name(mod_subfolder_parts, mod_subfolder)
			create_folder(input_subfolder_path, output_subfolder)
			process_files(input_subfiles, input_subfolder_path, output_subfolder, input_folder_path)

	if cfg.sg.user_settings_get_entry("output_zips"):
		create_zips(input_folder_path, output_folder)

	if len(warnings) > 0:
		warnings_popup()

	progress = 0
	total_progress = 0
	warnings = []

	elapsed = math.floor(time.time() - time_start)
	if cfg.sg.user_settings_get_entry("play_finish_sound"):
		playsound(finishSoundPath)
	print("Finished in {} {}".format(elapsed, pluralize("second", elapsed)))


def unzip(input_folder_path):
	for f in os.listdir(input_folder_path):
		zip_path = os.path.join(input_folder_path, f)
		if zipfile.is_zipfile(zip_path):
			with zipfile.ZipFile(zip_path) as item:
				item.extractall(input_folder_path)
			os.remove(zip_path)


def get_total_progress(input_folder_path):
	if input_folder_path.endswith(".rte"):
		mod_count = 1
	else:
		mod_count = 0
		for mod_name in os.listdir(input_folder_path):
			if os.path.isdir(os.path.join(input_folder_path, mod_name)) and mod_name.endswith(".rte"):
				mod_count += 1
	return mod_count * 2 if cfg.sg.user_settings_get_entry("output_zips") else mod_count


def get_mod_subfolder(input_folder_path, input_subfolder_path, true_input_folder_path):
	if input_folder_path.endswith(".rte"):
		return os.path.relpath(input_subfolder_path, true_input_folder_path)
	else:
		return os.path.relpath(input_subfolder_path, input_folder_path)


def try_print_mod_name(mod_subfolder_parts, mod_subfolder):
	if len(mod_subfolder_parts) == 1:
		print("Converting '{}'".format(mod_subfolder))
		update_progress()


def update_progress():
	global progress
	progress += 1
	cfg.progress_bar.UpdateBar(progress % total_progress, total_progress)


def create_folder(input_subfolder_path, output_subfolder):
	try:
		os.makedirs(output_subfolder)
	except FileExistsError:
		pass


def process_files(input_subfiles, input_subfolder_path, output_subfolder, input_folder_path):
	for full_filename in input_subfiles:
		filename, file_extension = os.path.splitext(full_filename)

		input_file_path  = os.path.join(input_subfolder_path, full_filename)
		output_file_path = os.path.join(output_subfolder, full_filename)

		if file_extension in (".ini", ".lua"):
			create_converted_file(input_file_path, output_file_path, input_folder_path)
		else:
			shutil.copyfile(input_file_path, output_file_path)


def create_converted_file(input_file_path, output_file_path, input_folder_path):
	try:
		with open(input_file_path, "r") as file_in:
			with open(output_file_path, "w") as file_out:
				all_lines_list = []
				file_path = os.path.relpath(input_file_path, input_folder_path)

				line_number = 0
				for line in file_in:
					line_number += 1

					if warnings_available:
						for old_str, new_str in warning_rules.items():
							if old_str in line:
								warnings.append("'{}' line {}: {} -> {}".format(file_path, line_number, old_str, new_str))

					all_lines_list.append(line)

				all_lines = "".join(all_lines_list)

				for old_str, new_str in conversion_rules.items():
					all_lines = all_lines.replace(old_str, new_str)

				all_lines = regex_replace(all_lines)
				file_out.write(regex_replace_bmps_and_wavs(all_lines))
	except:
		shutil.copyfile(input_file_path, output_file_path)


def regex_replace(all_lines):
	all_lines = simple_replace(all_lines, "Framerate = (.*)", "SpriteAnimMode = 7")
	all_lines = simple_replace(all_lines, "\tPlayerCount = (.*)\n", "")
	all_lines = simple_replace(all_lines, "\tTeamCount = (.*)\n", "")

	all_lines = specific_replace(all_lines, regex_replace_particle, False, "ParticleNumberToAdd = (.*)\n\tAddParticles = (.*)\n\t\tCopyOf = (.*)\n", "AddGib = Gib\n\t\tGibParticle = {}\n\t\t\tCopyOf = {}\n\t\tCount = {}\n")
	
	all_lines = specific_replace(all_lines, regex_replace_sound_priority, True, "SoundContainer(((?!SoundContainer).)*)Priority", "SoundContainer{}// Priority")

	# all_lines = specific_replace(all_lines, regex_replace_sound_priority, True, "AddSound(((?! AddSound).)*)Priority", "AddSound{}// Priority")
	
	all_lines = specific_replace(all_lines, regex_use_capture, False, "FundsOfTeam(.*) =", "Team{}Funds =")
	# all_lines = specific_replace(all_lines, regex_replace_playsound, False, "", "")

	return all_lines


def simple_replace(all_lines, pattern, replacement):
	matches = re.findall(pattern, all_lines)
	if len(matches) > 0:
		return re.sub(pattern, replacement, all_lines)
	return all_lines


def specific_replace(all_lines, fn, dotall, pattern, replacement):
	# TODO: Refactor so .findall takes re.DOTALL as an argument directly.
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
	# TODO: Combine these four patterns into two.
	all_lines = specific_replace(all_lines, regex_use_capture, False, "Base\.rte(.*?)\.bmp", "Base.rte{}.png")
	all_lines = specific_replace(all_lines, regex_use_capture, False, "base\.rte(.*?)\.bmp", "Base.rte{}.png")
	all_lines = specific_replace(all_lines, regex_use_capture, False, "Base\.rte(.*?)\.wav", "Base.rte{}.flac")
	all_lines = specific_replace(all_lines, regex_use_capture, False, "base\.rte(.*?)\.wav", "Base.rte{}.flac")
	return all_lines


def create_zips(input_folder_path, output_folder):
	if input_folder_path.endswith(".rte"):
		create_single_zip(Path(input_folder_path).name, output_folder)
	else:
		# TODO: Move check if it's a directory out of this loop. 
		folder_names = [f for f in os.listdir(input_folder_path) if os.path.isdir(os.path.join(output_folder, f))]
		for mod_name in folder_names:
			if mod_name.endswith(".rte"):
				create_single_zip(mod_name, output_folder)


def create_single_zip(mod_name, output_folder):
	print("Zipping '{}'".format(mod_name))
	mod_path = os.path.join(output_folder, mod_name)
	shutil.make_archive(mod_path.replace(".rte", "") + "-v1.0" + ".rte", "zip", root_dir=output_folder, base_dir=mod_name)
	shutil.rmtree(mod_path)
	update_progress()


def warnings_popup():
	if warnings_available:
		w = max(30, len(max(warnings, key=len)))
		h = min(50, len(warnings)) + 1 # + 1 necessary because popup_scrolled adds an extra line.
		cfg.sg.popup_scrolled("\n".join(warnings), title="Lines needing manual replacing", size=(w, h), button_color=cfg.sg.theme_button_color(), background_color=cfg.sg.theme_background_color())


def pluralize(word, count):
	return word + "s" if count != 1 else word