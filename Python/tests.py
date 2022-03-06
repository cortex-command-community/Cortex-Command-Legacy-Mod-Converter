import sys
from pathlib import Path

from Python import utils
from Python.ini_converting import ini_tokenizer_tests
from Python.ini_converting import ini_parser_tests


def run():
	ini_tokenizer_tests.tokenizer_tests()
	ini_parser_tests.parser_tests()
	# ini_parser_tests.single_line_tests()
	# ini_parser_tests.multi_line_tests()


def get_test_path_from_filename(filename):
	return Path(utils.resource_path(f"Python/ini_converting/ini_test_files/{filename}.ini"))


def read_test(filepath):
	return filepath.read_text()


def test(input_str, result, expected):
	function_name = sys._getframe(1).f_code.co_name
	error_message = (
		"A test error occurred, report it to MyNameIsTrez#1585!"
		f"\n\nTest function name: {function_name}"
		f"\n\nInput:\n{repr(input_str)}"
		f"\n\nExpected:\n{str(expected)}"
		f"\n\nResult:\n{str(result)}"
	)

	# print(result)

	# TODO: Comment these out before releasing this!
	# import json
	# with open("result.json", "w") as f:
	# 	f.write(json.dumps(result))
	# with open("expected.json", "w") as f:
	# 	f.write(json.dumps(expected))

	# TODO: Make the error_message not show twice in the popup.
	assert result == expected, error_message