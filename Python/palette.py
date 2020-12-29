import os, sys, io

import numpy as np
from PIL import Image


def load_vips_env():
	# pyvips from pip doesn't seem to work, unzip the latest vips-dev-w64-all.zip instead from https://github.com/libvips/libvips/releases.
	vipshome = 'c:\\vips-dev-8.10\\bin'
	os.environ['PATH'] = vipshome + ';' + os.environ['PATH']

load_vips_env()

import pyvips


# TODO: Move to shared_globals.py
def resource_path(relative_path):
	if hasattr(sys, '_MEIPASS'):
		return os.path.join(sys._MEIPASS, relative_path)
	return os.path.join(os.path.abspath("."), relative_path)


palette = Image.open(resource_path(os.path.join("Media", "palette.bmp"))).getpalette()


def is_input_image(full_filename):
	return full_filename.lower().endswith((".bmp", ".png", ".jpg", ".jpeg")) and full_filename.lower() != "palette.bmp"


def process_image(full_filename, input_image_path, output_image_path):
	global palette

	old_img = get_old_img(input_image_path)

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


def get_old_img(input_image_path):
	# pyvips acts as a substitute for PIL and cv2, because both of those can throw a warning in the terminal with RLE bmps.
	pyvips_img = pyvips.Image.new_from_file(input_image_path, access='sequential')
	np_img = vips2numpy(pyvips_img)
	return Image.fromarray(np.uint8(np_img))


format_to_np_dtype = {
    'uchar': np.uint8,
    'char': np.int8,
    'ushort': np.uint16,
    'short': np.int16,
    'uint': np.uint32,
    'int': np.int32,
    'float': np.float32,
    'double': np.float64,
    'complex': np.complex64,
    'dpcomplex': np.complex128,
}


def vips2numpy(vi):
	return np.ndarray(buffer=vi.write_to_memory(),
						dtype=format_to_np_dtype[vi.format],
						shape=[vi.height, vi.width, vi.bands])