import PySimpleGUI as sg

from Python import utils
from Python import shared_globals as cfg


def get_main_window_layout():
	return [
		[
			[
				sg.FolderBrowse(
					"CCCP folder",
					# size=(7, 1),
					# pad=(
					# 	(15, 15),
					# 	(3, 0),
					# )
				),
				sg.In(
					sg.user_settings_get_entry("cccp_folder"),
					size=(43, 1),
					tooltip=" Location of your CCCP folder ",
					enable_events = True,
					key="CCCP_FOLDER",
					background_color=sg.theme_input_background_color() if sg.user_settings_get_entry("cccp_folder") else cfg.NO_PATH_SET_COLOR,
					pad=(
						(0, 0),
						(3, 0),
					)
				)
			],
			[
				sg.Button(
					"Settings",
					key="LAUNCH_SETTINGS_WINDOW"
				),
				sg.Button(
					"Convert",
					key="CONVERT",
					size=(7, 1),
					pad=(
						(15, 0),
						(15, 15)
					)
				),
				sg.ProgressBar(
					999,
					size=(30, 40),
					key="PROGRESS_BAR",
					pad=(
						(15, 0),
						(0, 0)
					)
				),
				sg.Image(
					utils.path("Media/github-icon.png"),
					enable_events=True,
					key="GITHUB",
					tooltip=" Visit this program's GitHub page ",
					size=(56, 47)
				),
				sg.Image(
					utils.path("Media/discord-icon.png"),
					enable_events=True,
					key="DISCORD",
					tooltip=" Visit the CCCP Discord server for help ",
				),
			]
		]
	]


def get_main_window():
	return sg.Window(
		title=f"Legacy Mod Converter {cfg.CONVERTER_VERSION} for CCCP {cfg.GAME_VERSION}",
		layout=get_main_window_layout(),
		icon=utils.path("Media/legacy-mod-converter.ico"),
		font=("Helvetica", 16),
		finalize=True
	)
	# window.finalize() # TODO: Check if this reduces the white flicker at the start of the program.


def get_settings_window_layout():
	return [
		[
			[sg.Checkbox(
				"Skip conversion",
				tooltip=" For previously converted mods, does not skip case matching ",
				key="SKIP_CONVERSION",
				default=sg.user_settings_get_entry("skip_conversion"),
				enable_events=True,
			)],
			[sg.Checkbox(
				"Output zips",
				tooltip=" Zipping is slow ",
				key="OUTPUT_ZIPS",
				default=sg.user_settings_get_entry("output_zips"),
				enable_events=True,
			)],
			[sg.Checkbox(
				"Play finish sound",
				tooltip=" Notifies you when the conversion has finished ",
				key="PLAY_FINISH_SOUND",
				default=sg.user_settings_get_entry("play_finish_sound"),
				enable_events=True,
			)]
		]
	]


def get_settings_window():
	return sg.Window(
		title="Settings",
		layout=get_settings_window_layout(),
		icon=utils.path("Media/legacy-mod-converter.ico"),
		font=("Helvetica", 16),
		finalize=True
	)
	# window.finalize() # TODO: Check if this reduces the white flicker at the start of the program.
