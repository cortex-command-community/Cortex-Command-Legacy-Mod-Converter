from Python import tests
from Python.ini_converting import ini_tokenizer


def tokenizer_tests():
	test("1", [
		{ "type": "WORD", "content": "AddEffect" }, { "type": "EXTRA", "content": " " }, { "type": "EQUALS", "content": "=" }, { "type": "EXTRA", "content": " " }, { "type": "WORD", "content": "MOPixel" },
	])
	test("2", [
		{ "type": "NEWLINES", "content": "\n" },
		{ "type": "EXTRA", "content": "// foo" }, { "type": "NEWLINES", "content": "\n" },
		{ "type": "EXTRA", "content": "/*a\nb\nc*/" }, { "type": "NEWLINES", "content": "\n" },
		{ "type": "WORD", "content": "AddEffect" }, { "type": "EXTRA", "content": "  " }, { "type": "EQUALS", "content": "=" }, { "type": "EXTRA", "content": " " }, { "type": "WORD", "content": "MOPixel" }, { "type": "EXTRA", "content": "//bar" }, { "type": "NEWLINES", "content": "\n" },
		{ "type": "TABS", "content": "\t" }, { "type": "WORD", "content": "PresetName" }, { "type": "EXTRA", "content": " " }, { "type": "EQUALS", "content": "=" }, { "type": "EXTRA", "content": "  " }, { "type": "WORD", "content": "red_dot_tiny" }, { "type": "NEWLINES", "content": "\n" },
		{ "type": "TABS", "content": "\t\t" }, { "type": "WORD", "content": "Mass" }, { "type": "EXTRA", "content": "  " }, { "type": "EQUALS", "content": "=" }, { "type": "EXTRA", "content": "  " }, { "type": "WORD", "content": "0.0" }, { "type": "NEWLINES", "content": "\n" },
		{ "type": "TABS", "content": "\t\t" }, { "type": "WORD", "content": "Xd" }, { "type": "EXTRA", "content": " " }, { "type": "EQUALS", "content": "=" }, { "type": "EXTRA", "content": " " }, { "type": "WORD", "content": "42" }
	])


def test(filename, expected):
	text = tests.read_test(filename)
	tests.test(text, ini_tokenizer.get_tokens(text), expected)