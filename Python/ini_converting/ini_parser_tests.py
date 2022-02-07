from Python.reading_types import ReadingTypes

from Python import tests
from Python.ini_converting import ini_parser


def single_line_tests():
	run_single_line_test("a = b", [{"type": ReadingTypes.PROPERTY, "content": "a"}, {"type": ReadingTypes.EXTRA, "content": " = "}, {"type": ReadingTypes.VALUE, "content": "b"}])
	run_single_line_test(" a = b", [{"type": ReadingTypes.EXTRA, "content": " "}, {"type": ReadingTypes.PROPERTY, "content": "a"}, {"type": ReadingTypes.EXTRA, "content": " = "}, {"type": ReadingTypes.VALUE, "content": "b"}])
	run_single_line_test(" a = b c ", [{"type": ReadingTypes.EXTRA, "content": " "}, {"type": ReadingTypes.PROPERTY, "content": "a"}, {"type": ReadingTypes.EXTRA, "content": " = "}, {"type": ReadingTypes.VALUE, "content": "b c"}, {"type": ReadingTypes.EXTRA, "content": " "}])
	run_single_line_test(" a b = c ", [{"type": ReadingTypes.EXTRA, "content": " "}, {"type": ReadingTypes.PROPERTY, "content": "a b"}, {"type": ReadingTypes.EXTRA, "content": " = "}, {"type": ReadingTypes.VALUE, "content": "c"}, {"type": ReadingTypes.EXTRA, "content": " "}])
	run_single_line_test("a b = c d", [{"type": ReadingTypes.PROPERTY, "content": "a b"}, {"type": ReadingTypes.EXTRA, "content": " = "}, {"type": ReadingTypes.VALUE, "content": "c d"}])
	run_single_line_test(" a b = c d ", [{"type": ReadingTypes.EXTRA, "content": " "}, {"type": ReadingTypes.PROPERTY, "content": "a b"}, {"type": ReadingTypes.EXTRA, "content": " = "}, {"type": ReadingTypes.VALUE, "content": "c d"}, {"type": ReadingTypes.EXTRA, "content": " "}])
	run_single_line_test("a //", [{"type": ReadingTypes.PROPERTY, "content": "a"}, {"type": ReadingTypes.EXTRA, "content": " //"}])
	run_single_line_test("a = b //", [{"type": ReadingTypes.PROPERTY, "content": "a"}, {"type": ReadingTypes.EXTRA, "content": " = "}, {"type": ReadingTypes.VALUE, "content": "b"}, {"type": ReadingTypes.EXTRA, "content": " //"}])
	run_single_line_test("a = b // ", [{"type": ReadingTypes.PROPERTY, "content": "a"}, {"type": ReadingTypes.EXTRA, "content": " = "}, {"type": ReadingTypes.VALUE, "content": "b"}, {"type": ReadingTypes.EXTRA, "content": " // "}])
	run_single_line_test("// a = b", [{"type": ReadingTypes.EXTRA, "content": "// a = b"}])
	run_single_line_test(" // a = b", [{"type": ReadingTypes.EXTRA, "content": " // a = b"}])
	run_single_line_test("c// a = b", [{"type": ReadingTypes.PROPERTY, "content": "c"}, {"type": ReadingTypes.EXTRA, "content": "// a = b"}])
	run_single_line_test("a/b/c", [{"type": ReadingTypes.PROPERTY, "content": "a/b/c"}])
	run_single_line_test("foo / bar / baz", [{"type": ReadingTypes.PROPERTY, "content": "foo / bar / baz"}])
	run_single_line_test("a = b/c/d", [{"type": ReadingTypes.PROPERTY, "content": "a"}, {"type": ReadingTypes.EXTRA, "content": " = "}, {"type": ReadingTypes.VALUE, "content": "b/c/d"}])
	run_single_line_test("a // = b", [{"type": ReadingTypes.PROPERTY, "content": "a"}, {"type": ReadingTypes.EXTRA, "content": " // = b"}])
	run_single_line_test("foo//bar", [{"type": ReadingTypes.PROPERTY, "content": "foo"}, {"type": ReadingTypes.EXTRA, "content": "//bar"}])
	run_single_line_test("a = foo/bar/baz", [{"type": ReadingTypes.PROPERTY, "content": "a"}, {"type": ReadingTypes.EXTRA, "content": " = "}, {"type": ReadingTypes.VALUE, "content": "foo/bar/baz"}])
	run_single_line_test("a = b c", [{"type": ReadingTypes.PROPERTY, "content": "a"}, {"type": ReadingTypes.EXTRA, "content": " = "}, {"type": ReadingTypes.VALUE, "content": "b c"}])
	run_single_line_test("", [])
	run_single_line_test("	 Mass  =  240 ", [{"type": ReadingTypes.EXTRA, "content": "	 "}, {"type": ReadingTypes.PROPERTY, "content": "Mass"}, {"type": ReadingTypes.EXTRA, "content": "  =  "}, {"type": ReadingTypes.VALUE, "content": "240"}, {"type": ReadingTypes.EXTRA, "content": " "}])

	# run_single_line_test(" ", [{"type": ReadingTypes.EXTRA, "content": " "}])
	# run_single_line_test("/**/", [{"type": ReadingTypes.EXTRA, "content": "/**/"}])
	# run_single_line_test("/* a = b */", [{"type": ReadingTypes.EXTRA, "content": "/*"}, {"type": "extra", "content": " "}, {"type": "extra", "content": "a"}, {"type": "extra", "content": " "}, {"type": "extra", "content": "="}, {"type": "extra", "content": " "}, {"type": "extra", "content": "b"}, {"type": "extra", "content": " "}, {"type": "extra", "content": "*/"}])
	# run_single_line_test("/* a = b */ c = d", [{"type": "extra", "content": "/*"}, {"type": "extra", "content": " "}, {"type": "extra", "content": "a"}, {"type": "extra", "content": " "}, {"type": "extra", "content": "="}, {"type": "extra", "content": " "}, {"type": "extra", "content": "b"}, {"type": "extra", "content": " "}, {"type": "extra", "content": "*/"}, {"type": "extra", "content": " "}, {"type": "property", "content": "c"}, {"type": "extra", "content": " "}, {"type": "extra", "content": "="}, {"type": "extra", "content": " "}, {"type": "value", "content": "d"}])
	# run_single_line_test("// /*", [{"type": "extra", "content": "//"}, {"type": "extra", "content": " "}, {"type": "extra", "content": "/*"}])
	# run_single_line_test("foo/*bar*/", [{"type": "property", "content": "foo"}, {"type": "extra", "content": "/*bar*/"}])


def run_single_line_test(line, expected):
	# TODO: Verify the value of tab_count as well.
	depth_tab_count = 0
	line_tokens, tab_count = ini_parser.get_tokenized_line(line, depth_tab_count)

	tests.test(line, line_tokens, expected)


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