from Python import tests
from Python.ini_converting import ini_tokenizer
from Python.ini_converting import ini_parser


def parser_tests():
	# test("invalid_tabbing", [ # This is expected to raise a "Too many tabs found" error.
	# 	[
	# 		{ "type": "property", "content": "AddEffect" }, { "type": "extra", "content": " " }, { "type": "extra", "content": "=" }, { "type": "extra", "content": " " }, { "type": "value", "content": "MOPixel" }, { "type": "extra", "content": "\n" },
	# 		{ "type": "extra", "content": "\t\t" }, { "type": "property", "content": "Foo" }, { "type": "extra", "content": " " }, { "type": "extra", "content": "=" }, { "type": "extra", "content": " " }, { "type": "value", "content": "Bar" },
	# 	]
	# ])
	test("simple", [
		[
			{ "type": "property", "content": "AddEffect" }, { "type": "extra", "content": " " }, { "type": "extra", "content": "=" }, { "type": "extra", "content": " " }, { "type": "value", "content": "MOPixel" },
		]
	])
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
					{ "type": "extra", "content": "\t" }, { "type": "property", "content": "Baz" }, { "type": "extra", "content": " " }, { "type": "extra", "content": "=" }, { "type": "extra", "content": " " }, { "type": "value", "content": "Bee" }, { "type": "extra", "content": "\n" },
				]
			]}
		]
	])
	test("multiple", [
		[
			{ "type": "property", "content": "Foo" }, { "type": "extra", "content": " " }, { "type": "extra", "content": "=" }, { "type": "extra", "content": " " }, { "type": "value", "content": "Bar" }, { "type": "extra", "content": "\n" },
			{ "type": "children", "content": [
				[
					{ "type": "extra", "content": "\t" }, { "type": "property", "content": "Baz" }, { "type": "extra", "content": " " }, { "type": "extra", "content": "=" }, { "type": "extra", "content": " " }, { "type": "value", "content": "Bee" }, { "type": "extra", "content": "\n" },
				]
			]}
		],
		[
			{ "type": "property", "content": "A" }, { "type": "extra", "content": " " }, { "type": "extra", "content": "=" }, { "type": "extra", "content": " " }, { "type": "value", "content": "B" }, { "type": "extra", "content": "\n" },
			{ "type": "children", "content": [
				[
					{ "type": "extra", "content": "\t" }, { "type": "property", "content": "C" }, { "type": "extra", "content": " " }, { "type": "extra", "content": "=" }, { "type": "extra", "content": " " }, { "type": "value", "content": "D" }, { "type": "extra", "content": "\n" },
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
							{ "type": "extra", "content": "\t\t" }, { "type": "property", "content": "Xd" }, { "type": "extra", "content": " " }, { "type": "extra", "content": "=" }, { "type": "extra", "content": " " }, { "type": "value", "content": "42" },
						]
					]}
				]
			]}
		]
	])
	test("deindentation_1", [
		[
			{ "type": "property", "content": "PresetName" }, { "type": "extra", "content": " " }, { "type": "extra", "content": "=" }, { "type": "extra", "content": " " }, { "type": "value", "content": "Foo" }, { "type": "extra", "content": "\n" },
			{ "type": "children", "content": [
				[
					{ "type": "extra", "content": "\t" }, { "type": "property", "content": "A1" }, { "type": "extra", "content": " " }, { "type": "extra", "content": "=" }, { "type": "extra", "content": " " }, { "type": "value", "content": "X" }, { "type": "extra", "content": "\n\n" },
				],
				[
					{ "type": "extra", "content": "\t" }, { "type": "property", "content": "A2" }, { "type": "extra", "content": " " }, { "type": "extra", "content": "=" }, { "type": "extra", "content": " " }, { "type": "value", "content": "X" }, { "type": "extra", "content": "\n" },
				],
				[
					{ "type": "extra", "content": "\t" }, { "type": "property", "content": "B1" }, { "type": "extra", "content": " " }, { "type": "extra", "content": "=" }, { "type": "extra", "content": " " }, { "type": "value", "content": "X" }, { "type": "extra", "content": "\n" },
					{ "type": "extra", "content": " " }, { "type": "extra", "content": "\n" },
				],
				[
					{ "type": "extra", "content": "\t" }, { "type": "property", "content": "B2" }, { "type": "extra", "content": " " }, { "type": "extra", "content": "=" }, { "type": "extra", "content": " " }, { "type": "value", "content": "X" }, { "type": "extra", "content": "\n" },
				],
				[
					{ "type": "extra", "content": "\t" }, { "type": "property", "content": "C1" }, { "type": "extra", "content": " " }, { "type": "extra", "content": "=" }, { "type": "extra", "content": " " }, { "type": "value", "content": "X" }, { "type": "extra", "content": "\n" },
					{ "type": "extra", "content": "//foo" }, { "type": "extra", "content": "\n" },
				],
				[
					{ "type": "extra", "content": "\t" }, { "type": "property", "content": "C2" }, { "type": "extra", "content": " " }, { "type": "extra", "content": "=" }, { "type": "extra", "content": " " }, { "type": "value", "content": "X" },
				]
			]}
		]
	])
	test("deindentation_2", [
		[
			{ "type": "property", "content": "AddEffect" }, { "type": "extra", "content": " " }, { "type": "extra", "content": "=" }, { "type": "extra", "content": " " }, { "type": "value", "content": "MOPixel" }, { "type": "extra", "content": "\n" },
			{ "type": "children", "content": [
				[
					{ "type": "extra", "content": "\t" }, { "type": "property", "content": "PresetName" }, { "type": "extra", "content": " " }, { "type": "extra", "content": "=" }, { "type": "extra", "content": " " }, { "type": "value", "content": "Foo" }, { "type": "extra", "content": "\n" },
					{ "type": "children", "content": [
						[
							{ "type": "extra", "content": "\t\t" }, { "type": "property", "content": "A1" }, { "type": "extra", "content": " " }, { "type": "extra", "content": "=" }, { "type": "extra", "content": " " }, { "type": "value", "content": "X" }, { "type": "extra", "content": "\n\n" },
						],
						[
							{ "type": "extra", "content": "\t\t" }, { "type": "property", "content": "A2" }, { "type": "extra", "content": " " }, { "type": "extra", "content": "=" }, { "type": "extra", "content": " " }, { "type": "value", "content": "X" }, { "type": "extra", "content": "\n" },
						],
						[
							{ "type": "extra", "content": "\t\t" }, { "type": "property", "content": "B1" }, { "type": "extra", "content": " " }, { "type": "extra", "content": "=" }, { "type": "extra", "content": " " }, { "type": "value", "content": "X" }, { "type": "extra", "content": "\n" },
							{ "type": "extra", "content": " " }, { "type": "extra", "content": "\n" },
						],
						[
							{ "type": "extra", "content": "\t\t" }, { "type": "property", "content": "B2" }, { "type": "extra", "content": " " }, { "type": "extra", "content": "=" }, { "type": "extra", "content": " " }, { "type": "value", "content": "X" }, { "type": "extra", "content": "\n" },
						],
						[
							{ "type": "extra", "content": "\t\t" }, { "type": "property", "content": "C1" }, { "type": "extra", "content": " " }, { "type": "extra", "content": "=" }, { "type": "extra", "content": " " }, { "type": "value", "content": "X" }, { "type": "extra", "content": "\n" },
							{ "type": "extra", "content": "//foo" }, { "type": "extra", "content": "\n" },
						],
						[
							{ "type": "extra", "content": "\t\t" }, { "type": "property", "content": "C2" }, { "type": "extra", "content": " " }, { "type": "extra", "content": "=" }, { "type": "extra", "content": " " }, { "type": "value", "content": "X" },
						]
					]}
				]
			]}
		]
	])
	test("deindentation_3", [
		[
			{ "type": "property", "content": "AddEffect" }, { "type": "extra", "content": " " }, { "type": "extra", "content": "=" }, { "type": "extra", "content": " " }, { "type": "value", "content": "MOPixel" }, { "type": "extra", "content": "\n" },
			{ "type": "children", "content": [
				[
					{ "type": "extra", "content": "\t" }, { "type": "property", "content": "PresetName" }, { "type": "extra", "content": " " }, { "type": "extra", "content": "=" }, { "type": "extra", "content": " " }, { "type": "value", "content": "Foo" }, { "type": "extra", "content": "\n" },
					{ "type": "children", "content": [
						[
							{ "type": "extra", "content": "\t\t" }, { "type": "property", "content": "A1" }, { "type": "extra", "content": " " }, { "type": "extra", "content": "=" }, { "type": "extra", "content": " " }, { "type": "value", "content": "X" }, { "type": "extra", "content": "\n" },
							{ "type": "extra", "content": "\t" }, { "type": "extra", "content": "\n" },
						],
						[
							{ "type": "extra", "content": "\t\t" }, { "type": "property", "content": "A2" }, { "type": "extra", "content": " " }, { "type": "extra", "content": "=" }, { "type": "extra", "content": " " }, { "type": "value", "content": "X" }, { "type": "extra", "content": "\n" },
						],
						[
							{ "type": "extra", "content": "\t\t" }, { "type": "property", "content": "B1" }, { "type": "extra", "content": " " }, { "type": "extra", "content": "=" }, { "type": "extra", "content": " " }, { "type": "value", "content": "X" }, { "type": "extra", "content": "\n" },
							{ "type": "extra", "content": "\t" }, { "type": "extra", "content": " " }, { "type": "extra", "content": "\n" },
						],
						[
							{ "type": "extra", "content": "\t\t" }, { "type": "property", "content": "B2" }, { "type": "extra", "content": " " }, { "type": "extra", "content": "=" }, { "type": "extra", "content": " " }, { "type": "value", "content": "X" }, { "type": "extra", "content": "\n" },
						],
						[
							{ "type": "extra", "content": "\t\t" }, { "type": "property", "content": "C1" }, { "type": "extra", "content": " " }, { "type": "extra", "content": "=" }, { "type": "extra", "content": " " }, { "type": "value", "content": "X" }, { "type": "extra", "content": "\n" },
							{ "type": "extra", "content": "\t" }, { "type": "extra", "content": "//foo" }, { "type": "extra", "content": "\n" },
						],
						[
							{ "type": "extra", "content": "\t\t" }, { "type": "property", "content": "C2" }, { "type": "extra", "content": " " }, { "type": "extra", "content": "=" }, { "type": "extra", "content": " " }, { "type": "value", "content": "X" },
						]
					]}
				]
			]}
		]
	])
	test("spaces", [
		[
			{ "type": "property", "content": "Foo" }, { "type": "extra", "content": " " }, { "type": "extra", "content": "=" }, { "type": "extra", "content": " " }, { "type": "value", "content": "Bar Baz" },
		]
	])
	test("comment_before_tabs", [
		[
			{ "type": "property", "content": "A1" }, { "type": "extra", "content": " " }, { "type": "extra", "content": "=" }, { "type": "extra", "content": " " }, { "type": "value", "content": "A2" }, { "type": "extra", "content": "\n" },
			{ "type": "children", "content": [
				[
					{ "type": "extra", "content": "\t" }, { "type": "property", "content": "B1" }, { "type": "extra", "content": " " }, { "type": "extra", "content": "=" }, { "type": "extra", "content": " " }, { "type": "value", "content": "B2" }, { "type": "extra", "content": "\n" },
					{ "type": "children", "content": [
						[
							{ "type": "extra", "content": "\t\t" }, { "type": "property", "content": "C1" }, { "type": "extra", "content": " " }, { "type": "extra", "content": "=" }, { "type": "extra", "content": " " }, { "type": "value", "content": "C2" }, { "type": "extra", "content": "\n" },
							{ "type": "children", "content": [
								[
									{ "type": "extra", "content": "/*foo*/" }, { "type": "extra", "content": "\t\t\t" }, { "type": "property", "content": "D1" }, { "type": "extra", "content": " " }, { "type": "extra", "content": "=" }, { "type": "extra", "content": " " }, { "type": "value", "content": "D2" }, { "type": "extra", "content": "\n" },
								],
								[
									{ "type": "extra", "content": "\t\t\t" }, { "type": "property", "content": "E1" }, { "type": "extra", "content": " " }, { "type": "extra", "content": "=" }, { "type": "extra", "content": " " }, { "type": "value", "content": "E2" },
								]
							]}
						]
					]}
				]
			]}
		]
	])
	test("comment_in_tabs", [
		[
			{ "type": "property", "content": "A1" }, { "type": "extra", "content": " " }, { "type": "extra", "content": "=" }, { "type": "extra", "content": " " }, { "type": "value", "content": "A2" }, { "type": "extra", "content": "\n" },
			{ "type": "children", "content": [
				[
					{ "type": "extra", "content": "\t" }, { "type": "property", "content": "B1" }, { "type": "extra", "content": " " }, { "type": "extra", "content": "=" }, { "type": "extra", "content": " " }, { "type": "value", "content": "B2" }, { "type": "extra", "content": "\n" },
					{ "type": "children", "content": [
						[
							{ "type": "extra", "content": "\t\t" }, { "type": "property", "content": "C1" }, { "type": "extra", "content": " " }, { "type": "extra", "content": "=" }, { "type": "extra", "content": " " }, { "type": "value", "content": "C2" }, { "type": "extra", "content": "\n" },
							{ "type": "children", "content": [
								[
									{ "type": "extra", "content": "\t" }, { "type": "extra", "content": "/*foo*/" }, { "type": "extra", "content": "\t\t" }, { "type": "property", "content": "D1" }, { "type": "extra", "content": " " }, { "type": "extra", "content": "=" }, { "type": "extra", "content": " " }, { "type": "value", "content": "D2" }, { "type": "extra", "content": "\n" },
								],
								[
									{ "type": "extra", "content": "\t\t\t" }, { "type": "property", "content": "E1" }, { "type": "extra", "content": " " }, { "type": "extra", "content": "=" }, { "type": "extra", "content": " " }, { "type": "value", "content": "E2" },
								]
							]}
						]
					]}
				]
			]}
		]
	])
	test("spaces_at_start_of_line", [
		[
			{ "type": "property", "content": "Foo" }, { "type": "extra", "content": " " }, { "type": "extra", "content": "=" }, { "type": "extra", "content": " " }, { "type": "value", "content": "Bar" }, { "type": "extra", "content": "\n" }, { "type": "extra", "content": "    " },
		],
		[
			{ "type": "property", "content": "Baz" }, { "type": "extra", "content": " " }, { "type": "extra", "content": "=" }, { "type": "extra", "content": " " }, { "type": "value", "content": "Bee" },
		]
	])


def test(filename, expected):
	filepath = tests.get_test_path_from_filename(filename)

	tokens = ini_tokenizer.get_tokens(str(filepath))
	ini_cst = ini_parser.get_parsed_tokens(tokens)
	
	tests.test(filename, ini_cst, expected)
