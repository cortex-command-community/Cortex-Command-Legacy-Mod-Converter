import os, sys, json, webbrowser
from json.decoder import JSONDecodeError
from pathlib import Path

from Python import shared_globals as cfg
from Python import convert


MANUAL_REPLACEMENT_TITLE_SEPARATOR = "=" * 50

mods_warnings = []

FRESH_CONVERSION_RULES_REMINDER = "You can get a fresh ConversionRules folder by redownloading the Legacy Mod Converter from its GitHub repository with the below button."


warning_rules = {}


def load_conversion_and_warning_rules():
    try:
        for folder_path, subfolders, subfiles in os.walk("ConversionRules"):
            for filename in subfiles:
                p = folder_path / Path(filename)

                if p.is_file() and p.suffix.lower() == ".json":
                    with open(p) as f:
                        json_string = json.load(f)

                        if p.stem == "Warnings":
                            warning_rules.update(json_string)
                        else:
                            convert.conversion_rules.update(json_string)
    except JSONDecodeError as e:
        check_github_button_clicked_and_exit(
            cfg.sg.Popup(
                f"Error at path '{p}':\n{e}\n\nThis means the 'ConversionRules' folder couldn't be read, because it contained a wrongly formatted JSON file, which is often caused by a missing comma at the end of a rule.\n\n{FRESH_CONVERSION_RULES_REMINDER}",
                title="Malformed ConversionRules",
                custom_text="Go to the GitHub repository",
            )
        )

    if len(warning_rules) == 0 and len(convert.conversion_rules) == 0:
        check_github_button_clicked_and_exit(
            cfg.sg.Popup(
                f"The 'ConversionRules' folder doesn't contain any JSON files.\n\n{FRESH_CONVERSION_RULES_REMINDER}",
                title="Missing JSON files",
                custom_text="Go to the GitHub repository",
            )
        )


def check_github_button_clicked_and_exit(clicked_github_button):
    if clicked_github_button:
        webbrowser.open(
            "https://github.com/cortex-command-community/Cortex-Command-Legacy-Mod-Converter"
        )
    sys.exit()


def append_mod_replacement_warnings(line, file_path, line_number):
    for old_str, new_str in warning_rules.items():
        if old_str in line:
            append_mod_warning(file_path, line_number, f'"{old_str}"', new_str)


def append_mod_warning(file_path, line_number, error, error_subject):
    global mods_warnings
    warning = f"\nLine {line_number} at {file_path}\n\t{error}: {error_subject}"
    mods_warnings.append(warning)


def show_popup_if_necessary():
    if len(mods_warnings) > 0:
        warnings_popup()


def warnings_popup():
    message = (
        f"{MANUAL_REPLACEMENT_TITLE_SEPARATOR}\nLINES REQUIRING MANUAL REPLACEMENT\n{MANUAL_REPLACEMENT_TITLE_SEPARATOR}\n"
        + "\n".join(mods_warnings)
    )

    w = max(
        30,
        len(
            get_longest_line(message)
        ),  # Can't divide by two or anything because the line wrapping will cause the height of the window to be wrong, making user have to scroll.
    )
    h = min(
        50,
        len(message.splitlines())
        + 1,  # + 1 is necessary, because popup_scrolled always adds an empty line at the bottom.
    )

    cfg.sg.popup_scrolled(
        message,
        title="Lines requiring manual replacement",
        size=(w, h),
        button_color=cfg.sg.theme_button_color(),
        background_color=cfg.sg.theme_background_color(),
    )


def get_longest_line(message):
    return max(message.split("\n"), key=len)
