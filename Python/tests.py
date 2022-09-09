import sys
from pathlib import Path

from Python import utils
from Python.ini_converting import ini_tokenizer_tests
from Python.ini_converting import ini_cst_tests
from Python.ini_converting import ini_ast_tests


def run():
	ini_tokenizer_tests.tokenizer_tests()
	ini_cst_tests.cst_tests()
	ini_ast_tests.ast_tests()


def get_test_path_from_filename(filename):
	return Path(utils.path(f"Python/ini_converting/ini_test_files/{filename}.ini"))


def test(test_name, result, expected):
	if result != expected:
		# TODO: Comment these out before releasing this!
		# import json
		# with open("result.json", "w") as f:
		# 	f.write(json.dumps(result, indent=4))
		# with open("expected.json", "w") as f:
		# 	f.write(json.dumps(expected, indent=4))

		raise ValueError(f"The test '{test_name}' failed, report it to MyNameIsTrez#1585!")
