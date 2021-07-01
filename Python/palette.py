import os, sys, io

import numpy as np
from PIL import Image

from Python import utils


def load_vips_env():
	# "import pyvips" doesn't work, so I unzipped the latest vips-dev-w64-all.zip and put it in "Libs/".
	# https://github.com/libvips/libvips/releases
	vipshome = "Libs/vips-dev-8.10/bin"
	os.environ["PATH"] = vipshome + ";" + os.environ["PATH"]

load_vips_env()

import pyvips


regular_palette = Image.open(utils.resource_path(os.path.join("Media", "palette.bmp"))).getpalette()


def is_input_image(full_filename):
	return full_filename.lower().endswith((".bmp", ".png", ".jpg", ".jpeg")) and full_filename.lower() not in ("regular_palette.bmp")


def process_image(full_filename, input_image_path, output_image_path):
	global regular_palette

	old_img = get_old_img(input_image_path, test=full_filename)

	# old_img.save(full_filename)

	# print(old_img.palette)

	palette_img = Image.new('P', (1, 1))
	palette_img.putpalette(regular_palette)
	new_img = old_img.convert(mode="RGB").quantize(palette=palette_img, dither=False)

	new_img.save(os.path.splitext(output_image_path)[0] + ".png")


def get_old_img(input_image_path, test):
	# pyvips acts as a substitute for PIL and cv2, because both of those can throw a warning in the terminal with RLE bmps.
	pyvips_img = pyvips.Image.new_from_file(input_image_path, access='sequential')
	# print(dir(pyvips_img), "\n")
	# print(pyvips_img)
	# pyvips_img.write_to_file(test)
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