import os, sys

from pathlib import Path


def resource_path(relative_path):
	"""
	sys._MEIPASS is a temporary folder for PyInstaller
	See https://stackoverflow.com/a/13790741/13279557 for more information
	"""
	if hasattr(sys, '_MEIPASS'):
		return os.path.join(sys._MEIPASS, relative_path)
	return os.path.join(os.path.abspath("."), relative_path)


def get_relative_subfolder(input_folder_path, input_subfolder_path):
	return os.path.relpath(input_subfolder_path, os.path.join(input_folder_path, os.pardir) if input_folder_path.endswith(".rte") else input_folder_path)


def is_mod_folder_or_subfolder(mod_subfolder):
	mod_subfolder_parts = get_mod_subfolder_parts(mod_subfolder)
	# If it isn't the input folder and if it's (in) the rte folder.
	return len(mod_subfolder_parts) > 0 and mod_subfolder_parts[0].endswith(".rte")


def get_mod_subfolder_parts(mod_subfolder):
	return Path(mod_subfolder).parts