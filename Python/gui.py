import os, sys, webbrowser
import PySimpleGUI as sg
from pathlib import Path, PurePosixPath

from Python import shared_globals as cfg
from Python import convert
from Python import warnings


no_path_set_color = "#b35858"

CONVERTER_FOLDER_NAME = "_Mod Converter"


# TODO: Move to shared_globals.py
def resource_path(relative_path):
	if hasattr(sys, '_MEIPASS'):
		return os.path.join(sys._MEIPASS, relative_path)
	return os.path.join(os.path.abspath("."), relative_path)


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

	paths_column = [
		[sg.Frame(layout=[
		[
			sg.Text("CCCP folder:	"),
			sg.In(
				sg.user_settings_get_entry("cccp_folder"),
				size=(31, 1),
				tooltip=" Folder of your Cortex Command installation ",
				enable_events = True,
				key="CCCP_FOLDER",
				background_color=sg.theme_input_background_color() if sg.user_settings_get_entry("cccp_folder") else no_path_set_color
			),
			sg.FolderBrowse(size=(7, 1))
		],
		[
			sg.ProgressBar(999, size=(34.2, 40), key="PROGRESS_BAR"),
			sg.Button("Convert", key="CONVERT", size=(7, 1), pad=((5, 0), (14, 15)))
		]
		], title="Convert Mods")]
	]

	play_finish_sound_setting = sg.user_settings_get_entry("play_finish_sound")
	sg.user_settings_set_entry("play_finish_sound", True if play_finish_sound_setting == None else play_finish_sound_setting)

	options_column = [
		[sg.Frame(layout=[
		[
			sg.Checkbox(
				"Skip conversion",
				tooltip=" For previously converted mods, does not skip case matching ",
				key="SKIP_CONV",
				default=sg.user_settings_get_entry("skip_conversion"),
				enable_events=True
			),
			sg.Checkbox(
				"Output zips",
				tooltip=" Zipping is slow ",
				key="OUTPUT_ZIPS",
				default=sg.user_settings_get_entry("output_zips"),
				enable_events=True
			),
			sg.Checkbox(
				"Play finish sound",
				tooltip=" For when converting takes long ",
				key="PLAY_FINISH_SOUND",
				default=sg.user_settings_get_entry("play_finish_sound"),
				enable_events=True
			)
		]], title="Options")],
	]

	info_column = [
		[sg.Frame(layout=[[
			sg.Image(
				resource_path("Media/github-icon.png"),
				enable_events=True,
				key="GITHUB",
				tooltip=" Visit this program's GitHub page ",
				size=(47, 0)
			),
			sg.Image(
				resource_path("Media/discord-icon.png"),
				enable_events=True,
				key="DISCORD",
				tooltip=" Visit the CCCP Discord server for help ",
				size=(48, 0)
			)
		]], title="", pad=((9, 0), (12, 0)))]
	]

	layout = [
		[
			sg.Column(paths_column),
		],
		[
			sg.Column(options_column),
			sg.Column(info_column)
		]
	]

	cfg.sg = sg
	warnings.load_conversion_and_warning_rules()

	window = sg.Window("Legacy Mod Converter", layout, icon=resource_path("Media/legacy-mod-converter.ico"), font=("Helvetica", 16))
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

				input_folder = PurePosixPath(cccp_folder) / CONVERTER_FOLDER_NAME / "Input"
				print(str(input_folder))
				sg.user_settings_set_entry("input_folder", str(input_folder))
			else:
				valid_cccp_path = False
				window[event](background_color = no_path_set_color)

		elif event == "OUTPUT_ZIPS":
			sg.user_settings_set_entry("output_zips", values[event])
		elif event == "PLAY_FINISH_SOUND":
			sg.user_settings_set_entry("play_finish_sound", values[event])
		elif event == "SKIP_CONV":
			sg.user_settings_set_entry("skip_conversion", values[event])


		elif event == "CONVERT":
			if valid_cccp_path:
				convert.convert()


		elif event == "GITHUB":
			webbrowser.open("https://github.com/cortex-command-community/Cortex-Command-Legacy-Mod-Converter")
		elif event == "DISCORD":
			webbrowser.open("https://discord.gg/SdNnKJN")