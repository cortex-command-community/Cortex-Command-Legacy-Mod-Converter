import os, time, shutil, math, platform
from pathlib import Path
from playsound import playsound
import PySimpleGUI as sg

from Python import shared_globals as cfg
from Python import regex_rules, zips, update_progress, bmp_to_png, warnings, utils, stylua

from Python.case_check import case_check

from Python.ini_converting import ini_cst_builder, ini_rules, ini_writer

# from Python.lua_converting import lua_parser


conversion_rules = {} # TODO: Move this.


def convert_all():
	time_start = time.time()

	print("") # Newline.

	input_folder_path = "Input"
	output_folder_path = "Output"

	update_progress.set_max_progress(input_folder_path)

	for input_mod_path in get_input_mod_paths(input_folder_path):
		convert(
			input_mod_path,
			input_folder_path,
			output_folder_path,
			sg.user_settings_get_entry("beautify_lua"),
			sg.user_settings_get_entry("output_zips"),
			sg.user_settings_get_entry("skip_conversion"),
		)

	if sg.user_settings_get_entry("play_finish_sound"):
		playsound(utils.path("Media/finish.wav"), block=(platform.system() == "Linux"))

	elapsed = math.floor(time.time() - time_start)
	print(f"Finished in {elapsed} {pluralize('second', elapsed)}.")

	warnings.show_popup_if_necessary()


def get_input_mod_paths(input_folder_path):
	for entry in Path(input_folder_path).iterdir():
		if utils.is_mod_folder(entry):
			yield entry.resolve()


def convert(input_mod_path, input_folder_path, output_folder_path, beautify_lua, output_zip, skip_conversion):

	input_mod_name = input_mod_path.name
	output_mod_path = Path(output_folder_path) / input_mod_name

	zips.unzip(input_mod_path, input_folder_path)

	# TODO: Maybe give this input_mod_path instead of input_folder_path
	case_check.init_glob(output_folder_path, input_folder_path)

	converter_walk(input_mod_path, input_folder_path, output_folder_path, skip_conversion)

	if beautify_lua:
		stylua.stylize(input_mod_path, input_folder_path, output_folder_path)

	ini_cst = ini_cst_builder.get_full_cst(input_folder_path, output_folder_path, input_mod_path)
	ini_rules.apply_rules_on_ini_cst(ini_cst, output_folder_path)
	ini_writer.write_converted_ini_cst(ini_cst, output_mod_path)

	if output_zip:
		zips.zip(input_mod_name, Path(output_folder_path))


def converter_walk(input_mod_path, input_folder_path, output_folder_path, skip_conversion):
	for input_subfolder_path, _input_subfolders, input_subfiles in os.walk(input_mod_path):
		relative_subfolder = utils.get_relative_subfolder(str(input_mod_path), input_subfolder_path)

		if utils.is_mod_folder_or_subfolder(relative_subfolder):
			output_subfolder = os.path.join(output_folder_path, relative_subfolder)
			Path(output_subfolder).mkdir(exist_ok=True)
			process_files(input_subfiles, input_subfolder_path, output_subfolder, input_folder_path, skip_conversion)


def process_files(input_subfiles, input_subfolder_path, output_subfolder, input_folder_path, skip_conversion):
	for full_filename in input_subfiles:
		filename, file_extension = os.path.splitext(full_filename) # TODO: Use pathlib instead here
		file_extension = file_extension.lower()

		input_file_path = os.path.join(input_subfolder_path, full_filename)

		output_file_path = os.path.join(output_subfolder, filename + file_extension)

		if bmp_to_png.is_bmp(full_filename):
			if not skip_conversion:
				bmp_to_png.bmp_to_png(input_file_path, Path(output_file_path).with_suffix(".png"))
			else:
				shutil.copyfile(input_file_path, output_file_path)

		if cfg.progress_bar:
			update_progress.increment_progress()

		if full_filename == "desktop.ini": # Skip this Windows metadata file.
			continue

		if file_extension in (".ini", ".lua"):
			create_converted_file(input_file_path, output_file_path, input_folder_path, skip_conversion)
		elif not bmp_to_png.is_bmp(full_filename):
			shutil.copyfile(input_file_path, output_file_path)


def create_converted_file(input_file_path, output_file_path, input_folder_path, skip_conversion):
	# try: # TODO: Figure out why this try/except is necessary and why it doesn't check for an error type.
	with open(input_file_path, "r", errors="ignore") as file_in: # TODO: Why ignore errors?
		with open(output_file_path, "w") as file_out:
			all_lines = ""
			file_path = os.path.relpath(input_file_path, input_folder_path)

			line_number = 0
			for line in file_in:
				line_number += 1

				line = bmp_to_png.change_bmp_to_png_name(line, skip_conversion)

				# line = lua_parser.convert(line)

				regex_rules.playsound_warning(line, file_path, line_number)

				warnings.append_mod_replacement_warnings(line, file_path, line_number)

				all_lines += line

			# Conversion rules can contain newlines, so they can't be applied on a per-line basis.
			all_lines = apply_conversion_rules(all_lines, skip_conversion)

			# Case matching must be done after conversion, otherwise tons of errors wil be generated
			# all_lines = case_check.case_check(all_lines, input_file_path, output_file_path)

			if not skip_conversion:
				all_lines = regex_rules.regex_replace(all_lines)

			# Case matching must be done after conversion, otherwise tons of errors wil be generated
			all_lines = case_check.case_check(all_lines, input_file_path, output_file_path)

			file_out.write(all_lines)
	# except:
	# 	shutil.copyfile(input_file_path, output_file_path)


def apply_conversion_rules(all_lines, skip_conversion):
	if not skip_conversion:
		for old_str, new_str in conversion_rules.items():
			old_str_parts = os.path.splitext(old_str)
			# Because bmp -> png already happened on all_lines we'll make all old_str conversion rules png.
			if old_str_parts[1] == ".bmp":
				all_lines = all_lines.replace(old_str_parts[0] + ".png", new_str)
			else:
				all_lines = all_lines.replace(old_str, new_str)
	return all_lines


def pluralize(word, count):
	return word + "s" if count != 1 else word
