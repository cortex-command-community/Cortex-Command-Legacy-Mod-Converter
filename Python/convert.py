import os, sys, time, shutil, math, pathlib, webbrowser
from pathlib import Path
from playsound import playsound

from Python import shared_globals as cfg
from Python import regex_rules
from Python import zips as zips_py
from Python import update_progress
from Python import palette
from Python import warnings


foo = "bar"

conversion_rules = {}


# TODO: Move to shared_globals.py
def resource_path(relative_path):
	if hasattr(sys, '_MEIPASS'):
		return os.path.join(sys._MEIPASS, relative_path)
	return os.path.join(os.path.abspath("."), relative_path)


# If an exe executes this program then sys is frozen.
output_folder_path = ".." if getattr(sys, 'frozen', False) else "Output"


def convert():
	global output_folder_path

	print("") # Only prints a newline.

	time_start = time.time()

	input_folder_path = cfg.sg.user_settings_get_entry("input_folder")

	zips_py.unzip(input_folder_path)

	update_progress.set_max_progress(input_folder_path)
	
	for input_subfolder_path, input_subfolders, input_subfiles in os.walk(input_folder_path):
		mod_subfolder = get_mod_subfolder(input_folder_path, input_subfolder_path)

		mod_subfolder_parts = pathlib.Path(mod_subfolder).parts

		if len(mod_subfolder_parts) > 0 and mod_subfolder_parts[0].endswith(".rte"):
			try_print_mod_name(mod_subfolder_parts, mod_subfolder)
			output_subfolder = os.path.join(output_folder_path, mod_subfolder)
			create_folder(input_subfolder_path, output_subfolder)
			process_files(input_subfiles, input_subfolder_path, output_subfolder, input_folder_path, output_folder_path)

	if cfg.sg.user_settings_get_entry("output_zips"):
		zips_py.create_zips(input_folder_path, output_folder_path)

	elapsed = math.floor(time.time() - time_start)

	update_progress.increment_progress() # TODO: This is a temporary solution for zipping not being accounted in the progress.

	if cfg.sg.user_settings_get_entry("play_finish_sound"):
		playsound(resource_path("Media/finish.wav"), block=False)
	print("Finished in {} {}".format(elapsed, pluralize("second", elapsed)))

	if len(warnings.warning_results) > 0:
		warnings.warnings_popup()

	warnings.warning_results = []


def get_mod_subfolder(input_folder_path, input_subfolder_path):
	if input_folder_path.endswith(".rte"):
		return os.path.relpath(input_subfolder_path, os.path.join(input_folder_path, os.pardir))
	else:
		return os.path.relpath(input_subfolder_path, input_folder_path)


def try_print_mod_name(mod_subfolder_parts, mod_subfolder):
	if len(mod_subfolder_parts) == 1:
		print("Converting '{}'".format(mod_subfolder))


def create_folder(input_subfolder_path, output_subfolder):
	try:
		os.makedirs(output_subfolder)
	except FileExistsError:
		pass


def process_files(input_subfiles, input_subfolder_path, output_subfolder, input_folder_path, output_folder_path):
	for full_filename in input_subfiles:
		filename, file_extension = os.path.splitext(full_filename)

		input_file_path = os.path.join(input_subfolder_path, full_filename)

		output_file_path = os.path.join(output_subfolder, full_filename)

		if palette.is_input_image(full_filename):
			palette.process_image(full_filename, input_file_path, output_file_path)

		if full_filename == "desktop.ini":
			continue

		if file_extension in (".ini", ".lua"):
			create_converted_file(input_file_path, output_file_path, input_folder_path)
		else:
			if not palette.is_input_image(full_filename):
				shutil.copyfile(input_file_path, output_file_path)

		update_progress.increment_progress()

def create_converted_file(input_file_path, output_file_path, input_folder_path):
	# try: # TODO: Figure out why this try/except is necessary and why it doesn't check for an error type.
	with open(input_file_path, "r") as file_in:
		with open(output_file_path, "w") as file_out:
			all_lines_list = []
			file_path = os.path.relpath(input_file_path, input_folder_path)

			line_number = 0
			for line in file_in:
				line_number += 1

				if ".bmp" in line:
					if not any(keep_bmp in line for keep_bmp in ["palette.bmp", "palettemat.bmp"]):
						line = line.replace(".bmp", ".png")

				if warnings.warnings_available:
					regex_rules.playsound_warning(line, file_path, line_number)

					for old_str, new_str in warnings.warning_rules.items():
						if old_str in line:
							warnings.warning_results.append("'{}' line {}: {} -> {}".format(file_path, line_number, old_str, new_str))

				all_lines_list.append(line)

			all_lines = "".join(all_lines_list)

			# Conversion rules can contain newlines, so they can't be applied per-line.
			# Splitting the extension means it's fine that bmp -> png already happened.
			for old_str, new_str in conversion_rules.items():
				old_str_base = os.path.splitext(old_str)[0]
				new_str_base = os.path.splitext(new_str)[0]
				all_lines = all_lines.replace(old_str_base, new_str_base)

			all_lines = regex_rules.regex_replace(all_lines)
			file_out.write(regex_rules.regex_replace_wavs(all_lines))
	# except:
	# 	shutil.copyfile(input_file_path, output_file_path)


def pluralize(word, count):
	return word + "s" if count != 1 else word