# Run manually: python main.py
# Build EXE: pyinstaller --noconsole --onefile --icon="Media/legacy-mod-converter.ico" --add-data="Media/github-icon.png;Media" --add-data="Media/discord-icon.png;Media" --add-data="Media/finish.wav;Media" --name="Legacy Mod Converter" main.py


import traceback
import PySimpleGUI as sg

from Python import tests
from Python.gui import gui


if __name__ == '__main__':
	try: # TODO: The VS Code Python debugger isn't able to catch exceptions due to this.
		gui.init_window_theme()
		tests.run()
		gui.run_window(gui.init_window())
	except Exception as e:
		sg.popup_error("AN EXCEPTION OCCURRED!\n\nYou should make a screenshot of this and either make a GitHub issue for this by clicking the GitHub icon in this program, or you can send it to MyNameIsTrez#1585 on Discord.\n" + "_" * 60, traceback.format_exc(), title="AN EXCEPTION OCCURRED!")