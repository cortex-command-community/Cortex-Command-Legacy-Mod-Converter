# Run manually: python main.py
# Build EXE: pyinstaller --noconsole --onefile --icon="Media/legacy-mod-converter.ico" --add-data="Media/github-icon.png;Media" --add-data="Media/discord-icon.png;Media" --add-data="Media/finish.wav;Media" --add-data="Media/palette.bmp;Media" --name="Legacy Mod Converter" main.py


import traceback
import PySimpleGUI as sg

from Python.gui import gui


try:
	gui.init_window_theme()
	gui.run_window(gui.init_window())
except Exception as e:
	tb = traceback.format_exc()
	sg.popup_error("AN EXCEPTION OCCURRED!\n\nYou should make a screenshot of this and either make a GitHub issue for this by clicking the GitHub icon in this program, or you can send it to MyNameIsTrez#1585 on Discord.\n" + "_" * 60, e, tb, title="AN EXCEPTION OCCURRED!")