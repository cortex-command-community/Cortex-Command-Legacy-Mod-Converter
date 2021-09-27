import sys

from Python.ini_parser import ini_parser


def run():
	ini_parser_tests()


def ini_parser_tests():
	ini_parser_get_line_data("a = b", [{'type': 'property', 'value': 'a'}, {'type': 'extra', 'value': ' '}, {'type': 'extra', 'value': '='}, {'type': 'extra', 'value': ' '}, {'type': 'value', 'value': 'b'}])
	ini_parser_get_line_data("// a = b", [{'type': 'extra', 'value': '//'}, {'type': 'extra', 'value': ' '}, {'type': 'extra', 'value': 'a'}, {'type': 'extra', 'value': ' '}, {'type': 'extra', 'value': '='}, {'type': 'extra', 'value': ' '}, {'type': 'extra', 'value': 'b'}])
	ini_parser_get_line_data("a = b //", [{'type': 'property', 'value': 'a'}, {'type': 'extra', 'value': ' '}, {'type': 'extra', 'value': '='}, {'type': 'extra', 'value': ' '}, {'type': 'value', 'value': 'b'}, {'type': 'extra', 'value': ' '}, {'type': 'extra', 'value': '//'}])
	ini_parser_get_line_data(" // a = b", [{'type': 'extra', 'value': ' '}, {'type': 'extra', 'value': '//'}, {'type': 'extra', 'value': ' '}, {'type': 'extra', 'value': 'a'}, {'type': 'extra', 'value': ' '}, {'type': 'extra', 'value': '='}, {'type': 'extra', 'value': ' '}, {'type': 'extra', 'value': 'b'}])
	ini_parser_get_line_data("a = b // ", [{'type': 'property', 'value': 'a'}, {'type': 'extra', 'value': ' '}, {'type': 'extra', 'value': '='}, {'type': 'extra', 'value': ' '}, {'type': 'value', 'value': 'b'}, {'type': 'extra', 'value': ' '}, {'type': 'extra', 'value': '//'}, {'type': 'extra', 'value': ' '}])
	ini_parser_get_line_data("/* a = b */", [{'type': 'extra', 'value': '/*'}, {'type': 'extra', 'value': ' '}, {'type': 'extra', 'value': 'a'}, {'type': 'extra', 'value': ' '}, {'type': 'extra', 'value': '='}, {'type': 'extra', 'value': ' '}, {'type': 'extra', 'value': 'b'}, {'type': 'extra', 'value': ' '}, {'type': 'extra', 'value': '*/'}])
	ini_parser_get_line_data("/* a = b */ c = d", [{'type': 'extra', 'value': '/*'}, {'type': 'extra', 'value': ' '}, {'type': 'extra', 'value': 'a'}, {'type': 'extra', 'value': ' '}, {'type': 'extra', 'value': '='}, {'type': 'extra', 'value': ' '}, {'type': 'extra', 'value': 'b'}, {'type': 'extra', 'value': ' '}, {'type': 'extra', 'value': '*/'}, {'type': 'extra', 'value': ' '}, {'type': 'property', 'value': 'c'}, {'type': 'extra', 'value': ' '}, {'type': 'extra', 'value': '='}, {'type': 'extra', 'value': ' '}, {'type': 'value', 'value': 'd'}])
	ini_parser_get_line_data("// /*", [{'type': 'extra', 'value': '//'}, {'type': 'extra', 'value': ' '}, {'type': 'extra', 'value': '/*'}])
	ini_parser_get_line_data("foo/bar/baz", [{'type': 'property', 'value': 'foo/bar/baz'}])
	ini_parser_get_line_data("	 Mass  =  240 ", [{'type': 'extra', 'value': '\t '}, {'type': 'property', 'value': 'Mass'}, {'type': 'extra', 'value': '  '}, {'type': 'extra', 'value': '='}, {'type': 'extra', 'value': '  '}, {'type': 'value', 'value': '240'}, {'type': 'extra', 'value': ' '}])
	# ini_parser_get_line_data("", [])


multiline = False

def ini_parser_get_line_data(line, expected):
	global multiline

	line_data, multiline = ini_parser.get_line_data(line, multiline)

	test(line, line_data, expected)


def test(input_str, result, expected):
	function_name = sys._getframe(1).f_code.co_name
	error_message = (
		"A test error occurred, report it to MyNameIsTrez#1585!"
		f"\n\nTest function name: {function_name}"
		f"\n\nInput:\n{repr(input_str)}"
		f"\n\nExpected:\n{str(expected)}"
		f"\n\nResult:\n{str(result)}"
	)
	# TODO: Make the error_message not show twice in the popup.
	assert result == expected, error_message