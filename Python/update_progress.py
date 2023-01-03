import os

from Python import shared_globals as cfg
from Python import utils


progress = None
total_progress = None


def increment_progress(n=1):
    global progress

    progress += n
    cfg.progress_bar.update(current_count=progress % total_progress)
    # print(f"\tTP: {progress}")


def get_progress():
    global progress
    return progress


def set_progress(i):

    cfg.progress_bar.update(current_count=i)


def set_max_progress(input):
    global progress, total_progress

    progress = 0
    total_progress = 0

    if type(input) == int:
        total_progress = input
        cfg.progress_bar.update(
            max=total_progress, current_count=progress % total_progress
        )
        return

    for parent_subfolder_path, _, subfiles in os.walk(input):
        relative_subfolder = utils.get_relative_subfolder(input, parent_subfolder_path)

        if utils.is_mod_folder_or_subfolder(relative_subfolder):
            total_progress += len(subfiles)

    # TODO: Find a way to track the progress of zipping.
    # if cfg.sg.user_settings_get_entry("output_zips"):
    # 	total_progress = total_progress * 2

    cfg.progress_bar.update(
        current_count=progress, max=total_progress
    )  # current_count=0 is just because max=total_progress would be ignored otherwise
