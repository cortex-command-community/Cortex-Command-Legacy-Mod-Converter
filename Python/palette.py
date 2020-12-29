import os

from PIL import Image
import cv2


palette = Image.open(os.path.join("Media", "palette.bmp")).getpalette()


def is_input_image(full_filename):
	return full_filename.lower().endswith((".bmp", ".png", ".jpg", ".jpeg")) and full_filename.lower() != "palette.bmp"


def process_image(full_filename, input_image_path, output_image_path):
	global palette

	# A bmp threw an "Unsupported BMP compression (1)" with Image.open(), so we open it in cv2 first.
	# cv2 solution: https://stackoverflow.com/a/52416250/13279557
	# cv2 to PIL:   https://stackoverflow.com/a/43234001/13279557
	# old_img = Image.fromarray(cv2.imread(input_image_path)) # TODO: This may work just as well as the line below for all cases. 
	old_img = Image.fromarray(cv2.cvtColor(cv2.imread(input_image_path), cv2.COLOR_BGR2RGB))

	scale = 1
	old_img = old_img.resize((int(old_img.width * scale), int(old_img.height * scale)))

	# putpalette() always expects 256 * 3 ints.
	for k in range(256 - int(len(palette) / 3)):
		for j in range(3):
			palette.append(palette[j])

	palette_img = Image.new('P', (1, 1))
	palette_img.putpalette(palette)
	new_img = old_img.convert(mode="RGB").quantize(palette=palette_img, dither=False)

	new_img.save(os.path.splitext(output_image_path)[0] + ".png")