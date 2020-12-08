import os.path, pathlib, webbrowser
import PySimpleGUI as sg

from Python import shared_globals as cfg
from Python import convert


sg.user_settings_filename(filename="settings.json", path=".")


def init_window_theme():
	path_set_color = "#528b30"
	progress_bar_color = "#17569c"

	sg.theme("DarkGrey14")
	sg.theme_input_background_color(path_set_color)
	sg.theme_progress_bar_color((progress_bar_color, sg.theme_progress_bar_color()[1]))


def get_input_folder(input_folder):
	parts = pathlib.Path(input_folder).parts
	if parts[-1].endswith(".rte"):
		return pathlib.Path(*parts[:-1]).as_posix() # .as_posix() prevents .replace() issues.
	return input_folder


def init_window():
	no_path_set_color = "#b35858"

	paths_column = [
		[sg.Frame(layout=[
		[
			sg.Text("Mod to convert"),
			sg.In(
				sg.user_settings_get_entry("input_folder"),
				size=(34, 1),
				enable_events=True,
				key="-INPUT FOLDER-",
				background_color=sg.theme_input_background_color() if sg.user_settings_get_entry("input_folder") else no_path_set_color
			),
			sg.FolderBrowse()
		]
		], title="Paths", element_justification="right")]
	]

	options_column = [
		[sg.Frame(layout=[
			[sg.Checkbox("Output zips", size=(10, 1), tooltip=" Zipping is slow ", key="-OUTPUT ZIPS-", default=sg.user_settings_get_entry("output_zips"), enable_events=True)],
			[sg.Checkbox("Play finish sound", size=(12, 1), tooltip=" For when converting takes long ", key="-PLAY FINISH SOUND-", default=sg.user_settings_get_entry("play_finish_sound"), enable_events=True)]
		], title="Options")],
	]

	run_column = [
		[sg.Frame(layout=[
			[sg.Button("Convert", key="-CONVERT-")],
			[sg.ProgressBar(100, size=(17.4, 20), key="-PROGRESS BAR-")]
		], title="Run", element_justification="center")]
	]

	info_column = [
		[sg.Frame(layout=[
			[sg.Image("media/github-icon.png", enable_events=True, key="-GITHUB-", tooltip=" Visit this program's GitHub page ")],
			[sg.Image("media/discord-icon.png", enable_events=True, key="-DISCORD-", tooltip=" Visit the CCCP Discord server ")]
		], title="", pad=(0, (8, 0)))]
	]

	layout = [
		[
			sg.Column(paths_column),
		],
		[
			sg.Column(options_column),
			sg.Column(run_column),
			sg.Column(info_column)
		]
	]

	cfg.sg = sg
	window = sg.Window("Legacy Mod Converter - v1.0", layout, icon="media/cclmc-icon.ico", button_color=(sg.theme_text_color(), "#2a3948"))
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
				sg.user_settings_set_entry("input_folder", get_input_folder(input_folder_or_file))
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