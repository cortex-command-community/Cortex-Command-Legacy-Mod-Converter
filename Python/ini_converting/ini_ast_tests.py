from Python import test
from Python.ini_converting import ini_tokenizer
from Python.ini_converting import ini_cst
from Python.ini_converting import ini_ast


def ast_tests():
	ast_test("lstripped_tab", [
		{ "property": "Foo", "value": "Bar" }
	])
	ast_test("simple", [
		{ "property": "AddEffect", "value": "MOPixel" }
	])
	ast_test("comments", [
		{}
	])
	ast_test("nested", [
		{ "property": "Foo", "value": "Bar", "children": [
			{ "property": "Baz", "value": "Bee" }
		]}
	])
	ast_test("multiple", [
		{ "property": "Foo", "value": "Bar", "children": [
			{ "property": "Baz", "value": "Bee" }
		]},
		{ "property": "A", "value": "B", "children": [
			{ "property": "C", "value": "D" }
		]}
	])
	ast_test("complex", [
		{ "property": "AddEffect", "value": "MOPixel", "children": [
			{ "property": "PresetName", "value": "red_dot_tiny", "children": [
				{ "property": "Mass", "value": "0.0" },
				{ "property": "Xd", "value": "42" }
			]}
		]}
	])
	ast_test("deindentation_1", [
		{ "property": "PresetName", "value": "Foo", "children": [
			{ "property": "A1", "value": "X" },
			{ "property": "A2", "value": "X" },
			{ "property": "B1", "value": "X" },
			{ "property": "B2", "value": "X" },
			{ "property": "C1", "value": "X" },
			{ "property": "C2", "value": "X" }
		]}
	])
	ast_test("deindentation_2", [
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
	ast_test("deindentation_3", [
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
	ast_test("spaces", [
		{ "property": "Foo", "value": "Bar Baz" }
	])
	ast_test("comment_before_tabs", [
		{ "property": "A1", "value": "A2", "children": [
			{ "property": "B1", "value": "B2", "children": [
				{ "property": "C1", "value": "C2", "children": [
					{ "property": "D1", "value": "D2" },
					{ "property": "E1", "value": "E2" }
				]}
			]}
		]}
	])
	ast_test("comment_in_tabs", [
		{ "property": "A1", "value": "A2", "children": [
			{ "property": "B1", "value": "B2", "children": [
				{ "property": "C1", "value": "C2", "children": [
					{ "property": "D1", "value": "D2" },
					{ "property": "E1", "value": "E2" }
				]}
			]}
		]}
	])
	ast_test("spaces_at_start_of_line", [
		{ "property": "Foo", "value": "Bar" },
		{ "property": "Baz", "value": "Bee" }
	])
	ast_test("datamodule", [
		{ "property": "DataModule", "children": [
			{ "property": "IconFile", "value": "ContentFile", "children": [
				{ "property": "FilePath", "value": "Foo" }
			]},
			{ "property": "ModuleName", "value": "Bar" }
		]}
	])
	ast_test("value_on_next_line", [
		{ "property": "Foo", "value": "Bar" }
	])


def ast_test(filename, expected):
	filepath = test.get_test_path_from_filename(filename)

	tokens = ini_tokenizer.get_tokens(str(filepath))
	cst = ini_cst.get_cst(tokens)
	ast = ini_ast.get_ast(cst)

	test.test(filename, ast, expected)
