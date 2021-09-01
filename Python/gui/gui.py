import os, webbrowser
import PySimpleGUI as sg
from pathlib import Path, PurePosixPath

from Python import utils
from Python import shared_globals as cfg
from Python import convert
from Python import warnings
from Python.gui import gui_layout


def init_window_theme():
	path_set_color = "#528b30"
	progress_bar_color = "#17569c"

	sg.theme("DarkGrey14")
	sg.theme_input_background_color(path_set_color)
	sg.theme_progress_bar_color((progress_bar_color, sg.theme_progress_bar_color()[1]))
	sg.theme_button_color((sg.theme_text_color(), "#2a3948"))


def init_window():
	sg.user_settings_filename(filename="settings.json", path=".")

	if not os.path.isfile(sg.user_settings_filename()):
		sg.Popup("This is a tool that allows you to convert legacy (old) mods to the latest version of CCCP. You can get more information from the GitHub repo or the Discord server by clicking the corresponding icons.", title="Welcome screen", custom_text=" OK ")

	# if not sg.user_settings_get_entry("cccp_folder"):
	# 	sg.user_settings_set_entry("cccp_folder", "Input")

	play_finish_sound_setting = sg.user_settings_get_entry("play_finish_sound")
	sg.user_settings_set_entry("play_finish_sound", True if play_finish_sound_setting == None else play_finish_sound_setting)

	cfg.sg = sg
	warnings.load_conversion_and_warning_rules() # TODO: Why is this called in this GUI function?

	window = sg.Window(
		"Legacy Mod Converter",
		gui_layout.get_layout(),
		icon=utils.resource_path("Media/legacy-mod-converter.ico"),
		font=("Helvetica", 16)
	)
	cfg.progress_bar = window["PROGRESS_BAR"]
	window.finalize()

	return window


def run_window(window):
	valid_cccp_path = True if sg.user_settings_get_entry("cccp_folder") else False

	while True:
		event, values = window.read()

		if event == "Exit" or event == sg.WIN_CLOSED:
			window.close()
			break

		# print(event, values)

		if event == "CCCP_FOLDER":
			cccp_folder = values[event]
			if Path(cccp_folder).exists():
				valid_cccp_path = True
				window[event](background_color = sg.theme_input_background_color())
				
				sg.user_settings_set_entry("cccp_folder", cccp_folder)

				input_folder = PurePosixPath(cccp_folder) / cfg.CONVERTER_FOLDER_NAME / "Input" # Can't save Windows paths in settings.json
				sg.user_settings_set_entry("input_folder", str(input_folder))
			else:
				valid_cccp_path = False
				window[event](background_color = cfg.NO_PATH_SET_COLOR)

		elif event == "OUTPUT_ZIPS":
			sg.user_settings_set_entry("output_zips", values[event])
		elif event == "PLAY_FINISH_SOUND":
			sg.user_settings_set_entry("play_finish_sound", values[event])
		elif event == "SKIP_CONVERSION":
			sg.user_settings_set_entry("skip_conversion", values[event])

		elif event == "CONVERT":
			if valid_cccp_path:
				convert.convert()

		elif event == "GITHUB":
			webbrowser.open("https://github.com/cortex-command-community/Cortex-Command-Legacy-Mod-Converter")
		elif event == "DISCORD":
			webbrowser.open("https://discord.gg/TSU6StNQUG")