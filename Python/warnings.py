import os, sys, json, webbrowser
from jsoncomment import JsonComment

from Python import shared_globals as cfg
from Python import convert


WARNINGS_FILENAME = "Warnings.json"
WARNINGS_PATH = os.path.join("ConversionRules", WARNINGS_FILENAME)


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


def load_conversion_and_warning_rules():
	json_parser = JsonComment(json)

	json_files_found = 0
	try:
		for name in os.listdir("ConversionRules"):
			if name.endswith(".json") and name != WARNINGS_FILENAME:
				json_files_found += 1
				with open(os.path.join("ConversionRules", name)) as f:
					convert.conversion_rules.update(json_parser.load(f)) 

		with open(WARNINGS_PATH) as f:
			warning_rules.update(json_parser.load(f))
	except:
		check_github_button_clicked_and_exit(cfg.sg.Popup("The 'ConversionRules' folder wasn't found next to this executable. You can get the missing folder from the Legacy Mod Converter GitHub repo.", title="Missing ConversionRules folder", custom_text="Go to GitHub"))

	if json_files_found == 0:
		check_github_button_clicked_and_exit(cfg.sg.Popup("The 'ConversionRules' folder didn't contain any JSON files. You can get the JSON files from the Legacy Mod Converter GitHub repo.", title="Missing JSON files", custom_text="Go to GitHub"))


def check_github_button_clicked_and_exit(clicked_github_button):
	if clicked_github_button:
		webbrowser.open("https://github.com/cortex-command-community/Cortex-Command-Legacy-Mod-Converter")
	sys.exit()


mod_warnings = None # A global list set in clear_mod_warnings()
def clear_mod_warnings():
	global mod_warnings
	mod_warnings = []


def append_mod_replacement_warning(file_path, line_number, old_str, new_str):
	append_mod_warning(file_path, line_number, f"Replace '{old_str}' with", f"'{new_str}'")


def append_mod_warning(file_path, line_number, error, error_subject):
	global mod_warnings
	warning = f"\nLine {line_number} at {file_path}\n\t{error}: {error_subject}"
	mod_warnings.append(warning)


def prepend_mod_title(mod_name):
	title = "\n" + "\n".join(
		(WARNINGS_MOD_NAME_SEPARATOR, f"\t{mod_name}", WARNINGS_MOD_NAME_SEPARATOR)
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