import os

from Python import shared_globals as cfg
from Python import utils


progress = None
total_progress = None


def increment_progress():
	global progress

	progress += 1

	cfg.progress_bar.update(current_count=progress % total_progress)


def set_max_progress(input_folder_path):
	global progress, total_progress

	progress = 0
	total_progress = 0

	for parent_subfolder_path, _, subfiles in os.walk(input_folder_path):
		relative_subfolder = utils.get_relative_subfolder(input_folder_path, parent_subfolder_path)

		if utils.is_mod_folder_or_subfolder(relative_subfolder):
			total_progress += len(subfiles)

	# TODO: Find a way to track the progress of zipping.
	# if cfg.sg.user_settings_get_entry("output_zips"):
	# 	total_progress = total_progress * 2

	cfg.progress_bar.update(current_count=0, max=total_progress) # current_count=0 is just because max=total_progress would be ignored otherwise
