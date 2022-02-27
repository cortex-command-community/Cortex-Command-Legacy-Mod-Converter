from Python import tests
from Python.ini_converting import ini_tokenizer
from Python.ini_converting import ini_parser


def parser_tests():
	test("multiple", [
		[
			{ "type": "property", "content": "Foo" }, { "type": "extra", "content": " " }, { "type": "extra", "content": "=" }, { "type": "extra", "content": " " }, { "type": "value", "content": "Bar" }, { "type": "extra", "content": "\n" },
			{ "type": "lines_tokens", "content": [
				{ "type": "extra", "content": "\t" }, { "type": "property", "content": "Baz" }, { "type": "extra", "content": " " }, { "type": "extra", "content": "=" }, { "type": "extra", "content": " " }, { "type": "value", "content": "Bee" }
			]},
			{ "type": "property", "content": "A" }, { "type": "extra", "content": " " }, { "type": "extra", "content": "=" }, { "type": "extra", "content": " " }, { "type": "value", "content": "B" }, { "type": "extra", "content": "\n" },
			{ "type": "lines_tokens", "content": [
				{ "type": "extra", "content": "\t" }, { "type": "property", "content": "C" }, { "type": "extra", "content": " " }, { "type": "extra", "content": "=" }, { "type": "extra", "content": " " }, { "type": "value", "content": "D" }
			]}
		]
	])
	test("2", [
		[
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
		],
	])


def test(filename, expected):
	text = tests.read_test(filename)
	tokens = ini_tokenizer.get_tokens(text)
	tests.test(text, ini_parser.get_parsed_tokens(tokens), expected)