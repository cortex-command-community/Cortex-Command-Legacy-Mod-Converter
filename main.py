# Run manually: python main.py
# Build EXE for CCCP: pyinstaller --onefile --icon=Media/cclmc-icon.ico --add-data="Media/github-icon.png;Media" --add-data="Media/discord-icon.png;Media" --add-data="Media/finish.wav;Media" --name="Legacy Mod Converter" main.py

from Python import gui

gui.init_window_theme()
gui.run_window(gui.init_window())