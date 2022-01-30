from Python.reading_types import ReadingTypes

from Python import tests
from Python.ini_converting import ini_parser


def single_line_tests():
	# TODO: Add multiline tests.
	# TODO: Move these tests to the file ini_converting/ini_parser_tests.py
	run_single_line_test("a = b", [{"type": ReadingTypes.PROPERTY, "content": "a"}, {"type": ReadingTypes.EXTRA, "content": " = "}, {"type": ReadingTypes.VALUE, "content": "b"}])
	# run_single_line_test("// a = b", [{"type": "extra", "content": "//"}, {"type": "extra", "content": " "}, {"type": "extra", "content": "a"}, {"type": "extra", "content": " "}, {"type": "extra", "content": "="}, {"type": "extra", "content": " "}, {"type": "extra", "content": "b"}])
	# run_single_line_test("c// a = b", [{"type": "property", "content": "c"}, {"type": "extra", "content": "//"}, {"type": "extra", "content": " "}, {"type": "extra", "content": "a"}, {"type": "extra", "content": " "}, {"type": "extra", "content": "="}, {"type": "extra", "content": " "}, {"type": "extra", "content": "b"}])
	# run_single_line_test("a = b //", [{"type": "property", "content": "a"}, {"type": "extra", "content": " "}, {"type": "extra", "content": "="}, {"type": "extra", "content": " "}, {"type": "value", "content": "b"}, {"type": "extra", "content": " "}, {"type": "extra", "content": "//"}])
	# run_single_line_test(" // a = b", [{"type": "extra", "content": " "}, {"type": "extra", "content": "//"}, {"type": "extra", "content": " "}, {"type": "extra", "content": "a"}, {"type": "extra", "content": " "}, {"type": "extra", "content": "="}, {"type": "extra", "content": " "}, {"type": "extra", "content": "b"}])
	# run_single_line_test("a = b // ", [{"type": "property", "content": "a"}, {"type": "extra", "content": " "}, {"type": "extra", "content": "="}, {"type": "extra", "content": " "}, {"type": "value", "content": "b"}, {"type": "extra", "content": " "}, {"type": "extra", "content": "//"}, {"type": "extra", "content": " "}])
	# run_single_line_test("/* a = b */", [{"type": "extra", "content": "/*"}, {"type": "extra", "content": " "}, {"type": "extra", "content": "a"}, {"type": "extra", "content": " "}, {"type": "extra", "content": "="}, {"type": "extra", "content": " "}, {"type": "extra", "content": "b"}, {"type": "extra", "content": " "}, {"type": "extra", "content": "*/"}])
	# run_single_line_test("/* a = b */ c = d", [{"type": "extra", "content": "/*"}, {"type": "extra", "content": " "}, {"type": "extra", "content": "a"}, {"type": "extra", "content": " "}, {"type": "extra", "content": "="}, {"type": "extra", "content": " "}, {"type": "extra", "content": "b"}, {"type": "extra", "content": " "}, {"type": "extra", "content": "*/"}, {"type": "extra", "content": " "}, {"type": "property", "content": "c"}, {"type": "extra", "content": " "}, {"type": "extra", "content": "="}, {"type": "extra", "content": " "}, {"type": "value", "content": "d"}])
	# run_single_line_test("// /*", [{"type": "extra", "content": "//"}, {"type": "extra", "content": " "}, {"type": "extra", "content": "/*"}])
	# run_single_line_test("foo/bar/baz", [{"type": "property", "content": "foo/bar/baz"}])
	# run_single_line_test("foo//bar", [{"type": "property", "content": "foo"}, {"type": "extra", "content": "//bar"}])
	# run_single_line_test("foo/*bar*/", [{"type": "property", "content": "foo"}, {"type": "extra", "content": "/*bar*/"}])
	# run_single_line_test("	 Mass  =  240 ", [{"type": "extra", "content": "	 "}, {"type": "property", "content": "Mass"}, {"type": "extra", "content": "  "}, {"type": "extra", "content": "="}, {"type": "extra", "content": "  "}, {"type": "value", "content": "240"}, {"type": "extra", "content": " "}])
	# run_single_line_test("a = b c", [{"type": "property", "content": "a"}, {"type": "extra", "content": " "}, {"type": "extra", "content": "="}, {"type": "extra", "content": " "}, {"type": "value", "content": "b c"}])
	# run_single_line_test("", [])


def run_single_line_test(line, expected):
	# TODO: Verify the value of tab_count as well.
	depth_tab_count = 0
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
	# 		{"type": "property", "content": "a"}, {"type": "extra", "content": " "}, {"type": "extra", "content": "="}, {"type": "extra", "content": " "}, {"type": "value", "content": "b"},
	# 		{"type": "property", "content": "c"}, {"type": "extra", "content": " "}, {"type": "extra", "content": "="}, {"type": "extra", "content": " "}, {"type": "value", "content": "d"},
	# 		{"type": "property", "content": "e"}, {"type": "extra", "content": " "}, {"type": "extra", "content": "="}, {"type": "extra", "content": " "}, {"type": "value", "content": "f"},
	# 		{"type": "extra", "content": "/*"}, {"type": "extra", "content": "g"}, {"type": "extra", "content": " "}, {"type": "extra", "content": "="}, {"type": "extra", "content": " "}, {"type": "extra", "content": "h"},
	# 		{"type": "extra", "content": "*/"}, {"type": "extra", "content": "i"}, {"type": "extra", "content": " "}, {"type": "extra", "content": "="}, {"type": "extra", "content": " "}, {"type": "extra", "content": "j"},
	# 		{"type": "property", "content": "k"}, {"type": "extra", "content": " "}, {"type": "extra", "content": "="}, {"type": "extra", "content": " "}, {"type": "value", "content": "l"},
	# 	]
	# )