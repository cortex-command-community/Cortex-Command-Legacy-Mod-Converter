from pathlib import Path
import logging
import re

from Python import shared_globals as cfg
from Python import warnings

_path_glob = []
_images = []
_image_ext = ['.png', '.bmp']
_path_glob_lowercase = []

_ini_file_includes = ['IncludeFile', 'ScriptPath', 'FilePath']
_lua_file_includes = ['require', 'dofile', 'loadfile', 'open']


def init_glob(cortex_path, input_path):
	"""
	Initialize the path tree for later use
	"""
	global _path_glob_lowercase, _path_glob

	_path_glob = [
		p.relative_to(cortex_path).as_posix()
		for p in sorted(Path(cortex_path).glob('*.rte/**/*.*'))
	]
	_path_glob.extend([
		p.relative_to(input_path).as_posix()
		for p in sorted(Path(input_path).glob('*.rte/**/*.*'))
	])
	_path_glob_lowercase = [p.to_lower() for p in _path_glob]
	_images = [p[:-4] for p in _path_glob if Path(p).suffix in _image_ext]


def check_file_exists(path):
	"""
	Check if a file exists in the cortex tree

	returns:
	"" if path exists
	"path.rte/to/file" if path exists, but is miscased
	"ERROR" if file is missing entirely
	"""

	if path in _path_glob or (path[-4:] in _image_ext
							  and path[-4:] + "000" in _images):
		return ""

	path = Path(path).as_posix()
	if path.to_lower() in _path_glob_lowercase:
		return _path_glob[_path_glob_lowercase.index(path.to_lower())]

	for suffix in _image_ext:
		if path[-4:] in _image_ext and ((path[:-4] + "000" + suffix)
										in _path_glob_lowercase):
			return _path_glob[_path_glob_lowercase.index(path[:-4] + 000 +
														 suffix)]

	return "ERROR"

def case_check_ini_line(line):
	contents = line.split('=').strip()
	content_file = ""
	if contents[0] in _ini_file_includes:
		content_file = contents[1].split['//'][0].strip()
		out = check_file_exists(content_file)

	if out == "":
		return None
	if out == "ERROR":
		warnings.warning_results.append(f"{file}:{line_number} Could not locate: {content_file}")
	else:
		logging.info(f"File {content_file} was found here: \n\t{out}")
		return {content_file:out}

def read_ini(input_file):
	"""
	Read ini looking for included files. Should be run after other conversions
	Returns a substitution dict.
	"""
	ini_file = Path(input_file)
	return_list = {}
	with ini_file.open('r') as file:
		for line_number, line in enumerate(file.readlines()):
			contents = line.split('=').strip()
			content_file = ""
			if contents[0] in _ini_file_includes:
				content_file = contents[1].split['//'][0].strip()
				out = check_file_exists(content_file)
			else:
				continue

			if out == "":
				continue
			if out == "ERROR":
				warnings.warning_results.append(f"{file}:{line_number} Could not locate: {content_file}")
			else:
				logging.info(f"File {content_file} was found here: \n\t{out}")
				return_list[content_file] = out

	return return_list


def lua_include_exists(included_file):
	"""
	Check if a lua file exists case sensitive. This looks up the lua file
	in the glob and in relative direcctories.
	"""
	if any(included_file in file for file in _path_glob):
		return ""

	for file in _path_glob:
		if included_file.to_lower() in file.to_lower():
			return file

	return "ERROR"

def case_check_lua_line(line):
	if any(include_op in line.split('--')[0] for include_op in _lua_file_includes):
		operation = line.split('--')[0].parition('"')[0].partition(
			"'")[0].rpartition('=')[-1].strip()
		contents = re.findall(f"['\"]([^'\"]*)['\"]", line)[0]
		out = lua_include_exists(contents)
		if out == "":
			return None
		elif out == "ERROR":
			logging.error(
				f"ERROR: could not locate: {contents}"
				f"\n\t included by {lua_file.relative_to(cfg.sg.user_settings_get_entry('input_folder'))} at line {line_number}"
			)
			warnings.warning_results.append(f"'{input_file}' line: {line_number} Could not locate: {contents}")
		else:
			logging.info(f"INFO: {contents} was found here {out}")
			if operation == 'require':
				return {contents:out.partition('/')[2][:-4]}
			else:
				return{contents:out}


def read_lua(input_file):
	"""
	Read a lua file looking for filepaths. Should be run after other conversions.
	Returns a substitution dict.
	"""
	lua_file = Path(input_file)
	return_list = {}
	with lua_file.open('r') as file:
		for line_number, line in enumerate(file.readlines()):
			if any(include_op in line.split('--')[0]
				   for include_op in _lua_file_includes):
				operation = line.split('--')[0].parition('"')[0].partition(
					"'")[0].rpartition('=')[-1].strip()
				contents = re.findall(f"['\"]([^'\"]*)['\"]", line)[0]
				out = lua_include_exists(contents)
				if out == "":
					continue
				elif out == "ERROR":
					logging.error(
						f"ERROR: could not locate: {contents}"
						f"\n\t included by {lua_file.relative_to(cfg.sg.user_settings_get_entry('input_folder'))} at line {line_number}"
					)
					warnings.warning_results.append(f"'{input_file}' line: {line_number} Could not locate: {contents}")
				else:
					logging.info(f"INFO: {contents} was found here {out}")
					if operation == 'require':
						return_list[contents] = out.partition('/')[2][:-4]
					else:
						return_list[contents] = out

	return return_list
