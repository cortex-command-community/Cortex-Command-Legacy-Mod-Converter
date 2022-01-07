import os, sys, json, webbrowser
from json.decoder import JSONDecodeError
from pathlib import Path

from Python import shared_globals as cfg
from Python import convert


warning_rules = {} # A global that's initialized in load_conversion_and_warning_rules()


MANUAL_REPLACEMENT_TITLE_SEPARATOR = "=" * 50
mods_warnings = None # A global list set in init_mods_warnings()

def init_mods_warnings():
	global mods_warnings
	mods_warnings = [
		"\n".join(
			(MANUAL_REPLACEMENT_TITLE_SEPARATOR, "LINES REQUIRING MANUAL REPLACEMENT", MANUAL_REPLACEMENT_TITLE_SEPARATOR)
		)
	]


FRESH_CONVERSION_RULES_REMINDER = "You can get a fresh Conversion Rules folder by redownloading the Legacy Mod Converter from its GitHub repository with the below button."


def load_conversion_and_warning_rules():
	try:
		for folder_path, subfolders, subfiles in os.walk("Conversion Rules"):
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
		check_github_button_clicked_and_exit(cfg.sg.Popup(f"Error at path '{p}':\n{e}\n\nThis means the 'Conversion Rules' folder couldn't be read, because it contained a wrongly formatted JSON file, which is often caused by a missing comma at the end of a rule.\n\n{FRESH_CONVERSION_RULES_REMINDER}", title="Malformed Conversion Rules", custom_text="Go to the GitHub repository"))

	if len(warning_rules) == 0 and len(convert.conversion_rules) == 0:
		check_github_button_clicked_and_exit(cfg.sg.Popup(f"The 'Conversion Rules' folder doesn't contain any JSON files.\n\n{FRESH_CONVERSION_RULES_REMINDER}", title="Missing JSON files", custom_text="Go to the GitHub repository"))


def check_github_button_clicked_and_exit(clicked_github_button):
	if clicked_github_button:
		webbrowser.open("https://github.com/cortex-command-community/Cortex-Command-Legacy-Mod-Converter")
	sys.exit()


mod_warnings = None # A global list set in clear_mod_warnings()
def clear_mod_warnings():
	global mod_warnings
	mod_warnings = []


def append_mod_replacement_warnings(line, file_path, line_number):
	for old_str, new_str in warning_rules.items():
		if old_str in line:
			append_mod_replacement_warning(file_path, line_number, old_str, new_str)


def append_mod_replacement_warning(file_path, line_number, old_str, new_str):
	append_mod_warning(file_path, line_number, f"Replace '{old_str}' with", f"'{new_str}'")


def append_mod_warning(file_path, line_number, error, error_subject):
	global mod_warnings
	warning = f"\nLine {line_number} at {file_path}\n\t{error}: {error_subject}"
	mod_warnings.append(warning)


def prepend_mod_title(mod_name):
	title = "\n" + "\n".join(
		(cfg.WARNINGS_MOD_NAME_SEPARATOR, f"\t{mod_name}", cfg.WARNINGS_MOD_NAME_SEPARATOR)
	)
	mod_warnings.insert(0, title)


def push_mod_warnings():
	global mod_warnings
	mods_warnings.extend(mod_warnings)


def show_popup_if_necessary():
	if len(mods_warnings) > 1: # mods_warnings is initialized with a first line, so mods_warnings starts with a len of 1.
		warnings_popup()


def warnings_popup():
	message = "\n".join(mods_warnings)

	w = max(
		30,
		len(get_longest_line_length(message)) + 1 # TODO: Add a comment here on why + 1 is necessary.
	)
	h = min(
		50,
		len(message.splitlines()) + 1 # + 1 is necessary, because popup_scrolled always adds an empty line at the bottom.
	)

	cfg.sg.popup_scrolled(
		message,
		title="Lines requiring manual replacement",
		size=(w, h),
		button_color=cfg.sg.theme_button_color(),
		background_color=cfg.sg.theme_background_color(),
	)


def get_longest_line_length(message):
	return max(message.split("\n"), key=len)