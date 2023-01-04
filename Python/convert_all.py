import math
import platform
import time
from pathlib import Path

import PySimpleGUI as sg
from cortex_command_mod_converter_engine import convert
from playsound import playsound

from Python.utils import get_path


def convert_all(progress_bar):
    time_start = time.time()

    input_folder_path = str(
        Path(sg.user_settings_get_entry("cccp_folder"))
        / "LegacyModConverter-v1.2-pre4.0"
        / "Input"
    )
    output_folder_path = sg.user_settings_get_entry("cccp_folder")

    mod_count = len(list(get_input_mod_paths(input_folder_path)))
    progress_bar.segment(mod_count)
    for i, input_mod_path in enumerate(get_input_mod_paths(input_folder_path)):
        progress_bar.setTitle(
            f"Converting {input_mod_path.stem}{input_mod_path.suffix} ({i+1}/{mod_count})...\t"
        )
        convert.convert(
            input_mod_path,
            output_folder_path,
            sg.user_settings_get_entry("beautify_lua"),
            sg.user_settings_get_entry("output_zips"),
            sg.user_settings_get_entry("skip_conversion"),
        )

    if sg.user_settings_get_entry("play_finish_sound"):
        playsound(get_path("Media/finish.wav"), block=(platform.system() == "Linux"))

    elapsed = math.floor(time.time() - time_start)
    time_str = f"Finished in {elapsed} {pluralize('second', elapsed)}."
    if progress_bar:
        progress_bar.setText(time_str, "")

    print(time_str)

    from Python.gui.gui import unlock_convert_button

    unlock_convert_button()


def get_input_mod_paths(input_folder_path):
    for entry in Path(input_folder_path).iterdir():
        if is_mod_folder(entry):
            yield entry.resolve()


def is_mod_folder(entry):
    return entry.is_dir() and entry.suffix == ".rte"


def pluralize(word, count):
    return word + "s" if count != 1 else word
