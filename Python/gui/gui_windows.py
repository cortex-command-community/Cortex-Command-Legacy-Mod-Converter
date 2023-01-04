import PySimpleGUI as sg

import Python.cfg as cfg
from Python.utils import get_path


window = None


def get_main_window_layout():
    progressColumn = [
        [
            sg.ProgressBar(
                max_value=None,  # Calculated and set later on
                key="PROGRESS_BAR",
                size=(47, 35),
                pad=((5, 3), (6, 0)),
            )
        ],
        [
            sg.Text(
                text="Waiting...",
                size=(72, 1),
                key="PROGRESS_BAR_TEXT",
                font=("Helvetica", 9),
            )
        ],
    ]

    return [
        [
            sg.FolderBrowse(
                "CCCP folder",
                size=(12, None),
                pad=((10, 0), (15, 0)),
            ),
            sg.InputText(
                sg.user_settings_get_entry("cccp_folder"),
                tooltip=" Location of your CCCP folder ",
                enable_events=True,
                key="CCCP_FOLDER",
                background_color=sg.theme_input_background_color()
                if sg.user_settings_get_entry("cccp_folder")
                else cfg.NO_PATH_SET_COLOR,
                font=("Helvetica", 20),
                size=(61, None),
                pad=((20, 0), (15, 0)),
            ),
        ],
        [
            sg.Button(
                "Settings",
                key="LAUNCH_SETTINGS_WINDOW",
                size=(12, None),
                pad=((10, 0), (20, 14)),
            ),
            sg.Button(
                "Convert",
                key="CONVERT",
                size=(12, None),
                pad=((20, 0), (20, 14)),
            ),
            sg.Column(progressColumn, element_justification="left"),
            sg.Image(
                get_path("Media/github-icon.png"),
                enable_events=True,
                key="GITHUB",
                tooltip=" Visit this program's GitHub page ",
                pad=((17, 0), (7, 0)),
            ),
            sg.Image(
                get_path("Media/discord-icon.png"),
                enable_events=True,
                key="DISCORD",
                tooltip=" Visit the CCCP Discord server for help ",
                pad=((13, 3), (1, 0)),
            ),
        ],
    ]


def get_main_window():
    global window
    if not window:
        window = sg.Window(
            title=f"Legacy Mod Converter {cfg.CONVERTER_VERSION} for CCCP {cfg.GAME_VERSION}",
            layout=get_main_window_layout(),
            icon=get_path("Media/legacy-mod-converter.ico"),
            font=("Helvetica", 25),
            finalize=True,
        )

    return window


def get_settings_window_layout():
    return [
        [
            [
                sg.Checkbox(
                    "Skip conversion",
                    tooltip=" For previously converted mods, does not skip case matching ",
                    key="SKIP_CONVERSION",
                    default=sg.user_settings_get_entry("skip_conversion"),
                    enable_events=True,
                )
            ],
            [
                sg.Checkbox(
                    "Output zips",
                    tooltip=" Zipping is slow ",
                    key="OUTPUT_ZIPS",
                    default=sg.user_settings_get_entry("output_zips"),
                    enable_events=True,
                )
            ],
            [
                sg.Checkbox(
                    "Play finish sound",
                    tooltip=" Notifies you when the conversion has finished ",
                    key="PLAY_FINISH_SOUND",
                    default=sg.user_settings_get_entry("play_finish_sound"),
                    enable_events=True,
                )
            ],
            [
                sg.Checkbox(
                    "Beautify Lua",
                    tooltip=" Fixes the indentation and much more of Lua files ",
                    key="BEAUTIFY_LUA",
                    default=sg.user_settings_get_entry("beautify_lua"),
                    enable_events=True,
                )
            ],
            [
                sg.Checkbox(
                    "Launch after converting",
                    tooltip=" Launches launch_dev.bat after converting ",
                    key="LAUNCH_AFTER_CONVERT",
                    default=sg.user_settings_get_entry("launch_after_convert"),
                    enable_events=True,
                )
            ],
        ]
    ]


def get_settings_window():
    return sg.Window(
        title="Settings",
        layout=get_settings_window_layout(),
        icon=get_path("Media/legacy-mod-converter.ico"),
        font=("Helvetica", 25),
        finalize=True,
    )
