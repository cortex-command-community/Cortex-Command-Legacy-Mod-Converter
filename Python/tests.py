import sys

from Python.ini_converting import ini_parser_tests


def run():
	single_line_tests()
	multi_line_tests()

def single_line_tests():
	ini_parser_tests.single_line_tests()


def multi_line_tests():
	ini_parser_tests.multi_line_tests()


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
	# TODO: Make the error_message not show twice in the popup.
	assert result == expected, error_message