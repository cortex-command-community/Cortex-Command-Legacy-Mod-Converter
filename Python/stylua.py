import os, subprocess

from pathlib import Path


from Python import utils


class WronglyFormattedLuaFile(Exception):
	pass


def run(input_folder_path, output_folder_path):
	for name in os.listdir(input_folder_path):
		input_path = input_folder_path / Path(name)
		if not utils.is_mod_folder(input_path):
			continue

		output_path = utils.get_output_path_from_input_path(input_folder_path, output_folder_path, input_path)

		if os.name == "nt": # If the OS is Windows
			stylua_path = utils.path("Lib/stylua/Windows/stylua.exe")
		elif os.name == "posix": # If the OS is Linux
			stylua_path = utils.path("Lib/stylua/Linux/stylua")

		# Setting stdin to subprocess.DEVNULL is necessary for the EXE not to throw "OSError: [WinError 6] The handle is invalid"
		result = subprocess.run([stylua_path, output_path], capture_output=True, text=True, stdin=subprocess.DEVNULL)

		if result.stderr:
			raise WronglyFormattedLuaFile(result.stderr.replace("\n", "\n\n"))
