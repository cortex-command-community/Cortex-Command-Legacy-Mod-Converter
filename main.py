# Run manually: python main.py

# Build exe not from spec: pyinstaller --noconsole --onefile --icon=Media/cclmc-icon.ico --add-data "Media/github-icon.png;Media" --add-data "Media/discord-icon.png;Media" --add-data "Media/finish.wav;Media" --add-data "ConversionRules;ConversionRules" --name="Legacy Mod Converter" main.py
# Build exe from spec (can be outdated): pyinstaller "Legacy Mod Converter.spec"

from Python import gui

gui.init_window_theme()
gui.run_window(gui.init_window())