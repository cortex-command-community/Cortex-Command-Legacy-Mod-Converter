import os, sys
import pathlib, webbrowser
import PySimpleGUI as sg

from Python import shared_globals as cfg
from Python import convert


sg.user_settings_filename(filename="settings.json", path=".")
no_path_set_color = "#b35858"


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
	if not os.path.isfile(sg.user_settings_filename()):
		sg.Popup("This is a tool that allows you to convert legacy (old) mods to the latest version of CCCP. You can get more information from the GitHub repo or the Discord server by clicking the corresponding icons.", title="Welcome screen", custom_text=" OK ")

	paths_column = [
		[sg.Frame(layout=[
		[
			sg.In(
				sg.user_settings_get_entry("input_folder"),
				size=(31, 1),
				enable_events=True,
				key="-INPUT FOLDER-",
				background_color=sg.theme_input_background_color() if sg.user_settings_get_entry("input_folder") else no_path_set_color
			),
			sg.FolderBrowse(size=(7, 1))
		],
		[
			sg.ProgressBar(999, size=(34.2, 40), key="-PROGRESS BAR-"),
			sg.Button("Convert", key="-CONVERT-", size=(7, 1), pad=((5, 0), (14, 15)))
		]
		], title="Convert Mods")]
	]

	play_finish_sound_setting = sg.user_settings_get_entry("play_finish_sound")
	sg.user_settings_set_entry("play_finish_sound", True if play_finish_sound_setting == None else play_finish_sound_setting)

	options_column = [
		[sg.Frame(layout=[[
			sg.Checkbox("Output zips", tooltip=" Zipping is slow ", key="-OUTPUT ZIPS-", default=sg.user_settings_get_entry("output_zips"), enable_events=True),
			sg.Checkbox("Play finish sound", tooltip=" For when converting takes long ", key="-PLAY FINISH SOUND-", default=sg.user_settings_get_entry("play_finish_sound"), enable_events=True)
		]], title="Options")],
	]

	info_column = [
		[sg.Frame(layout=[[
			sg.Image(resource_path("Media/github-icon.png"), enable_events=True, key="-GITHUB-", tooltip=" Visit this program's GitHub page ", size=(47, 0)),
			sg.Image(resource_path("Media/discord-icon.png"), enable_events=True, key="-DISCORD-", tooltip=" Visit the CCCP Discord server for help ", size=(48, 0))
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
	convert.load_conversion_and_warning_rules()

	window = sg.Window("Legacy Mod Converter", layout, icon=resource_path("Media/legacy-mod-converter.ico"), font=("Helvetica", 16))
	cfg.progress_bar = window["-PROGRESS BAR-"]

	return window


def run_window(window):
	valid_input_path = True if sg.user_settings_get_entry("input_folder") else False

	while True:
		event, values = window.read()

		if event == "Exit" or event == sg.WIN_CLOSED:
			window.close()
			break

		# print(event, values)

		if event == "-INPUT FOLDER-":
			input_folder = values[event]
			if os.path.exists(input_folder):
				valid_input_path = True
				window[event](background_color = sg.theme_input_background_color())
				sg.user_settings_set_entry("input_folder", input_folder)
			else:
				valid_input_path = False
				window[event](background_color = no_path_set_color)
		
		elif event == "-OUTPUT ZIPS-":
			sg.user_settings_set_entry("output_zips", values[event])
		elif event == "-PLAY FINISH SOUND-":
			sg.user_settings_set_entry("play_finish_sound", values[event])
		
		elif event == "-CONVERT-":
			if valid_input_path:
				convert.convert()

		
		elif event == "-GITHUB-":
			webbrowser.open("https://github.com/cortex-command-community/Cortex-Command-Legacy-Mod-Converter")
		elif event == "-DISCORD-":
			webbrowser.open("https://discord.gg/SdNnKJN")