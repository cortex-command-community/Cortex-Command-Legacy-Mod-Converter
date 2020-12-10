import os, sys
import os.path, pathlib, webbrowser
import PySimpleGUI as sg

from Python import shared_globals as cfg
from Python import convert


sg.user_settings_filename(filename="settings.json", path=".")


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


def init_window():
	if not os.path.isfile(sg.user_settings_filename()):
		clicked_github_button = sg.Popup("This is a tool that allows you to convert legacy (old) mods to the latest version of CCCP. You can get more information from the Legacy Mod Converter GitHub repo.", title="Welcome screen", custom_text="Go to GitHub")
		if clicked_github_button:
			webbrowser.open("https://github.com/cortex-command-community/Cortex-Command-Legacy-Mod-Converter")
	
	no_path_set_color = "#b35858"

	paths_column = [
		[sg.Frame(layout=[
		[
			sg.In(
				sg.user_settings_get_entry("input_folder"),
				size=(37, 1),
				enable_events=True,
				key="-INPUT FOLDER-",
				background_color=sg.theme_input_background_color() if sg.user_settings_get_entry("input_folder") else no_path_set_color
			),
			sg.FolderBrowse()
		],
		[
			sg.ProgressBar(100, size=(23.9, 20), key="-PROGRESS BAR-"),
			sg.Button("Convert", key="-CONVERT-")
		]
		], title="Convert Mods")]
	]

	play_finish_sound_setting = sg.user_settings_get_entry("play_finish_sound")
	sg.user_settings_set_entry("play_finish_sound", True if play_finish_sound_setting == None else play_finish_sound_setting)

	options_column = [
		[sg.Frame(layout=[
		[
			sg.Checkbox("Output zips", size=(8, 1), tooltip=" Zipping is slow ", key="-OUTPUT ZIPS-", default=sg.user_settings_get_entry("output_zips"), enable_events=True),
			sg.Checkbox("Play finish sound", size=(12, 1), tooltip=" For when converting takes long ", key="-PLAY FINISH SOUND-", default=sg.user_settings_get_entry("play_finish_sound"), enable_events=True)
		]
		], title="Options")],
	]

	info_column = [
		[sg.Frame(layout=[
		[
			sg.Image(resource_path("Media/github-icon.png"), enable_events=True, key="-GITHUB-", tooltip=" Visit this program's GitHub page ", size=(0, 30)),
			sg.Image(resource_path("Media/discord-icon.png"), enable_events=True, key="-DISCORD-", tooltip=" Visit the CCCP Discord server for help ", size=(0, 30))
		]
		], title="", pad=((9, 0), (8, 0)))]
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
	convert.load_conversion_rules()

	window = sg.Window("Legacy Mod Converter - v1.0", layout, icon=resource_path("Media/cclmc-icon.ico"), button_color=(sg.theme_text_color(), "#2a3948"))
	cfg.progress_bar = window["-PROGRESS BAR-"]

	return window


def run_window(window):
	while True:
		event, values = window.read()

		if event == "Exit" or event == sg.WIN_CLOSED:
			window.close()
			break

		# print(event, values)

		if event == "-INPUT FOLDER-":
			input_folder_or_file = values[event]
			if input_folder_or_file != "":
				sg.user_settings_set_entry("input_folder", input_folder_or_file)
				window[event](background_color = sg.theme_input_background_color())
		
		elif event == "-OUTPUT ZIPS-":
			sg.user_settings_set_entry("output_zips", values["-OUTPUT ZIPS-"])
		elif event == "-PLAY FINISH SOUND-":
			sg.user_settings_set_entry("play_finish_sound", values["-PLAY FINISH SOUND-"])
		
		elif event == "-CONVERT-":
			if sg.user_settings_get_entry("input_folder") not in (None, ""):
				convert.convert()
		
		elif event == "-GITHUB-":
			webbrowser.open("https://github.com/cortex-command-community/Cortex-Command-Legacy-Mod-Converter")
		elif event == "-DISCORD-":
			webbrowser.open("https://discord.gg/SdNnKJN")