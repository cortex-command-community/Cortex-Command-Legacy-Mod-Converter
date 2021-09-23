from Python.ini_parser import ini_parser


def run():
	ini_parser_tests()


def ini_parser_tests():
	foo("a = b", [{'type': 'property', 'value': 'a'}, {'type': 'value', 'value': 'b'}])
	foo("// a = b", [{'type': 'extra', 'value': '// a = b'}])
	foo("a = b //", [{'type': 'property', 'value': 'a'}, {'type': 'value', 'value': 'b'}, {'type': 'extra', 'value': ' //'}])
	foo(" // a = b", [{'type': 'extra', 'value': ' // a = b'}])
	foo("a = b // ", [{'type': 'property', 'value': 'a'}, {'type': 'value', 'value': 'b'}, {'type': 'extra', 'value': ' //'}])
	# foo("/* a = b */", [{'type': 'extra', 'value': '/* a = b */'}])
	foo("/* a = b */ c = d", [{'type': 'extra', 'value': '/* a = b */'}, {'type': 'property', 'value': 'c'}, {'type': 'value', 'value': 'd'}])
	# foo("", )


multiline = False

def foo(line, expected):
	global multiline

	line_data, multiline = ini_parser.get_line_data(line, multiline)

	error_message = f"Test error!\nInput:\n{line}\nBecame:\n{str(line_data)}\nExpected:\n{str(expected)}"

	assert line_data == expected, error_message