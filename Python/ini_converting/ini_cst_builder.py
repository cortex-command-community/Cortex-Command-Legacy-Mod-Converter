import os
from pathlib import Path

from Python import utils
from Python.ini_converting import ini_tokenizer
from Python.ini_converting import ini_parser


def get_ini_cst(input_folder_path, output_folder_path, subfolder_path):
	"""
	The "cst" in this function's name stands for Concrete Syntax Tree.
	"""
	parsed_portion = {}

	for name in os.listdir(subfolder_path):
		p = subfolder_path / Path(name)
		relative_subfolder = utils.get_relative_subfolder(input_folder_path, str(p))

		if not utils.is_mod_folder_or_subfolder(relative_subfolder): # TODO: Remove this once CCCP has a Mods folder that can be iterated over.
			continue
		elif p.is_file() and p.suffix == ".ini" and p.stem != "desktop": # Skip the desktop.ini Windows metadata file.
			output_file_path = utils.get_output_file_path_from_input_file_path(input_folder_path, output_folder_path, p)
			tokens = ini_tokenizer.get_tokens(output_file_path)
			parsed_portion[name] = ini_parser.get_parsed_tokens(tokens)
		elif p.is_dir():
			parsed_portion[name] = get_ini_cst(input_folder_path, output_folder_path, str(p))

	return parsed_portion
