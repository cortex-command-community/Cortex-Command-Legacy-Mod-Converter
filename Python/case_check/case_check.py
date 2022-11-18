from pathlib import Path
import re

from Python.case_check.case_check_errors import error_could_not_locate, error_failed_to_find_module


_path_glob = []
_path_glob_lowercase = []
_modules = []

_images = None
_image_ext = [".png", ".bmp"]

_ini_file_includes = ["IncludeFile", "ScriptPath", "FilePath", "Path", "ScriptFile"]
_lua_file_includes = ["require", "dofile", "loadfile", "io.open"]


def init_glob(cccp_path, input_path):
	"""
	Initialize the path tree for later use
	"""
	global _path_glob_lowercase, _path_glob, _images, _modules

	_path_glob = [
		p.relative_to(cccp_path).as_posix()[:-len(p.suffix)] + p.suffix.lower()
		for p in sorted(Path(cccp_path).glob("*.rte/**/*.*"))
	]
	_path_glob.extend([
		p.relative_to(input_path).as_posix()[:-len(p.suffix)] + p.suffix.lower()
		for p in sorted(Path(input_path).glob("*.rte/**/*.*"))
	])
	# print(_path_glob)
	_path_glob_lowercase = [p.lower() for p in _path_glob]
	_modules = [p.relative_to(cccp_path).as_posix() for p in sorted(Path(cccp_path).glob("*.rte"))]
	_modules.extend([
		p.relative_to(input_path).as_posix()
		for p in sorted(Path(input_path).glob("*.rte"))
	])
	_images = [p[:-4] for p in _path_glob if Path(p).suffix in _image_ext]


def case_check(all_lines, input_file_path, output_file_path):
	file_case_match = {}

	for line_number, line in enumerate(all_lines.split("\n"), start=1):
		# lua and ini separately because of naming differences especially for animations and lua "require"
		if Path(input_file_path).suffix == ".ini":
			# Output file name because line numbers may differ between input and output
			file_case_match.update(case_check_ini_line(line, output_file_path, line_number))
		elif Path(input_file_path).suffix == ".lua":
			file_case_match.update(case_check_lua_line(line, output_file_path, line_number))

	for bad_file, new_file in file_case_match.items():
		all_lines = all_lines.replace(bad_file, new_file)

	return all_lines


def check_file_exists(path):
	"""
	Check if a file exists in the CCCP tree.

	returns:
	"" if path exists
	"path.rte/to/file" if path exists, but is miscased
	"ERROR" if file is missing entirely
	"""

	if (path in _path_glob) or (path[-4:] in _image_ext and any((path[:-4] == image or (path[:-4] + "000") == image) for image in _images)):
		return ""

	path = Path(path).as_posix().replace("\\", "/")
	if path.lower() in _path_glob_lowercase:
		return _path_glob[_path_glob_lowercase.index(path.lower())]

	if path[-4:] in _image_ext:
		for image in _images:
			if path[:-4].lower() == image.lower():
				return image + path[-4:]
			elif path[:-4].lower() + "000" == image.lower():
				return image[:-3] + path[-4:]


	return "ERROR"


def case_check_ini_line(line, file_name, line_number):
	line_uncommented = line.split("//")[0].strip()
	if any(line_uncommented.startswith(include_op) for include_op in _ini_file_includes):

		contents = line_uncommented.rpartition("=")[-1].strip()
		out = check_file_exists(contents)

		if out == "":
			return {}
		if out == "ERROR":
			error_could_not_locate(file_name, line_number, contents)
			return {}
		else:
			return {contents:out}
	else:
		return {}


def lua_include_exists(included_file):
	"""
	Check if a lua file exists case sensitive. This looks up the lua file
	in the glob and in relative directories.
	"""
	if included_file in _path_glob or any(included_file + ".lua" in file for file in _path_glob):
		return ""

	included_file = Path(included_file).as_posix().replace("\\", "/")

	for i, file in enumerate(_path_glob_lowercase):
		if included_file.lower() in file:
			if ".rte" in included_file.lower().partition("/")[0]:
				return _path_glob[i]
			else:
				if included_file.lower() == file.partition("/")[2][:-4]:
					return _path_glob[i]

	return "ERROR"


def case_check_lua_line(line, file_name, line_number):

	if any(include_op in line.split("--")[0] for include_op in _lua_file_includes):
		operation = line.split("--")[0].partition('"')[0].partition("'")[0].rpartition("=")[-1].strip("( ")
		contents = re.search(r"['\"]([^'\"]*)['\"]", line.split("--")[0])
		out = ""
		if contents:
			contents = contents.group(1)
			out = lua_include_exists(contents)
		if out == "":
			return {}
		elif out == "ERROR":
			error_could_not_locate(file_name, line_number, contents)
			return {}
		else:
			if operation == "require":
				return {contents:out.partition("/")[2][:-4]}
			else:
				return {contents:out}

	if ".rte" in line.split("--")[0]:
		contents = re.search(r"['\"]([^'\"]*)['\"]", line.split("--")[0])
		if contents:
			for match in contents.groups():
				if ".rte" in match.partition("/")[0]:
					module = match.partition("/")[0].strip(";:\"'")
					if	module in _modules:
						return {}
					elif module.lower() in [m.lower() for m in _modules]:
						return {module:_modules[[m.lower() for m in _modules].index(module.lower())]}
					else:
						error_failed_to_find_module(file_name, line_number, module)
						return {}

	return {}
