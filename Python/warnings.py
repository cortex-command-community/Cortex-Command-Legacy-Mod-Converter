import os, sys, json, webbrowser
from jsoncomment import JsonComment

from Python import shared_globals as cfg
from Python import convert


warnings_file_name = "Warnings.json"
warnings_path = os.path.join("ConversionRules", warnings_file_name)
warnings_available = os.path.isfile(warnings_path)

warning_rules = {}

MANUAL_REPLACEMENT_TITLE_SEPARATOR = "=" * 50
warning_results = [
	MANUAL_REPLACEMENT_TITLE_SEPARATOR +
	"\nLINES REQUIRING MANUAL REPLACEMENT\n" +
	MANUAL_REPLACEMENT_TITLE_SEPARATOR + "\n"
]


def load_conversion_and_warning_rules():
	json_parser = JsonComment(json)

	json_files_found = 0
	try:
		for name in os.listdir("ConversionRules"):
			if name.endswith(".json") and name != warnings_file_name:
				json_files_found += 1
				with open(os.path.join("ConversionRules", name)) as f:
					convert.conversion_rules.update(json_parser.load(f)) 
		if warnings_available:
			with open(warnings_path) as f:
				warning_rules.update(json_parser.load(f))
	except:
		check_github_button_clicked_and_exit(cfg.sg.Popup("The 'ConversionRules' folder wasn't found next to this executable. You can get the missing folder from the Legacy Mod Converter GitHub repo.", title="Missing ConversionRules folder", custom_text="Go to GitHub"))

	if json_files_found == 0:
		check_github_button_clicked_and_exit(cfg.sg.Popup("The 'ConversionRules' folder didn't contain any JSON files. You can get the JSON files from the Legacy Mod Converter GitHub repo.", title="Missing JSON files", custom_text="Go to GitHub"))


def check_github_button_clicked_and_exit(clicked_github_button):
	if clicked_github_button:
		webbrowser.open("https://github.com/cortex-command-community/Cortex-Command-Legacy-Mod-Converter")
	sys.exit()


def warnings_popup():
	if warnings_available:
		message = "\n".join(warning_results)

		w = max(30, len(max(message.split("\n"), key=len)) + 1)
		h = min(50, len(message.splitlines()) + 1) # + 1 is necessary, because popup_scrolled always adds an empty line at the bottom.

		cfg.sg.popup_scrolled(message, title="Lines requiring manual replacement", size=(w, h), button_color=cfg.sg.theme_button_color(), background_color=cfg.sg.theme_background_color())