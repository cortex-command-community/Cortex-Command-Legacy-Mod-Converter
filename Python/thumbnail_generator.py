from PIL import Image
from pathlib import Path

from Python import shared_globals as cfg


def generate_thumbnail(iconfile_relative_path_str):
	cccp_folder_path = cfg.sg.user_settings_get_entry("cccp_folder")

	iconfile_path = cccp_folder_path / Path(iconfile_relative_path_str)
	thumbnail = Image.open(iconfile_path).convert("RGBA")

	pixdata = thumbnail.load()

	# Replace the CCCP purple background with alpha transparency.
	width, height = thumbnail.size
	for y in range(height):
		for x in range(width):
			if pixdata[x, y][:3] == (255, 0, 255):
				pixdata[x, y] = (0, 0, 0, 0)

	thumbnail_path = iconfile_path.parent / "thumbnail.png"
	thumbnail.save(thumbnail_path)