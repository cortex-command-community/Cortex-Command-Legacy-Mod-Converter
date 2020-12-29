import os

import numpy as np
from PIL import Image

def load_vips_env():
    vipshome = 'c:\\vips-dev-8.10\\bin'
    os.environ['PATH'] = vipshome + ';' + os.environ['PATH']

load_vips_env()

import pyvips

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

get_old_img("input.bmp").show()