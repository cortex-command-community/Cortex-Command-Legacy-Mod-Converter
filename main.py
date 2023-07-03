import sys
from traceback import TracebackException

import PySimpleGUI as sg

from Python.gui import gui

if __name__ == "__main__":
    try:
        gui.init_window_theme()
        gui.init_settings()
        gui.run_window()
    except Exception as e:
        error = sys.exc_info()[1]
        stack = sys.exc_info()[2]

        te = TracebackException(type(error), error, stack, limit=None, compact=True)
        stack_str = "".join(te.stack.format())

        sg.popup_error(
            error.args[0] + "_" * 60 + "\n",
            "If you can't figure out how to fix the above error, you should make a screenshot of this entire window (using Windows key + Shift + S), and either make a GitHub issue for this by clicking the GitHub icon in this program, or you can send this to MyNameIsTrez#1585 on Discord.\n"
            + "_" * 60
            + "\n",
            stack_str,
            title="Error",
        )
