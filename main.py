import traceback

import PySimpleGUI as sg

from Python.gui import gui

if __name__ == "__main__":
    try:
        gui.init_window_theme()
        gui.init_settings()
        gui.run_window()
    except Exception as e:
        sg.popup_error(
            "AN EXCEPTION OCCURRED!\n\nYou should make a screenshot of this and either make a GitHub issue for this by clicking the GitHub icon in this program, or you can send it to MyNameIsTrez#1585 on Discord.\n"
            + "_" * 60,
            traceback.format_exc(),
            title="AN EXCEPTION OCCURRED!",
        )
