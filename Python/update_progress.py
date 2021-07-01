import os

from Python import shared_globals as cfg


progress = 0
total_progress = 0


def increment_progress():
	global progress # TODO: See what happens when this line is removed.
	progress += 1
	if total_progress != 0:
		cfg.progress_bar.UpdateBar(progress % total_progress, total_progress)


def set_max_progress(input_folder_path):
	global progress, total_progress  # TODO: See what happens when this line is removed.

	progress = 0
	total_progress = 0

	for input_subfolder_path, input_subfolders, input_subfiles in os.walk(input_folder_path):
		for filename in input_subfiles:
			total_progress += 1

	# TODO: Find a way to track the progress of zipping.
	# if cfg.sg.user_settings_get_entry("output_zips"):
	# 	total_progress = total_progress * 2