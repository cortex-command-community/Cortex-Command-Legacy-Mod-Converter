import os, sys, io, cv2

from PIL import Image


palette = Image.open(os.path.join("Media", "palette.bmp")).getpalette()


def is_input_image(full_filename):
	return full_filename.lower().endswith((".bmp", ".png", ".jpg", ".jpeg")) and full_filename.lower() != "palette.bmp"


def process_image(full_filename, input_image_path, output_image_path):
	global palette

	old_img = get_old_img(input_image_path)

	# scale = 1
	# old_img = old_img.resize((int(old_img.width * scale), int(old_img.height * scale)))

	# # putpalette() always expects 256 * 3 ints.
	# for k in range(256 - int(len(palette) / 3)):
	# 	for j in range(3):
	# 		palette.append(palette[j])

	# palette_img = Image.new('P', (1, 1))
	# palette_img.putpalette(palette)
	# new_img = old_img.convert(mode="RGB").quantize(palette=palette_img, dither=False)

	# new_img.save(os.path.splitext(output_image_path)[0] + ".png")


def get_old_img(input_image_path):
	# This prevents cv2 from printing warnings to the terminal.
	# TODO: Fix the cv2 and PIL bmp reading issue instead of redirecting a warning away from the terminal.
	with suppress_stdout_stderr():
		# A bmp threw an "Unsupported BMP compression (1)" with Image.open(), so we open it in cv2 first.
		# cv2 solution: https://stackoverflow.com/a/52416250/13279557
		# cv2 to PIL:   https://stackoverflow.com/a/43234001/13279557
		# old_img = Image.fromarray(cv2.imread(input_image_path)) # TODO: This may work just as well as the line below for all cases.
		old_img = Image.fromarray(cv2.cvtColor(cv2.imread(input_image_path), cv2.COLOR_BGR2RGB))

	return old_img


# This stackoverflow's question answers itself in the question with the solution to getting rid of "libpng warning: iCCP: known incorrect sRGB profile".
# https://stackoverflow.com/q/11130156/13279557
class suppress_stdout_stderr(object):
    '''
    A context manager for doing a "deep suppression" of stdout and stderr in 
    Python, i.e. will suppress all print, even if the print originates in a 
    compiled C/Fortran sub-function.
    	This will not suppress raised exceptions, since exceptions are printed
    to stderr just before a script exits, and after the context manager has
    exited (at least, I think that is why it lets exceptions through).      

    '''
    def __init__(self):
        # Open a pair of null files
        self.null_fds =  [os.open(os.devnull,os.O_RDWR) for x in range(2)]
        # Save the actual stdout (1) and stderr (2) file descriptors.
        self.save_fds = [os.dup(1), os.dup(2)]

    def __enter__(self):
        # Assign the null pointers to stdout and stderr.
        os.dup2(self.null_fds[0],1)
        os.dup2(self.null_fds[1],2)

    def __exit__(self, *_):
        # Re-assign the real stdout/stderr back to (1) and (2)
        os.dup2(self.save_fds[0],1)
        os.dup2(self.save_fds[1],2)
        # Close all file descriptors
        for fd in self.null_fds + self.save_fds:
            os.close(fd)