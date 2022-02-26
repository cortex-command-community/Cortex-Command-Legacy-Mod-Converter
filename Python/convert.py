import os, sys, time, shutil, math, pathlib, webbrowser, platform
from pathlib import Path
from playsound import playsound
import PySimpleGUI as sg

from Python import shared_globals as cfg
from Python import regex_rules
from Python import zips as zips_py
from Python import update_progress
from Python import bmp_to_png
from Python import warnings
from Python.case_check import case_check
from Python import utils

from Python.ini_converting import ini_tokenizer
from Python.ini_converting import ini_parser
from Python.ini_converting import ini_rules
from Python.ini_converting import ini_writer

# from Python.lua_converting import lua_parser


conversion_rules = {} # TODO: Move this.


def convert():
	print("") # Just prints a newline.

	output_folder_path = sg.user_settings_get_entry("cccp_folder")

	time_start = time.time()

	input_folder_path = cfg.sg.user_settings_get_entry("input_folder")
	cccp_folder_path = cfg.sg.user_settings_get_entry("cccp_folder")

	warnings.init_mods_warnings()

	zips_py.unzip(input_folder_path)

	update_progress.set_max_progress(input_folder_path)

	case_check.init_glob(cccp_folder_path, input_folder_path)

	converter_walk(input_folder_path, output_folder_path)


	token_cst = ini_tokenizer.get_token_cst(input_folder_path, mod_names)
	cst = ini_parser.parse_token_cst(token_cst)
	ini_rules.apply_rules_on_cst(cst)
	ini_writer.write_converted_ini_recursively(cst, Path(output_folder_path))


	if cfg.sg.user_settings_get_entry("output_zips"):
		zips_py.create_zips(input_folder_path, output_folder_path)

	if cfg.sg.user_settings_get_entry("play_finish_sound"):
		playsound(utils.resource_path("Media/finish.wav"), block=(platform.system() == "Linux"))


	elapsed = math.floor(time.time() - time_start)
	print(f"Finished in {elapsed} {pluralize('second', elapsed)}.")

	warnings.show_popup_if_necessary()


def converter_walk(input_folder_path, output_folder_path):
	for input_subfolder_path, input_subfolders, input_subfiles in os.walk(input_folder_path):
		relative_subfolder = utils.get_relative_subfolder(input_folder_path, input_subfolder_path)

		if is_mod_folder(relative_subfolder):
			warnings.clear_mod_warnings()

		if utils.is_mod_folder_or_subfolder(relative_subfolder):
			output_subfolder = os.path.join(output_folder_path, relative_subfolder)
			create_folder(input_subfolder_path, output_subfolder)
			process_files(input_subfiles, input_subfolder_path, output_subfolder, input_folder_path, output_folder_path)


def is_mod_folder(relative_subfolder):
	# If it isn't the input folder and if it's the rte folder.
	mod_subfolder_parts = utils.get_mod_subfolder_parts(relative_subfolder)
	return len(mod_subfolder_parts) == 1 and mod_subfolder_parts[0].endswith(".rte")


def create_folder(input_subfolder_path, output_subfolder):
	try:
		os.makedirs(output_subfolder)
	except FileExistsError:
		pass


def process_files(input_subfiles, input_subfolder_path, output_subfolder, input_folder_path, output_folder_path):
	for full_filename in input_subfiles:
		filename, file_extension = os.path.splitext(full_filename)
		file_extension = file_extension.lower()

		input_file_path = os.path.join(input_subfolder_path, full_filename)

		output_file_path = os.path.join(output_subfolder, filename + file_extension)

		if bmp_to_png.is_bmp(full_filename):
			if not cfg.sg.user_settings_get_entry("skip_conversion"):
				bmp_to_png.bmp_to_png(input_file_path, Path(output_file_path).with_suffix(".png"))
			else:
				shutil.copyfile(input_file_path, output_file_path)

		update_progress.increment_progress()

		if full_filename == "desktop.ini": # Skip this Windows metadata file.
			continue

		if file_extension in (".ini", ".lua"):
			create_converted_file(input_file_path, output_file_path, input_folder_path, file_extension)
		elif not bmp_to_png.is_bmp(full_filename):
			shutil.copyfile(input_file_path, output_file_path)


def create_converted_file(input_file_path, output_file_path, input_folder_path, file_extension):
	# try: # TODO: Figure out why this try/except is necessary and why it doesn't check for an error type.
	with open(input_file_path, "r", errors="ignore") as file_in: # TODO: Why ignore errors?
		with open(output_file_path, "w") as file_out:
			all_lines = ""
			file_path = os.path.relpath(input_file_path, input_folder_path)

			line_number = 0
			for line in file_in:
				line_number += 1

				line = bmp_to_png.change_bmp_to_png_name(line)

				# line = lua_parser.convert(line)

				regex_rules.playsound_warning(line, file_path, line_number)

				warnings.append_mod_replacement_warnings(line, file_path, line_number)

				all_lines += line

			# Conversion rules can contain newlines, so they can't be applied on a per-line basis.
			all_lines = apply_conversion_rules(all_lines)

			# Case matching must be done after conversion, otherwise tons of errors wil be generated
			all_lines = case_check.case_check(all_lines, input_file_path, output_file_path)

			if not cfg.sg.user_settings_get_entry("skip_conversion"):
				all_lines = regex_rules.regex_replace(all_lines)

			file_out.write(all_lines)
	# except:
	# 	shutil.copyfile(input_file_path, output_file_path)


def apply_conversion_rules(all_lines):
	if not cfg.sg.user_settings_get_entry("skip_conversion"):
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