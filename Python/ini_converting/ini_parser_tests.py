from Python import tests
from Python.ini_converting import ini_tokenizer
from Python.ini_converting import ini_parser


def parser_tests():
	test("simple", [
		[
			{ "type": "property", "content": "AddEffect" }, { "type": "extra", "content": " " }, { "type": "extra", "content": "=" }, { "type": "extra", "content": " " }, { "type": "value", "content": "MOPixel" }
		]
	])
	# test("invalid_tabbing", [
	# 	[
	# 		{ "type": "property", "content": "AddEffect" }, { "type": "extra", "content": " " }, { "type": "extra", "content": "=" }, { "type": "extra", "content": " " }, { "type": "value", "content": "MOPixel" }, { "type": "extra", "content": "\n" },
	# 		{ "type": "extra", "content": "\t\t" }, { "type": "property", "content": "Foo" }, { "type": "extra", "content": " " }, { "type": "extra", "content": "=" }, { "type": "extra", "content": " " }, { "type": "value", "content": "Bar" }
	# 	]
	# ])
	test("comments", [
		[
			{ "type": "extra", "content": "\n" },
			{ "type": "extra", "content": "// foo"}, { "type": "extra", "content": "\n" },
			{ "type": "extra", "content": "/*a\nb\nc*/" }, { "type": "extra", "content": "\n" },
		],
	])
	test("nested", [
		[
			{ "type": "property", "content": "Foo" }, { "type": "extra", "content": " " }, { "type": "extra", "content": "=" }, { "type": "extra", "content": " " }, { "type": "value", "content": "Bar" }, { "type": "extra", "content": "\n" },
			{ "type": "children", "content": [
				[
					{ "type": "extra", "content": "\t" }, { "type": "property", "content": "Baz" }, { "type": "extra", "content": " " }, { "type": "extra", "content": "=" }, { "type": "extra", "content": " " }, { "type": "value", "content": "Bee" }, { "type": "extra", "content": "\n" }
				]
			]}
		]
	])
	test("multiple", [
		[
			{ "type": "property", "content": "Foo" }, { "type": "extra", "content": " " }, { "type": "extra", "content": "=" }, { "type": "extra", "content": " " }, { "type": "value", "content": "Bar" }, { "type": "extra", "content": "\n" },
			{ "type": "children", "content": [
				[
					{ "type": "extra", "content": "\t" }, { "type": "property", "content": "Baz" }, { "type": "extra", "content": " " }, { "type": "extra", "content": "=" }, { "type": "extra", "content": " " }, { "type": "value", "content": "Bee" }, { "type": "extra", "content": "\n" }
				]
			]}
		],
		[
			{ "type": "property", "content": "A" }, { "type": "extra", "content": " " }, { "type": "extra", "content": "=" }, { "type": "extra", "content": " " }, { "type": "value", "content": "B" }, { "type": "extra", "content": "\n" },
			{ "type": "children", "content": [
				[
					{ "type": "extra", "content": "\t" }, { "type": "property", "content": "C" }, { "type": "extra", "content": " " }, { "type": "extra", "content": "=" }, { "type": "extra", "content": " " }, { "type": "value", "content": "D" }, { "type": "extra", "content": "\n" }
				]
			]}
		]
	])
	test("complex", [
		[
			{ "type": "extra", "content": "\n" },
			{ "type": "extra", "content": "// foo"}, { "type": "extra", "content": "\n" },
			{ "type": "extra", "content": "/*a\nb\nc*/" }, { "type": "extra", "content": "\n" },
			{ "type": "property", "content": "AddEffect" }, { "type": "extra", "content": "  " }, { "type": "extra", "content": "=" }, { "type": "extra", "content": " " }, { "type": "value", "content": "MOPixel" }, { "type": "extra", "content": "//bar" }, { "type": "extra", "content": "\n" },
			{ "type": "children", "content": [
				[
					{ "type": "extra", "content": "\t" }, { "type": "property", "content": "PresetName" }, { "type": "extra", "content": " " }, { "type": "extra", "content": "=" }, { "type": "extra", "content": "  " }, { "type": "value", "content": "red_dot_tiny" }, { "type": "extra", "content": "\n" },
					{ "type": "children", "content": [
						[
							{ "type": "extra", "content": "\t\t" }, { "type": "property", "content": "Mass" }, { "type": "extra", "content": "  " }, { "type": "extra", "content": "=" }, { "type": "extra", "content": "  " }, { "type": "value", "content": "0.0" }, { "type": "extra", "content": "\n" },
						],
						[
							{ "type": "extra", "content": "\t\t" }, { "type": "property", "content": "Xd" }, { "type": "extra", "content": " " }, { "type": "extra", "content": "=" }, { "type": "extra", "content": " " }, { "type": "value", "content": "42" }
						]
					]}
				]
			]}
		]
	])


def test(filename, expected):
	filepath = tests.get_test_path_from_filename(filename)
	text = tests.read_test(filepath)
	tokens = ini_tokenizer.get_tokens(str(filepath))
	ini_cst = ini_parser.get_parsed_tokens(tokens)
	tests.test(text, ini_cst, expected)
