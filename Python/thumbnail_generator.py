from math import ceil

from PIL import Image
from pathlib import Path

from Python import shared_globals as cfg


def generate_thumbnail(iconfile_relative_path_str, output_folder_path):
	"""
	Almost all mods have a ModuleIcon.bmp, and sometimes a Preview.bmp
	The Preview.bmp is often bigger and prettier than the ModuleIcon.bmp,
	but because it isn't always available it won't be used here.

	mod.io's preview image tips state:
	- 1280x720 or larger recommended
	- 16:9 aspect ratio recommended

	How to scale a 23x23 ModuleIcon.bmp:
	1. Scale the entire image by ceil(720 / 23)
	2. Add transparency on the sides so the width is AT LEAST (16/9) times the new height.
	   It's fine if it's way wider, as mod.io cuts off the sides of the image if it's too wide.
	"""
	iconfile_path = output_folder_path / Path(iconfile_relative_path_str)
	thumbnail = Image.open(iconfile_path).convert("RGBA")

	pixdata = thumbnail.load()

	width, height = thumbnail.size

	replace_pink_with_transparency(pixdata, width, height)

	thumbnail = resize_height_to_720p(thumbnail, width, height)

	# thumbnail = add_transparent_sides(thumbnail)

	thumbnail_path = iconfile_path.parent / "thumbnail.png"
	thumbnail.save(thumbnail_path)


def replace_pink_with_transparency(pixdata, width, height):
	"""
	Replaces the CCCP pink background with real alpha transparency.
	"""
	for y in range(height):
		for x in range(width):
			if pixdata[x, y][:3] == (255, 0, 255):
				pixdata[x, y] = (0, 0, 0, 0)


def resize_height_to_720p(base_img, base_width, base_height):
	"""
	mod.io's preview image tips state "1280x720 or larger recommended"
	Source of the code: https://stackoverflow.com/a/451580/13279557
	"""
	minimum_height = 720

	scale_factor = ceil(minimum_height / base_height)

	new_width  = base_width * scale_factor
	new_height = base_height * scale_factor

	# print(scale_factor, base_width, base_height, new_width, new_height)

	new_img = base_img.resize( (new_width,new_height), Image.NEAREST)
	return new_img


# def add_transparent_sides(base_img):
#     image = image.convert('RGBA')
#     width, height = image.size
#     new_width = 512
#     new_height = new_width * height // width
#     image = image.resize((new_width, new_height), resample=Image.ANTIALIAS)
#     new_image = Image.new('RGBA', (512, 512), (0, 0, 0, 0))
#     upper = (512 - image.size[1]) // 2
#     new_image.paste(image, (0, upper))
#     return new_image
