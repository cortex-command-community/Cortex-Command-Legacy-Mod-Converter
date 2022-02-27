from Python import tests
from Python.ini_converting import ini_tokenizer
from Python.ini_converting import ini_parser


def parser_tests():
	test("simple", [
		{ "type": "lines_tokens", "content": [
			{ "type": "property", "content": "AddEffect" }, { "type": "extra", "content": " " }, { "type": "extra", "content": "=" }, { "type": "extra", "content": " " }, { "type": "value", "content": "MOPixel" }
		]}
	])
	test("comments", [
		{ "type": "lines_tokens", "content": [
			{ "type": "extra", "content": "\n" },
			{ "type": "extra", "content": "// foo"}, { "type": "extra", "content": "\n" },
			{ "type": "extra", "content": "/*a\nb\nc*/" }, { "type": "extra", "content": "\n" },
		]},
	])
	test("multiple", [
		{ "type": "lines_tokens", "content": [
			{ "type": "property", "content": "Foo" }, { "type": "extra", "content": " " }, { "type": "extra", "content": "=" }, { "type": "extra", "content": " " }, { "type": "value", "content": "Bar" }, { "type": "extra", "content": "\n" },
			{ "type": "lines_tokens", "content": [
				{ "type": "extra", "content": "\t" }, { "type": "property", "content": "Baz" }, { "type": "extra", "content": " " }, { "type": "extra", "content": "=" }, { "type": "extra", "content": " " }, { "type": "value", "content": "Bee" }, { "type": "extra", "content": "\n" }
			]}
		]},
		{ "type": "lines_tokens", "content": [
			{ "type": "property", "content": "A" }, { "type": "extra", "content": " " }, { "type": "extra", "content": "=" }, { "type": "extra", "content": " " }, { "type": "value", "content": "B" }, { "type": "extra", "content": "\n" },
			{ "type": "lines_tokens", "content": [
				{ "type": "extra", "content": "\t" }, { "type": "property", "content": "C" }, { "type": "extra", "content": " " }, { "type": "extra", "content": "=" }, { "type": "extra", "content": " " }, { "type": "value", "content": "D" }, { "type": "extra", "content": "\n" }
			]}
		]}
	])
	test("complex", [
		{ "type": "lines_tokens", "content": [
			{ "type": "extra", "content": "\n" },
			{ "type": "extra", "content": "// foo"}, { "type": "extra", "content": "\n" },
			{ "type": "extra", "content": "/*a\nb\nc*/" }, { "type": "extra", "content": "\n" },
			{ "type": "property", "content": "AddEffect" }, { "type": "extra", "content": "  " }, { "type": "extra", "content": "=" }, { "type": "extra", "content": " " }, { "type": "value", "content": "MOPixel" }, { "type": "extra", "content": "//bar" }, { "type": "extra", "content": "\n" },
			{ "type": "lines_tokens", "content": [
				{ "type": "extra", "content": "\t" }, { "type": "property", "content": "PresetName" }, { "type": "extra", "content": " " }, { "type": "extra", "content": "=" }, { "type": "extra", "content": "  " }, { "type": "value", "content": "red_dot_tiny" }, { "type": "extra", "content": "\n" },
				{ "type": "lines_tokens", "content": [
					{ "type": "extra", "content": "\t\t" }, { "type": "property", "content": "Mass" }, { "type": "extra", "content": "  " }, { "type": "extra", "content": "=" }, { "type": "extra", "content": "  " }, { "type": "value", "content": "0.0" }, { "type": "extra", "content": "\n" },
					{ "type": "extra", "content": "\t\t" }, { "type": "property", "content": "Xd" }, { "type": "extra", "content": " " }, { "type": "extra", "content": "=" }, { "type": "extra", "content": " " }, { "type": "value", "content": "42" }
				]}
			]}
		]},
	])


def test(filename, expected):
	text = tests.read_test(filename)
	tokens = ini_tokenizer.get_tokens(text)
	ini_cst, _ = ini_parser.get_parsed_tokens(tokens, [])
	tests.test(text, ini_cst, expected)