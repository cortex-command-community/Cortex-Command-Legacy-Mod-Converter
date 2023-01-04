import os
from pathlib import Path

from Python import utils
from Python.ini_converting import ini_tokenizer
from Python.ini_converting import ini_cst
from Python import shared_globals as cfg


def get_full_cst(input_folder_path, output_folder_path, subfolder_path):
    """
    The "cst" in this function's name stands for Concrete Syntax Tree. Returns the tree root and the number of ini files.
    """
    parsed_portion = {}

    for name in os.listdir(subfolder_path):
        p = subfolder_path / Path(name)
        relative_subfolder = utils.get_relative_subfolder(input_folder_path, str(p))

        if not utils.is_mod_folder_or_subfolder(
            relative_subfolder
        ):  # TODO: Remove this once CCCP has a Mods folder that can be iterated over.
            continue
        elif (
            p.is_file() and p.suffix == ".ini" and p.stem != "desktop"
        ):  # Skips the desktop.ini Windows metadata file.
            output_file_path = output_folder_path / Path(relative_subfolder)
            tokens = ini_tokenizer.get_tokens(output_file_path)
            parsed_portion[name] = ini_cst.get_cst(tokens)
            cfg.progress_bar.inc()
        elif p.is_dir():
            cst = get_full_cst(input_folder_path, output_folder_path, str(p))
            parsed_portion[name] = cst

    return parsed_portion
