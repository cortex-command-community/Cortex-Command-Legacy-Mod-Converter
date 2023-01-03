import os, webbrowser
import PySimpleGUI as sg
from pathlib import Path
from threading import Thread

from Python import shared_globals as cfg
from Python import convert
from Python import warnings
from Python.progress_bar import ProgressBar

from Python.gui import gui_windows


def init_window_theme():
    path_set_color = "#528b30"
    progress_bar_color = "#17569c"

    sg.theme("DarkGrey14")
    sg.theme_input_background_color(path_set_color)
    sg.theme_progress_bar_color((progress_bar_color, sg.theme_progress_bar_color()[1]))
    sg.theme_button_color((sg.theme_text_color(), "#2a3948"))


def init_settings():
    sg.user_settings_filename(filename="settings.json", path=".")

    if not os.path.isfile(sg.user_settings_filename()):
        sg.Popup(
            "This is a tool that allows you to convert legacy (old) mods to the latest version of CCCP.\n\nYou can get more information from the GitHub repository and the Discord server by clicking their corresponding icons in the bottom-right corner after pressing OK.",
            title="Welcome",
            custom_text=" OK ",
        )

    cfg.sg = sg

    warnings.load_conversion_and_warning_rules()  # TODO: Why is this called in this GUI function?

    default_settings_to_true(["play_finish_sound", "beautify_lua"])


def default_settings_to_true(settings_to_default_to_true):
    for setting_to_default_to_true in settings_to_default_to_true:
        play_finish_sound_setting = sg.user_settings_get_entry(
            setting_to_default_to_true
        )
        sg.user_settings_set_entry(
            setting_to_default_to_true,
            True if play_finish_sound_setting == None else play_finish_sound_setting,
        )


def is_part_of_cccp_folder(cccp_folder):
    if not cccp_folder.exists():
        return False

    while cccp_folder and cccp_folder.name != "":
        for entry in cccp_folder.iterdir():
            if entry.is_file() and "Cortex Command" in entry.name:
                sg.user_settings_set_entry("cccp_folder", str(cccp_folder))
                return True

        cccp_folder = cccp_folder.parent

    return False


def run_window():
    main_window = gui_windows.get_main_window()
    settings_window = None

    cfg.progress_bar = ProgressBar(
        main_window["PROGRESS_BAR"], main_window["PROGRESS_BAR_TEXT"]
    )

    valid_cccp_path = True if sg.user_settings_get_entry("cccp_folder") else False

    while True:
        window, event, values = sg.read_all_windows()

        if event == "Exit" or event == sg.WIN_CLOSED:
            window.close()
            if window == main_window:
                break
            if window == settings_window:
                settings_window = None
                main_window.Enable()
                main_window.BringToFront()

        elif event == "CCCP_FOLDER":
            cccp_folder = Path(values[event])

            if is_part_of_cccp_folder(cccp_folder):
                valid_cccp_path = True
                window[event](background_color=sg.theme_input_background_color())
                window[event](value=sg.user_settings_get_entry("cccp_folder"))
            else:
                valid_cccp_path = False
                window[event](background_color=cfg.NO_PATH_SET_COLOR)

        elif event == "LAUNCH_SETTINGS_WINDOW" and settings_window == None:
            settings_window = gui_windows.get_settings_window()
            main_window.Disable()

        elif event in (
            "SKIP_CONVERSION",
            "OUTPUT_ZIPS",
            "PLAY_FINISH_SOUND",
            "BEAUTIFY_LUA",
            "LAUNCH_AFTER_CONVERT",
        ):
            value = values[event]
            sg.user_settings_set_entry(event.lower(), value)

        elif event == "CONVERT":
            if valid_cccp_path:
                cfg.progress_bar.setTitle("Starting...")
                cfg.progress_bar.reset()
                lock_convert_button()
                # Run on a separate thread, don't lock up the UI.
                t = Thread(target=convert.convert_all)
                t.start()

        elif event == "GITHUB":
            webbrowser.open(
                "https://github.com/cortex-command-community/Cortex-Command-Legacy-Mod-Converter"
            )
        elif event == "DISCORD":
            webbrowser.open("https://discord.gg/TSU6StNQUG")


def unlock_convert_button():
    gui_windows.get_main_window()["CONVERT"].update(disabled=False)


def lock_convert_button():
    gui_windows.get_main_window()["CONVERT"].update(disabled=True)
