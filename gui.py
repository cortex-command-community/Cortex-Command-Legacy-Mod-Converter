# Run: python gui.py
# Build: pyinstaller --noconsole --onefile --icon=cclmc-icon.ico --name="Legacy Mod Converter" gui.py

import os.path, pathlib
import PySimpleGUI as sg
import config, convert


def get_folder_containing_mods(mods_folder):
	parts = pathlib.Path(mods_folder).parts
	if parts[-1].endswith(".rte"):
		return pathlib.Path(*parts[:-1]).as_posix() # .as_posix() prevents .replace() issues.
	return mods_folder


paths_column = [
	[sg.Frame(layout=[
	[
		sg.Text("Folder with legacy mod(s)"),
		sg.In(
			sg.user_settings_get_entry("mods_folder"),
			size=(25, 1),
			enable_events=True,
			key="-MODS FOLDER-",
			background_color="light green" if sg.user_settings_get_entry("mods_folder") else "pink"
		),
		sg.FolderBrowse()
	],
	[
		sg.Text("Output CCCP folder"),
		sg.In(
			sg.user_settings_get_entry("output_folder"),
			size=(25, 1),
			enable_events=True,
			key="-OUTPUT FOLDER-",
			background_color="light green" if sg.user_settings_get_entry("output_folder") else "pink"
		),
		sg.FolderBrowse()
	]
	], title="Paths", element_justification="right")],
]

options_column = [
	[sg.Frame(layout=[
		[sg.Checkbox("Output zips", size=(10, 1), tooltip=" Zipping is slow ", key="-OUTPUT ZIPS-", default=sg.user_settings_get_entry("output_zips"))],
		[sg.Checkbox("Play finish sound", size=(12, 1), tooltip=" For when converting takes long ", key="-PLAY FINISH SOUND-", default=sg.user_settings_get_entry("play_finish_sound"))]
	], title="Options")],
]

run_column = [
	[sg.Frame(layout=[
		[sg.Button("Convert", key="-CONVERT-")],
		[sg.ProgressBar(100, size=(22.5, 20), key="-PROGRESS BAR-")]
	], title="Run", element_justification="center")],
]

layout = [
	[
		sg.Column(paths_column),
	],
	[
		sg.Column(options_column),
		sg.Column(run_column)
	]
]

config.sg = sg
window = sg.Window("Legacy Mod Converter - v1.0", layout, icon="I:/Users/welfj/Documents/Programming/Python/cc-legacy-mod-converter/cclmc-icon.ico")
config.progress_bar = window["-PROGRESS BAR-"]


while True:
	event, values = window.read()

	if event == "Exit" or event == sg.WIN_CLOSED:
		window.close()
		break

	if event == "-MODS FOLDER-":
		mods_folder = values[event]
		if mods_folder != "":
			sg.user_settings_set_entry("mods_folder", get_folder_containing_mods(mods_folder))
			window[event](background_color="light green")
	elif event == "-OUTPUT FOLDER-":
		output_folder = values[event]
		if output_folder != "":
			sg.user_settings_set_entry("output_folder", output_folder)
			window[event](background_color="light green")
	elif event == "-CONVERT-":
		if sg.user_settings_get_entry("mods_folder") not in (None, "") and sg.user_settings_get_entry("output_folder") not in (None, ""):
			sg.user_settings_set_entry("output_zips", values["-OUTPUT ZIPS-"])
			sg.user_settings_set_entry("play_finish_sound", values["-PLAY FINISH SOUND-"])
			convert.main()