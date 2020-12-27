import os, sys, time, shutil, math, zipfile, json, pathlib, webbrowser
from pathlib import Path
from jsoncomment import JsonComment
from playsound import playsound

from Python import shared_globals as cfg
from Python import regex_rules
from Python.zips import create_zips
from Python import update_progress


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


# If an exe executes this program then sys is frozen.
output_folder = ".." if getattr(sys, 'frozen', False) else "Output"


def load_conversion_and_warning_rules():
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
	global output_folder, warnings

	time_start = time.time()

	input_folder_path = cfg.sg.user_settings_get_entry("input_folder")
	true_input_folder_path = os.path.join(input_folder_path, os.pardir) # TODO: Better variable name.

	unzip(input_folder_path)

	update_progress.set_max_progress(input_folder_path)
	
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

	update_progress.progress = 0
	update_progress.total_progress = 0
	warnings = []

	elapsed = math.floor(time.time() - time_start)
	if cfg.sg.user_settings_get_entry("play_finish_sound"):
		playsound(resource_path("Media/finish.wav"))
	print("Finished in {} {}".format(elapsed, pluralize("second", elapsed)))


def unzip(input_folder_path):
	for f in os.listdir(input_folder_path):
		zip_path = os.path.join(input_folder_path, f)
		if zipfile.is_zipfile(zip_path):
			with zipfile.ZipFile(zip_path) as item:
				item.extractall(input_folder_path)
			os.remove(zip_path)


def get_mod_subfolder(input_folder_path, input_subfolder_path, true_input_folder_path):
	if input_folder_path.endswith(".rte"):
		return os.path.relpath(input_subfolder_path, true_input_folder_path)
	else:
		return os.path.relpath(input_subfolder_path, input_folder_path)


def try_print_mod_name(mod_subfolder_parts, mod_subfolder):
	if len(mod_subfolder_parts) == 1:
		print("Converting '{}'".format(mod_subfolder))
		update_progress.increment_progress()


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

		if full_filename == "desktop.ini":
			continue

		if file_extension in (".ini", ".lua"):
			create_converted_file(input_file_path, output_file_path, input_folder_path)
		else:
			shutil.copyfile(input_file_path, output_file_path)


def create_converted_file(input_file_path, output_file_path, input_folder_path):
	# try: # TODO: Figure out why this try/except is necessary and why it doesn't check for an error type.
	with open(input_file_path, "r") as file_in:
		with open(output_file_path, "w") as file_out:
			all_lines_list = []
			file_path = os.path.relpath(input_file_path, input_folder_path)

			line_number = 0
			for line in file_in:
				line_number += 1

				if warnings_available:
					regex_rules.playsound_warning(line, file_path, line_number, warnings)

					for old_str, new_str in warning_rules.items():
						if old_str in line:
							print(old_str, new_str)
							warnings.append("'{}' line {}: {} -> {}".format(file_path, line_number, old_str, new_str))

				all_lines_list.append(line)

			all_lines = "".join(all_lines_list)

			for old_str, new_str in conversion_rules.items():
				all_lines = all_lines.replace(old_str, new_str)

			all_lines = regex_rules.regex_replace(all_lines)
			file_out.write(regex_rules.regex_replace_bmps_and_wavs(all_lines))
	# except:
	# 	shutil.copyfile(input_file_path, output_file_path)


def warnings_popup():
	if warnings_available:
		w = max(30, len(max(warnings, key=len)))
		h = min(50, len(warnings)) + 1 # + 1 necessary because popup_scrolled adds an extra line.
		cfg.sg.popup_scrolled("\n".join(warnings), title="Lines needing manual replacing", size=(w, h), button_color=cfg.sg.theme_button_color(), background_color=cfg.sg.theme_background_color())


def pluralize(word, count):
	return word + "s" if count != 1 else word