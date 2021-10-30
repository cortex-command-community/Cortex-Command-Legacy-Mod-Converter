from Python import tests
from Python.ini_converting import ini_parser


def single_line_tests():
	# TODO: Add multiline tests.
	# TODO: Move these tests to the file ini_converting/ini_parser_tests.py
	ini_parser_get_line_data("a = b", 0, [{'type': 'property', 'value': 'a'}, {'type': 'extra', 'value': ' '}, {'type': 'extra', 'value': '='}, {'type': 'extra', 'value': ' '}, {'type': 'value', 'value': 'b'}])
	ini_parser_get_line_data("// a = b", 0, [{'type': 'extra', 'value': '//'}, {'type': 'extra', 'value': ' '}, {'type': 'extra', 'value': 'a'}, {'type': 'extra', 'value': ' '}, {'type': 'extra', 'value': '='}, {'type': 'extra', 'value': ' '}, {'type': 'extra', 'value': 'b'}])
	ini_parser_get_line_data("c// a = b", 0, [{'type': 'property', 'value': 'c'}, {'type': 'extra', 'value': '//'}, {'type': 'extra', 'value': ' '}, {'type': 'extra', 'value': 'a'}, {'type': 'extra', 'value': ' '}, {'type': 'extra', 'value': '='}, {'type': 'extra', 'value': ' '}, {'type': 'extra', 'value': 'b'}])
	ini_parser_get_line_data("a = b //", 0, [{'type': 'property', 'value': 'a'}, {'type': 'extra', 'value': ' '}, {'type': 'extra', 'value': '='}, {'type': 'extra', 'value': ' '}, {'type': 'value', 'value': 'b'}, {'type': 'extra', 'value': ' '}, {'type': 'extra', 'value': '//'}])
	ini_parser_get_line_data(" // a = b", 0, [{'type': 'extra', 'value': ' '}, {'type': 'extra', 'value': '//'}, {'type': 'extra', 'value': ' '}, {'type': 'extra', 'value': 'a'}, {'type': 'extra', 'value': ' '}, {'type': 'extra', 'value': '='}, {'type': 'extra', 'value': ' '}, {'type': 'extra', 'value': 'b'}])
	ini_parser_get_line_data("a = b // ", 0, [{'type': 'property', 'value': 'a'}, {'type': 'extra', 'value': ' '}, {'type': 'extra', 'value': '='}, {'type': 'extra', 'value': ' '}, {'type': 'value', 'value': 'b'}, {'type': 'extra', 'value': ' '}, {'type': 'extra', 'value': '//'}, {'type': 'extra', 'value': ' '}])
	ini_parser_get_line_data("/* a = b */", 0, [{'type': 'extra', 'value': '/*'}, {'type': 'extra', 'value': ' '}, {'type': 'extra', 'value': 'a'}, {'type': 'extra', 'value': ' '}, {'type': 'extra', 'value': '='}, {'type': 'extra', 'value': ' '}, {'type': 'extra', 'value': 'b'}, {'type': 'extra', 'value': ' '}, {'type': 'extra', 'value': '*/'}])
	ini_parser_get_line_data("/* a = b */ c = d", 0, [{'type': 'extra', 'value': '/*'}, {'type': 'extra', 'value': ' '}, {'type': 'extra', 'value': 'a'}, {'type': 'extra', 'value': ' '}, {'type': 'extra', 'value': '='}, {'type': 'extra', 'value': ' '}, {'type': 'extra', 'value': 'b'}, {'type': 'extra', 'value': ' '}, {'type': 'extra', 'value': '*/'}, {'type': 'extra', 'value': ' '}, {'type': 'property', 'value': 'c'}, {'type': 'extra', 'value': ' '}, {'type': 'extra', 'value': '='}, {'type': 'extra', 'value': ' '}, {'type': 'value', 'value': 'd'}])
	ini_parser_get_line_data("// /*", 0, [{'type': 'extra', 'value': '//'}, {'type': 'extra', 'value': ' '}, {'type': 'extra', 'value': '/*'}])
	ini_parser_get_line_data("foo/bar/baz", 0, [{'type': 'property', 'value': 'foo/bar/baz'}])
	ini_parser_get_line_data("foo//bar", 0, [{'type': 'property', 'value': 'foo'}, {'type': 'extra', 'value': '//bar'}])
	ini_parser_get_line_data("foo/*bar*/", 0, [{'type': 'property', 'value': 'foo'}, {'type': 'extra', 'value': '/*bar*/'}])
	ini_parser_get_line_data("	 Mass  =  240 ", 0, [{'type': 'extra', 'value': '	 '}, {'type': 'property', 'value': 'Mass'}, {'type': 'extra', 'value': '  '}, {'type': 'extra', 'value': '='}, {'type': 'extra', 'value': '  '}, {'type': 'value', 'value': '240'}, {'type': 'extra', 'value': ' '}])
	# ini_parser_get_line_data("", 0, [])


def ini_parser_get_line_data(line, depth_tab_count, expected):
	# TODO: Verify the value of tab_count as well.
	line_data, tab_count = ini_parser.get_line_data(line, depth_tab_count)

	tests.test(line, line_data, expected)


def multi_line_tests():
	pass
	# """
	# Foo = Bar
	# 	FireSound = Sound
	# // foo
	# 		AddSample = ContentFile
	# """

	# foo(
	# 	"""a = b"""
	# 	"""\tc = d"""
	# 	"""\t\te = f"""
	# 	"""/*\tg = h"""
	# 	"""*/\ti = j"""
	# 	"""\tk = l""",
	# 	0,
	# 	[
	# 		{'type': 'property', 'value': 'a'}, {'type': 'extra', 'value': ' '}, {'type': 'extra', 'value': '='}, {'type': 'extra', 'value': ' '}, {'type': 'value', 'value': 'b'},
	# 		{'type': 'property', 'value': 'c'}, {'type': 'extra', 'value': ' '}, {'type': 'extra', 'value': '='}, {'type': 'extra', 'value': ' '}, {'type': 'value', 'value': 'd'},
	# 		{'type': 'property', 'value': 'e'}, {'type': 'extra', 'value': ' '}, {'type': 'extra', 'value': '='}, {'type': 'extra', 'value': ' '}, {'type': 'value', 'value': 'f'},
	# 		{'type': 'extra', 'value': '/*'}, {'type': 'extra', 'value': 'g'}, {'type': 'extra', 'value': ' '}, {'type': 'extra', 'value': '='}, {'type': 'extra', 'value': ' '}, {'type': 'extra', 'value': 'h'},
	# 		{'type': 'extra', 'value': '*/'}, {'type': 'extra', 'value': 'i'}, {'type': 'extra', 'value': ' '}, {'type': 'extra', 'value': '='}, {'type': 'extra', 'value': ' '}, {'type': 'extra', 'value': 'j'},
	# 		{'type': 'property', 'value': 'k'}, {'type': 'extra', 'value': ' '}, {'type': 'extra', 'value': '='}, {'type': 'extra', 'value': ' '}, {'type': 'value', 'value': 'l'},
	# 	]
	# )