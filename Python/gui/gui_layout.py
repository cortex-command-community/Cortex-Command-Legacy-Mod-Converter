import PySimpleGUI as sg

from Python import utils


def get_layout():
	return [
		[
			sg.Column(get_paths_column()),
		],
		[
			sg.Column(get_options_column()),
			sg.Column(get_info_column())
		]
	]


def get_paths_column():
	return [
		[
			sg.Frame(
				layout=[
					[
						sg.Text(
							"CCCP folder:",
							pad=(
								(13, 12),
								(0, 0),
							)
						),
						sg.In(
							sg.user_settings_get_entry("cccp_folder"),
							size=(36, 1),
							tooltip=" Folder of your Cortex Command installation ",
							enable_events = True,
							key="CCCP_FOLDER",
							background_color=sg.theme_input_background_color() if sg.user_settings_get_entry("cccp_folder") else no_path_set_color,
							pad=(
								(0, 0),
								(3, 0),
							)
						),
						sg.FolderBrowse(
							size=(7, 1),
							pad=(
								(15, 15),
								(3, 0),
							)
						)
					],
					[
						sg.ProgressBar(
							999,
							size=(34.2, 40),
							key="PROGRESS_BAR",
							pad=(
								(7, 0),
								(0, 0)
							)
						),
						sg.Button(
							"Convert",
							key="CONVERT",
							size=(7, 1),
							pad=(
								(15, 0),
								(14, 15)
							)
						)
					]
				],
				title="Convert Mods"
			)
		]
	]


def get_options_column():
	return [
		[
			sg.Frame(
				layout=[
					[
						sg.Checkbox(
							"Skip conversion",
							tooltip=" For previously converted mods, does not skip case matching ",
							key="SKIP_CONVERSION",
							default=sg.user_settings_get_entry("skip_conversion"),
							enable_events=True,
							pad=(
								(100, 0),
								(0, 50)
							)
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
					]
				],
				title="Options"
			)
		],
	]


def get_info_column():
	return [
		[
			sg.Frame(
				layout=[
					[
						sg.Image(
							utils.resource_path("Media/github-icon.png"),
							enable_events=True,
							key="GITHUB",
							tooltip=" Visit this program's GitHub page ",
							size=(47, 0)
						),
						sg.Image(
							utils.resource_path("Media/discord-icon.png"),
							enable_events=True,
							key="DISCORD",
							tooltip=" Visit the CCCP Discord server for help ",
							size=(48, 0)
						)
					]
				],
				title="",
				pad=(
					(9, 0),
					(12, 0)
				)
			)
		]
	]