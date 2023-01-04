import sys, os


def get_path(relative_path):
    """
    sys._MEIPASS is a temporary folder for PyInstaller
    See https://stackoverflow.com/a/13790741/13279557 for more information
    """
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)
