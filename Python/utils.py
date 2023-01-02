import os, sys

from pathlib import Path


def path(relative_path):
    """
    sys._MEIPASS is a temporary folder for PyInstaller
    See https://stackoverflow.com/a/13790741/13279557 for more information
    """
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


def get_relative_subfolder(input_folder_path, input_subfolder_path):
    return os.path.relpath(
        input_subfolder_path,
        os.path.join(input_folder_path, os.pardir)
        if input_folder_path.endswith(".rte")
        else input_folder_path,
    )


def is_mod_folder(entry):
    return entry.is_dir() and entry.suffix == ".rte"


def is_mod_folder_or_subfolder(path):
    path_parts = Path(path).parts
    # If it is a folder inside of the input folder and if it is the mod folder or is inside of it.
    return len(path_parts) >= 1 and path_parts[0].endswith(".rte")


def get_output_path_from_input_path(input_folder_path, output_folder_path, input_path):
    relative = input_path.relative_to(input_folder_path)
    return str(output_folder_path / relative)
