# Use "python gui.py", "py gui.py" doesn't work.
# Run "pyinstaller --noconsole --onefile gui.py"

import os.path, pathlib
import PySimpleGUI as sg
import config, convert


def get_folder_containing_mods(mods_folder):
	parts = pathlib.Path(mods_folder).parts
	if parts[-1].endswith(".rte"):
		return pathlib.Path(*parts[:-1]).as_posix() # .as_posix() prevents .replace() problems.
	return mods_folder


paths_column = [
	[sg.Frame(layout=[
	[
		sg.Text("Folder with legacy mod(s)"),
		sg.In(size=(25, 1), enable_events=True, key="-MODS FOLDER-"),
		sg.FolderBrowse()
	],
	[
		sg.Text("Output CCCP folder"),
		sg.In(size=(25, 1), enable_events=True, key="-OUTPUT FOLDER-"),
		sg.FolderBrowse()
	]
	], title='Paths', element_justification='right')],
]

options_column = [
	[sg.Frame(layout=[
		[sg.Checkbox('Output zips', size=(10, 1), tooltip=' Zipping is slow ', key="-OUTPUT ZIPS-")],
		[sg.Checkbox('Play finish sound', size=(12, 1), tooltip=' For when converting takes long ', key="-PLAY FINISH SOUND-", default=True)]
	], title='Options')],
]

run_column = [
	[sg.Frame(layout=[
		[sg.Button('Convert', key="-CONVERT-")],
		[sg.ProgressBar(100, size=(22.5, 20), key='-PROGRESS BAR-')]
	], title='Run', element_justification='center')],
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

window = sg.Window("Legacy Mod Converter - Alpha", layout)
config.progress_bar = window['-PROGRESS BAR-']


while True:
	event, values = window.read()

	if event == "Exit" or event == sg.WIN_CLOSED:
		window.close()
		break

	# print("EVENT:", event)
	# print("VALUES:", values)

	if event == "-MODS FOLDER-":
		mods_folder = values[event]
		if mods_folder != "":
			config.mods_folder = get_folder_containing_mods(mods_folder)
	elif event == "-OUTPUT FOLDER-":
		config.output_folder = values[event]
	elif event == "-CONVERT-":
		# TODO: Prevent the user from pressing the "Convert" button if the mods & output folder haven't been set yet.
		# TODO: Retain paths from last time .exe was started somehow. 
		config.output_zips = values["-OUTPUT ZIPS-"]
		config.play_finish_sound = values["-PLAY FINISH SOUND-"]
		convert.main()