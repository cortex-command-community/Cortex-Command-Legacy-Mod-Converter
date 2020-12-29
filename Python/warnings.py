import os, sys, json
from jsoncomment import JsonComment

from Python import shared_globals as cfg
from Python import convert


warnings_file_name = "Warnings.json"
warnings_path = os.path.join("ConversionRules", warnings_file_name)
warnings_available = os.path.isfile(warnings_path)

warning_rules = {}
warning_results = []


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
		w = max(30, len(max(warning_results, key=len)))
		h = min(50, len(warning_results)) + 1 # + 1 necessary because popup_scrolled adds an extra line.
		cfg.sg.popup_scrolled("\n".join(warning_results), title="Lines needing manual replacing", size=(w, h), button_color=cfg.sg.theme_button_color(), background_color=cfg.sg.theme_background_color())