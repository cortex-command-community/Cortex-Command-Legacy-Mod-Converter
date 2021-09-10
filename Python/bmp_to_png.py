import os
from PIL import Image
from pathlib import Path
import numpy as np

from Python import shared_globals as cfg


def is_bmp(full_filename):
	return Path(full_filename).suffix.lower() == ".bmp"


def get_bmp_compression_method(img):
	img.seek(0x1E)
	return int.from_bytes(img.read(4), byteorder="little")


def is_bmp_rle8_compressed(img):
	return get_bmp_compression_method(img) == 1


def get_bmp_pixel_index_array_offset(img):
	img.seek(0xA)
	# Start of the rle8.bmp example's pixel array: 08 00 03 F8
	return int.from_bytes(img.read(4), byteorder="little")


def get_bmp_pixel_index_array_byte_size(img):
	img.seek(0x22)
	return int.from_bytes(img.read(4), byteorder="little")


def get_bmp_width(img):
	img.seek(0x12)
	return int.from_bytes(img.read(2), byteorder="little")


def get_bmp_height(img):
	img.seek(0x16)
	return int.from_bytes(img.read(2), byteorder="little")


# See the MS docs for more information on how the BI_RLE8 decoding works:
# https://docs.microsoft.com/en-us/windows/win32/gdi/bitmap-compression
def get_decoded_pixel_index_array(rle_bytes, width, height):
	decompressed = [[] for _ in range(height)]

	byte_index = -1
	x = -1 # Tracking the x value in case of delta bytes.
	y = height - 1

	while True:
		run_even = True

		byte_index += 1
		byte = rle_bytes[byte_index] # Get the first byte.

		if byte == 0:
			byte_index += 1
			special_byte = rle_bytes[byte_index] # Get the second byte.

			if special_byte == 0: # End of line.
				# print(f"End of line at {x, y}, added {width - x - 1} times 0.")

				# Makes sure that the 2D array keeps a homogeneous shape. Assumes the palette's first color represents transparency.
				for _ in range(width - x - 1):
					decompressed[y].append(0)

				x = -1
				y -= 1
			elif special_byte == 1: # End of bitmap.
				# print(f"End of bitmap at {x, y}.")

				# Makes sure that the 2D array keeps a homogeneous shape. Assumes the palette's first color represents transparency.
				if x != -1 and y != -1: # If the file ends with "00 00 00 01" then the special_byte == 0 if-case will mess up the below for-loop.
					# print("Filling the last empty pixels in this row with {} times 0.")
					for _ in range(width - x - 1):
						x += 1
						decompressed[y].append(0)

					# print("Adding rows of 0.")
					for _ in range(y * width):
						if x == width - 1:
							x = -1
							y -= 1

						x += 1
						# print(x, y)
						decompressed[y].append(0)

				return decompressed
			elif special_byte == 2: # Delta. The 2 bytes following the escape contain unsigned values indicating the offset to the right and up of the next pixel from the current position.
				byte_index += 1
				offset_x = rle_bytes[byte_index]
				byte_index += 1
				offset_y = rle_bytes[byte_index]

				# When there's an end-of-line and a delta afterwards, the RLE8 delta's offsets are from before the end-of-line (x, y) movement
				# of going all the way to the left and up one is applied. 
				if x == -1:
					x = width - 1
					y = y + 1
				# print((x, y), (x, y), (offset_x, offset_y))

				for _ in range(offset_x):
					if x == width - 1:
						x = -1
						y -= 1

					x += 1
					decompressed[y].append(0)

				for _ in range(offset_y * width): # TODO: Does this work when offset_y > 1?
					if x == width - 1:
						x = -1
						y -= 1

					x += 1
					decompressed[y].append(0)

					# if y == 71:
					# 	print(f"Vertically placed 0 at {x, y}.")

				if x == width - 1:
					x = -1
					y -= 1
			else: # Called "absolute mode" in the MS Docs.
				following = special_byte

				for _ in range(following):
					x += 1
					byte_index += 1
					palette_index = rle_bytes[byte_index]
					decompressed[y].append(palette_index)
					run_even = not run_even

			# Adding padding so each run has an even number of bytes.
			if not run_even:
				byte_index += 1

		else: # Called "encoded mode" in the MS Docs.
			repeat = byte

			byte_index += 1
			palette_index = rle_bytes[byte_index]

			for _ in range(repeat):
				x += 1
				decompressed[y].append(palette_index)


def get_pixel_index_array_bytes(img):
	pixel_index_array_offset = get_bmp_pixel_index_array_offset(img)
	pixel_index_array_byte_size = get_bmp_pixel_index_array_byte_size(img)

	img.seek(pixel_index_array_offset)
	return img.read(pixel_index_array_byte_size)


def get_pixel_array(img, width, height, palette):
	pixel_index_array_bytes = get_pixel_index_array_bytes(img)
	decoded_pixel_index_array = get_decoded_pixel_index_array(pixel_index_array_bytes, width, height)

	# for index, row in enumerate(decoded_pixel_index_array):
	# 	print(index, len(row))
	# print("")
	# print(len(decoded_pixel_index_array[71]), decoded_pixel_index_array[71])
	# print("")
	
	# TODO: Raise a custom ValueError exception for:
	#       "ValueError: setting an array element with a sequence. The requested array has an inhomogeneous shape after 1 dimensions. The detected shape was (143,) + inhomogeneous part."
	numpy_pixel_index_array = np.array(decoded_pixel_index_array, dtype="uint8")
	return numpy_pixel_index_array

def get_palette(img):
	img.seek(0x36)
	# TODO: This program won't work for BMPs with palettes that don't have an alpha layer, or that don't have exactly 256 palette colors.
	palette = list(img.read(4 * 256))
	del palette[3::4] # Removes the alpha values.

	# Swaps the R and B values.
	palette[0:-2:3], palette[2::3] = palette[2::3], palette[0:-2:3]

	return palette


def convert_rle8_bmp_to_png(img, input_filepath, output_filepath):
	width = get_bmp_width(img)
	height = get_bmp_height(img)

	palette = get_palette(img)
	
	pixel_array = get_pixel_array(img, width, height, palette)
	
	img = Image.fromarray(pixel_array, mode="P")
	img.putpalette(palette)

	img.save(output_filepath)


def bmp_to_png(input_filepath, output_filepath):
	with open(input_filepath, "rb") as img:
		if is_bmp_rle8_compressed(img):
			convert_rle8_bmp_to_png(img, input_filepath, output_filepath)
		else:
			Image.open(input_filepath).save(output_filepath)


def change_bmp_to_png_name(line):
	if not any(skipped_filename in line for skipped_filename in ("palette.bmp", "palettemat.bmp")) and not cfg.sg.user_settings_get_entry("skip_conversion"):
		return line.replace(".bmp", ".png")
	else:
		return line