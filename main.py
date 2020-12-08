# Run: python main.py output
# Build: pyinstaller --noconsole --onefile --icon=media/cclmc-icon.ico --name="Legacy Mod Converter" main.py

from Python import gui

gui.init_window_theme()
gui.run_window(gui.init_window())