from Python import tests
from Python.ini_converting import ini_tokenizer


def tokenizer_tests():
	test("simple", [
		{ "type": "WORD", "content": "AddEffect" }, { "type": "EXTRA", "content": " " }, { "type": "EQUALS", "content": "=" }, { "type": "EXTRA", "content": " " }, { "type": "WORD", "content": "MOPixel" },
	])
	test("comments", [
		{ "type": "NEWLINES", "content": "\n" },
		{ "type": "EXTRA", "content": "// foo" }, { "type": "NEWLINES", "content": "\n" },
		{ "type": "EXTRA", "content": "/*a\nb\nc*/" }, { "type": "NEWLINES", "content": "\n" },
	])
	test("multiple", [
		{ "type": "WORD", "content": "Foo" }, { "type": "EXTRA", "content": " " }, { "type": "EQUALS", "content": "=" }, { "type": "EXTRA", "content": " " }, { "type": "WORD", "content": "Bar" }, { "type": "NEWLINES", "content": "\n" },
		{ "type": "TABS", "content": "\t" }, { "type": "WORD", "content": "Baz" }, { "type": "EXTRA", "content": " " }, { "type": "EQUALS", "content": "=" }, { "type": "EXTRA", "content": " " }, { "type": "WORD", "content": "Bee" }, { "type": "NEWLINES", "content": "\n" },
		{ "type": "WORD", "content": "A" }, { "type": "EXTRA", "content": " " }, { "type": "EQUALS", "content": "=" }, { "type": "EXTRA", "content": " " }, { "type": "WORD", "content": "B" }, { "type": "NEWLINES", "content": "\n" },
		{ "type": "TABS", "content": "\t" }, { "type": "WORD", "content": "C" }, { "type": "EXTRA", "content": " " }, { "type": "EQUALS", "content": "=" }, { "type": "EXTRA", "content": " " }, { "type": "WORD", "content": "D" }, { "type": "NEWLINES", "content": "\n" },
	])
	test("complex", [
		{ "type": "NEWLINES", "content": "\n" },
		{ "type": "EXTRA", "content": "// foo" }, { "type": "NEWLINES", "content": "\n" },
		{ "type": "EXTRA", "content": "/*a\nb\nc*/" }, { "type": "NEWLINES", "content": "\n" },
		{ "type": "WORD", "content": "AddEffect" }, { "type": "EXTRA", "content": "  " }, { "type": "EQUALS", "content": "=" }, { "type": "EXTRA", "content": " " }, { "type": "WORD", "content": "MOPixel" }, { "type": "EXTRA", "content": "//bar" }, { "type": "NEWLINES", "content": "\n" },
		{ "type": "TABS", "content": "\t" }, { "type": "WORD", "content": "PresetName" }, { "type": "EXTRA", "content": " " }, { "type": "EQUALS", "content": "=" }, { "type": "EXTRA", "content": "  " }, { "type": "WORD", "content": "red_dot_tiny" }, { "type": "NEWLINES", "content": "\n" },
		{ "type": "TABS", "content": "\t\t" }, { "type": "WORD", "content": "Mass" }, { "type": "EXTRA", "content": "  " }, { "type": "EQUALS", "content": "=" }, { "type": "EXTRA", "content": "  " }, { "type": "WORD", "content": "0.0" }, { "type": "NEWLINES", "content": "\n" },
		{ "type": "TABS", "content": "\t\t" }, { "type": "WORD", "content": "Xd" }, { "type": "EXTRA", "content": " " }, { "type": "EQUALS", "content": "=" }, { "type": "EXTRA", "content": " " }, { "type": "WORD", "content": "42" },
	])


def test(filename, expected):
	text = tests.read_test(filename)
	tests.test(text, ini_tokenizer.get_tokens(text), expected)