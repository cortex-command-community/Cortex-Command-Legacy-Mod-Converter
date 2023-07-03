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

        sg.popup_no_buttons(
            "Most errors are very easy to fix, so please take a minute to look closely at the below error.\nIf you still aren't able to figure it out on your own, make a screenshot of this entire window by pressing Windows key + Shift + S at the same time, and pressing Ctrl + V to paste this in the #project-mod-converter channel of the CCCP Discord server.\n"
            + "_" * 60,
            error.args[0] + "_" * 60,
            "Extra information for MyNameIsTrez:",
            stack_str,
            title="Error",
        )
