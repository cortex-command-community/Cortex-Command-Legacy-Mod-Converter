from Python import tests
from Python.ini_converting import ini_tokenizer
from Python.ini_converting import ini_cst
from Python.ini_converting import ini_ast


def ast_tests():
	test("lstripped_tab", [
		{ "property": "Foo", "value": "Bar" }
	])
	test("simple", [
		{ "property": "AddEffect", "value": "MOPixel" }
	])
	test("comments", [
		{}
	])
	test("nested", [
		{ "property": "Foo", "value": "Bar", "children": [
			{ "property": "Baz", "value": "Bee" }
		]}
	])
	test("multiple", [
		{ "property": "Foo", "value": "Bar", "children": [
			{ "property": "Baz", "value": "Bee" }
		]},
		{ "property": "A", "value": "B", "children": [
			{ "property": "C", "value": "D" }
		]}
	])
	test("complex", [
		{ "property": "AddEffect", "value": "MOPixel", "children": [
			{ "property": "PresetName", "value": "red_dot_tiny", "children": [
				{ "property": "Mass", "value": "0.0" },
				{ "property": "Xd", "value": "42" }
			]}
		]}
	])
	test("deindentation_1", [
		{ "property": "PresetName", "value": "Foo", "children": [
			{ "property": "A1", "value": "X" },
			{ "property": "A2", "value": "X" },
			{ "property": "B1", "value": "X" },
			{ "property": "B2", "value": "X" },
			{ "property": "C1", "value": "X" },
			{ "property": "C2", "value": "X" }
		]}
	])
	test("deindentation_2", [
		{ "property": "AddEffect", "value": "MOPixel", "children": [
			{ "property": "PresetName", "value": "Foo", "children": [
				{ "property": "A1", "value": "X" },
				{ "property": "A2", "value": "X" },
				{ "property": "B1", "value": "X" },
				{ "property": "B2", "value": "X" },
				{ "property": "C1", "value": "X" },
				{ "property": "C2", "value": "X" }
			]}
		]}
	])
	test("deindentation_3", [
		{ "property": "AddEffect", "value": "MOPixel", "children": [
			{ "property": "PresetName", "value": "Foo", "children": [
				{ "property": "A1", "value": "X" },
				{ "property": "A2", "value": "X" },
				{ "property": "B1", "value": "X" },
				{ "property": "B2", "value": "X" },
				{ "property": "C1", "value": "X" },
				{ "property": "C2", "value": "X" }
			]}
		]}
	])
	test("spaces", [
		{ "property": "Foo", "value": "Bar Baz" }
	])
	test("comment_before_tabs", [
		{ "property": "A1", "value": "A2", "children": [
			{ "property": "B1", "value": "B2", "children": [
				{ "property": "C1", "value": "C2", "children": [
					{ "property": "D1", "value": "D2" },
					{ "property": "E1", "value": "E2" }
				]}
			]}
		]}
	])
	test("comment_in_tabs", [
		{ "property": "A1", "value": "A2", "children": [
			{ "property": "B1", "value": "B2", "children": [
				{ "property": "C1", "value": "C2", "children": [
					{ "property": "D1", "value": "D2" },
					{ "property": "E1", "value": "E2" }
				]}
			]}
		]}
	])
	test("spaces_at_start_of_line", [
		{ "property": "Foo", "value": "Bar" },
		{ "property": "Baz", "value": "Bee" }
	])
	test("datamodule", [
		{ "property": "DataModule", "children": [
			{ "property": "IconFile", "value": "ContentFile", "children": [
				{ "property": "FilePath", "value": "Foo" }
			]},
			{ "property": "ModuleName", "value": "Bar" }
		]}
	])
	test("value_on_next_line", [
		{ "property": "Foo", "value": "Bar" }
	])


def test(filename, expected):
	filepath = tests.get_test_path_from_filename(filename)

	tokens = ini_tokenizer.get_tokens(str(filepath))
	cst = ini_cst.get_cst(tokens)
	ast = ini_ast.get_ast(cst)

	tests.test(filename, ast, expected)
