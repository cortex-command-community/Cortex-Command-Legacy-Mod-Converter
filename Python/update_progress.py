import os

from Python import shared_globals as cfg


progress = 0
total_progress = 0


def increment_progress():
	global progress # TODO: See what happens when this line is removed.
	progress += 1
	cfg.progress_bar.UpdateBar(progress % total_progress, total_progress)


def set_max_progress(input_folder_path):
	global total_progress # TODO: See what happens when this line is removed.
	if input_folder_path.endswith(".rte"):
		mod_count = 1
	else:
		mod_count = 0
		for mod_name in os.listdir(input_folder_path):
			if os.path.isdir(os.path.join(input_folder_path, mod_name)) and mod_name.endswith(".rte"):
				mod_count += 1
	total_progress = mod_count * 2 if cfg.sg.user_settings_get_entry("output_zips") else mod_count