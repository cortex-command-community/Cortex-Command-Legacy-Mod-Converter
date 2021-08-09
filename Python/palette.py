import os

from pathlib import Path
from PIL import Image


def is_bmp(full_filename):
	return Path(full_filename).suffix.lower() == ".bmp"


def bmp_to_png(input_image_path, output_image_path):
	# This converts an indexed BMP to an RGB PNG unfortunately.
	# image = cv2.imread(input_image_path)
	# cv2.imwrite(str(output_image_path), image)
	# print(output_image_path)
	Image.open(input_image_path).save(output_image_path)