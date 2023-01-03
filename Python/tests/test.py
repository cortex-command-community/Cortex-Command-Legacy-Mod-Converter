from pathlib import Path

from Python import utils


def get_test_path_from_filename(filename):
    return Path(utils.path(f"Python/tests/ini_test_files/{filename}.ini"))
