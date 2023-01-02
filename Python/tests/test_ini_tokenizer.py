import unittest

from Python.ini_converting import ini_tokenizer

from Python.tests import test


class TestINITokenizer(unittest.TestCase):
	def test_comment_before_tabs(self):
		self.tokenizer_test("comment_before_tabs", [
			{ "type": "WORD", "content": "A1" }, { "type": "EXTRA", "content": " " }, { "type": "EQUALS", "content": "=" }, { "type": "EXTRA", "content": " " }, { "type": "WORD", "content": "A2" }, { "type": "NEWLINES", "content": "\n" },
			{ "type": "TABS", "content": "\t" }, { "type": "WORD", "content": "B1" }, { "type": "EXTRA", "content": " " }, { "type": "EQUALS", "content": "=" }, { "type": "EXTRA", "content": " " }, { "type": "WORD", "content": "B2" }, { "type": "NEWLINES", "content": "\n" },
			{ "type": "TABS", "content": "\t\t" }, { "type": "WORD", "content": "C1" }, { "type": "EXTRA", "content": " " }, { "type": "EQUALS", "content": "=" }, { "type": "EXTRA", "content": " " }, { "type": "WORD", "content": "C2" }, { "type": "NEWLINES", "content": "\n" },
			{ "type": "EXTRA", "content": "/*foo*/" }, { "type": "TABS", "content": "\t\t\t" }, { "type": "WORD", "content": "D1" }, { "type": "EXTRA", "content": " " }, { "type": "EQUALS", "content": "=" }, { "type": "EXTRA", "content": " " }, { "type": "WORD", "content": "D2" }, { "type": "NEWLINES", "content": "\n" },
			{ "type": "TABS", "content": "\t\t\t" }, { "type": "WORD", "content": "E1" }, { "type": "EXTRA", "content": " " }, { "type": "EQUALS", "content": "=" }, { "type": "EXTRA", "content": " " }, { "type": "WORD", "content": "E2" },
		])

	def test_comment_in_tabs(self):
		self.tokenizer_test("comment_in_tabs", [
			{ "type": "WORD", "content": "A1" }, { "type": "EXTRA", "content": " " }, { "type": "EQUALS", "content": "=" }, { "type": "EXTRA", "content": " " }, { "type": "WORD", "content": "A2" }, { "type": "NEWLINES", "content": "\n" },
			{ "type": "TABS", "content": "\t" }, { "type": "WORD", "content": "B1" }, { "type": "EXTRA", "content": " " }, { "type": "EQUALS", "content": "=" }, { "type": "EXTRA", "content": " " }, { "type": "WORD", "content": "B2" }, { "type": "NEWLINES", "content": "\n" },
			{ "type": "TABS", "content": "\t\t" }, { "type": "WORD", "content": "C1" }, { "type": "EXTRA", "content": " " }, { "type": "EQUALS", "content": "=" }, { "type": "EXTRA", "content": " " }, { "type": "WORD", "content": "C2" }, { "type": "NEWLINES", "content": "\n" },
			{ "type": "TABS", "content": "\t" }, { "type": "EXTRA", "content": "/*foo*/" }, { "type": "TABS", "content": "\t\t" }, { "type": "WORD", "content": "D1" }, { "type": "EXTRA", "content": " " }, { "type": "EQUALS", "content": "=" }, { "type": "EXTRA", "content": " " }, { "type": "WORD", "content": "D2" }, { "type": "NEWLINES", "content": "\n" },
			{ "type": "TABS", "content": "\t\t\t" }, { "type": "WORD", "content": "E1" }, { "type": "EXTRA", "content": " " }, { "type": "EQUALS", "content": "=" }, { "type": "EXTRA", "content": " " }, { "type": "WORD", "content": "E2" },
		])

	def test_comments(self):
		self.tokenizer_test("comments", [
			{ "type": "EXTRA", "content": "// foo" }, { "type": "NEWLINES", "content": "\n" },
			{ "type": "EXTRA", "content": "/*a\nb\nc*/" }, { "type": "NEWLINES", "content": "\n" },
		])

	def test_complex(self):
		self.tokenizer_test("complex", [
			{ "type": "EXTRA", "content": "// foo" }, { "type": "NEWLINES", "content": "\n" },
			{ "type": "EXTRA", "content": "/*a\nb\nc*/" }, { "type": "NEWLINES", "content": "\n" },
			{ "type": "WORD", "content": "AddEffect" }, { "type": "EXTRA", "content": "  " }, { "type": "EQUALS", "content": "=" }, { "type": "EXTRA", "content": " " }, { "type": "WORD", "content": "MOPixel" }, { "type": "EXTRA", "content": "//bar" }, { "type": "NEWLINES", "content": "\n" },
			{ "type": "TABS", "content": "\t" }, { "type": "WORD", "content": "PresetName" }, { "type": "EXTRA", "content": " " }, { "type": "EQUALS", "content": "=" }, { "type": "EXTRA", "content": "  " }, { "type": "WORD", "content": "red_dot_tiny" }, { "type": "NEWLINES", "content": "\n" },
			{ "type": "TABS", "content": "\t" }, { "type": "WORD", "content": "Mass" }, { "type": "EXTRA", "content": "  " }, { "type": "EQUALS", "content": "=" }, { "type": "EXTRA", "content": "  " }, { "type": "WORD", "content": "0.0" }, { "type": "NEWLINES", "content": "\n" },
			{ "type": "TABS", "content": "\t" }, { "type": "WORD", "content": "Xd" }, { "type": "EXTRA", "content": " " }, { "type": "EQUALS", "content": "=" }, { "type": "EXTRA", "content": " " }, { "type": "WORD", "content": "42" }, { "type": "NEWLINES", "content": "\n" },
		])

	def test_datamodule(self):
		self.tokenizer_test("datamodule", [
			{ "type": "WORD", "content": "DataModule" }, { "type": "NEWLINES", "content": "\n" },
			{ "type": "TABS", "content": "\t" }, { "type": "WORD", "content": "IconFile" }, { "type": "EXTRA", "content": " " }, { "type": "EQUALS", "content": "=" }, { "type": "EXTRA", "content": " " }, { "type": "WORD", "content": "ContentFile" }, { "type": "NEWLINES", "content": "\n" },
			{ "type": "TABS", "content": "\t\t" }, { "type": "WORD", "content": "FilePath" }, { "type": "EXTRA", "content": " " }, { "type": "EQUALS", "content": "=" }, { "type": "EXTRA", "content": " " }, { "type": "WORD", "content": "Foo" }, { "type": "NEWLINES", "content": "\n" },
			{ "type": "TABS", "content": "\t" }, { "type": "WORD", "content": "ModuleName" }, { "type": "EXTRA", "content": " " }, { "type": "EQUALS", "content": "=" }, { "type": "EXTRA", "content": " " }, { "type": "WORD", "content": "Bar" },
		])

	def test_deindentation_1(self):
		self.tokenizer_test("deindentation_1", [
			{ "type": "WORD", "content": "PresetName" }, { "type": "EXTRA", "content": " " }, { "type": "EQUALS", "content": "=" }, { "type": "EXTRA", "content": " " }, { "type": "WORD", "content": "Foo" }, { "type": "NEWLINES", "content": "\n" },

			{ "type": "TABS", "content": "\t" }, { "type": "WORD", "content": "A1" }, { "type": "EXTRA", "content": " " }, { "type": "EQUALS", "content": "=" }, { "type": "EXTRA", "content": " " }, { "type": "WORD", "content": "X" }, { "type": "NEWLINES", "content": "\n\n" },
			{ "type": "TABS", "content": "\t" }, { "type": "WORD", "content": "A2" }, { "type": "EXTRA", "content": " " }, { "type": "EQUALS", "content": "=" }, { "type": "EXTRA", "content": " " }, { "type": "WORD", "content": "X" }, { "type": "NEWLINES", "content": "\n" },

			{ "type": "TABS", "content": "\t" }, { "type": "WORD", "content": "B1" }, { "type": "EXTRA", "content": " " }, { "type": "EQUALS", "content": "=" }, { "type": "EXTRA", "content": " " }, { "type": "WORD", "content": "X" }, { "type": "NEWLINES", "content": "\n" },
			{ "type": "EXTRA", "content": " " }, { "type": "NEWLINES", "content": "\n" },
			{ "type": "TABS", "content": "\t" }, { "type": "WORD", "content": "B2" }, { "type": "EXTRA", "content": " " }, { "type": "EQUALS", "content": "=" }, { "type": "EXTRA", "content": " " }, { "type": "WORD", "content": "X" }, { "type": "NEWLINES", "content": "\n" },

			{ "type": "TABS", "content": "\t" }, { "type": "WORD", "content": "C1" }, { "type": "EXTRA", "content": " " }, { "type": "EQUALS", "content": "=" }, { "type": "EXTRA", "content": " " }, { "type": "WORD", "content": "X" }, { "type": "NEWLINES", "content": "\n" },
			{ "type": "EXTRA", "content": "//foo" }, { "type": "NEWLINES", "content": "\n" },
			{ "type": "TABS", "content": "\t" }, { "type": "WORD", "content": "C2" }, { "type": "EXTRA", "content": " " }, { "type": "EQUALS", "content": "=" }, { "type": "EXTRA", "content": " " }, { "type": "WORD", "content": "X" },
		])

	def test_deindentation_2(self):
		self.tokenizer_test("deindentation_2", [
			{ "type": "WORD", "content": "AddEffect" }, { "type": "EXTRA", "content": " " }, { "type": "EQUALS", "content": "=" }, { "type": "EXTRA", "content": " " }, { "type": "WORD", "content": "MOPixel" }, { "type": "NEWLINES", "content": "\n" },
			{ "type": "TABS", "content": "\t" }, { "type": "WORD", "content": "PresetName" }, { "type": "EXTRA", "content": " " }, { "type": "EQUALS", "content": "=" }, { "type": "EXTRA", "content": " " }, { "type": "WORD", "content": "Foo" }, { "type": "NEWLINES", "content": "\n" },

			{ "type": "TABS", "content": "\t\t" }, { "type": "WORD", "content": "A1" }, { "type": "EXTRA", "content": " " }, { "type": "EQUALS", "content": "=" }, { "type": "EXTRA", "content": " " }, { "type": "WORD", "content": "X" }, { "type": "NEWLINES", "content": "\n\n" },
			{ "type": "TABS", "content": "\t\t" }, { "type": "WORD", "content": "A2" }, { "type": "EXTRA", "content": " " }, { "type": "EQUALS", "content": "=" }, { "type": "EXTRA", "content": " " }, { "type": "WORD", "content": "X" }, { "type": "NEWLINES", "content": "\n" },

			{ "type": "TABS", "content": "\t\t" }, { "type": "WORD", "content": "B1" }, { "type": "EXTRA", "content": " " }, { "type": "EQUALS", "content": "=" }, { "type": "EXTRA", "content": " " }, { "type": "WORD", "content": "X" }, { "type": "NEWLINES", "content": "\n" },
			{ "type": "EXTRA", "content": " " }, { "type": "NEWLINES", "content": "\n" },
			{ "type": "TABS", "content": "\t\t" }, { "type": "WORD", "content": "B2" }, { "type": "EXTRA", "content": " " }, { "type": "EQUALS", "content": "=" }, { "type": "EXTRA", "content": " " }, { "type": "WORD", "content": "X" }, { "type": "NEWLINES", "content": "\n" },

			{ "type": "TABS", "content": "\t\t" }, { "type": "WORD", "content": "C1" }, { "type": "EXTRA", "content": " " }, { "type": "EQUALS", "content": "=" }, { "type": "EXTRA", "content": " " }, { "type": "WORD", "content": "X" }, { "type": "NEWLINES", "content": "\n" },
			{ "type": "EXTRA", "content": "//foo" }, { "type": "NEWLINES", "content": "\n" },
			{ "type": "TABS", "content": "\t\t" }, { "type": "WORD", "content": "C2" }, { "type": "EXTRA", "content": " " }, { "type": "EQUALS", "content": "=" }, { "type": "EXTRA", "content": " " }, { "type": "WORD", "content": "X" },
		])

	def test_deindentation_3(self):
		self.tokenizer_test("deindentation_3", [
			{ "type": "WORD", "content": "AddEffect" }, { "type": "EXTRA", "content": " " }, { "type": "EQUALS", "content": "=" }, { "type": "EXTRA", "content": " " }, { "type": "WORD", "content": "MOPixel" }, { "type": "NEWLINES", "content": "\n" },
			{ "type": "TABS", "content": "\t" }, { "type": "WORD", "content": "PresetName" }, { "type": "EXTRA", "content": " " }, { "type": "EQUALS", "content": "=" }, { "type": "EXTRA", "content": " " }, { "type": "WORD", "content": "Foo" }, { "type": "NEWLINES", "content": "\n" },

			{ "type": "TABS", "content": "\t\t" }, { "type": "WORD", "content": "A1" }, { "type": "EXTRA", "content": " " }, { "type": "EQUALS", "content": "=" }, { "type": "EXTRA", "content": " " }, { "type": "WORD", "content": "X" }, { "type": "NEWLINES", "content": "\n" },
			{ "type": "TABS", "content": "\t" }, { "type": "NEWLINES", "content": "\n" },
			{ "type": "TABS", "content": "\t\t" }, { "type": "WORD", "content": "A2" }, { "type": "EXTRA", "content": " " }, { "type": "EQUALS", "content": "=" }, { "type": "EXTRA", "content": " " }, { "type": "WORD", "content": "X" }, { "type": "NEWLINES", "content": "\n" },

			{ "type": "TABS", "content": "\t\t" }, { "type": "WORD", "content": "B1" }, { "type": "EXTRA", "content": " " }, { "type": "EQUALS", "content": "=" }, { "type": "EXTRA", "content": " " }, { "type": "WORD", "content": "X" }, { "type": "NEWLINES", "content": "\n" },
			{ "type": "TABS", "content": "\t" }, { "type": "EXTRA", "content": " " }, { "type": "NEWLINES", "content": "\n" },
			{ "type": "TABS", "content": "\t\t" }, { "type": "WORD", "content": "B2" }, { "type": "EXTRA", "content": " " }, { "type": "EQUALS", "content": "=" }, { "type": "EXTRA", "content": " " }, { "type": "WORD", "content": "X" }, { "type": "NEWLINES", "content": "\n" },

			{ "type": "TABS", "content": "\t\t" }, { "type": "WORD", "content": "C1" }, { "type": "EXTRA", "content": " " }, { "type": "EQUALS", "content": "=" }, { "type": "EXTRA", "content": " " }, { "type": "WORD", "content": "X" }, { "type": "NEWLINES", "content": "\n" },
			{ "type": "TABS", "content": "\t" }, { "type": "EXTRA", "content": "//foo" }, { "type": "NEWLINES", "content": "\n" },
			{ "type": "TABS", "content": "\t\t" }, { "type": "WORD", "content": "C2" }, { "type": "EXTRA", "content": " " }, { "type": "EQUALS", "content": "=" }, { "type": "EXTRA", "content": " " }, { "type": "WORD", "content": "X" },
		])

	def test_include_files(self):
		self.tokenizer_test("include_files", [
			{ "type": "WORD", "content": "IncludeFile" }, { "type": "EXTRA", "content": " " }, { "type": "EQUALS", "content": "=" }, { "type": "EXTRA", "content": " " }, { "type": "WORD", "content": "A.ini" }, { "type": "NEWLINES", "content": "\n\n" },
			{ "type": "WORD", "content": "IncludeFile" }, { "type": "EXTRA", "content": " " }, { "type": "EQUALS", "content": "=" }, { "type": "EXTRA", "content": " " }, { "type": "WORD", "content": "B.ini" }, { "type": "NEWLINES", "content": "\n" },
		])

		# It's fine that the tokenizer doesn't realize that this is an invalid file, because complex checking is the CST parser's responsibility.

	def test_invalid_tabbing(self):
		self.tokenizer_test("invalid_tabbing", [
			{ "type": "WORD", "content": "AddEffect" }, { "type": "EXTRA", "content": " " }, { "type": "EQUALS", "content": "=" }, { "type": "EXTRA", "content": " " }, { "type": "WORD", "content": "MOPixel" }, { "type": "NEWLINES", "content": "\n" },
			{ "type": "TABS", "content": "\t\t" }, { "type": "WORD", "content": "Foo" }, { "type": "EXTRA", "content": " " }, { "type": "EQUALS", "content": "=" }, { "type": "EXTRA", "content": " " }, { "type": "WORD", "content": "Bar" },
		])

	def test_lstripped_tab(self):
		self.tokenizer_test("lstripped_tab", [
			{ "type": "WORD", "content": "Foo" }, { "type": "EXTRA", "content": " " }, { "type": "EQUALS", "content": "=" }, { "type": "EXTRA", "content": " " }, { "type": "WORD", "content": "Bar" }
		])

	def test_multiple(self):
		self.tokenizer_test("multiple", [
			{ "type": "WORD", "content": "Foo" }, { "type": "EXTRA", "content": " " }, { "type": "EQUALS", "content": "=" }, { "type": "EXTRA", "content": " " }, { "type": "WORD", "content": "Bar" }, { "type": "NEWLINES", "content": "\n" },
			{ "type": "TABS", "content": "\t" }, { "type": "WORD", "content": "Baz" }, { "type": "EXTRA", "content": " " }, { "type": "EQUALS", "content": "=" }, { "type": "EXTRA", "content": " " }, { "type": "WORD", "content": "Bee" }, { "type": "NEWLINES", "content": "\n" },
			{ "type": "WORD", "content": "A" }, { "type": "EXTRA", "content": " " }, { "type": "EQUALS", "content": "=" }, { "type": "EXTRA", "content": " " }, { "type": "WORD", "content": "B" }, { "type": "NEWLINES", "content": "\n" },
			{ "type": "TABS", "content": "\t" }, { "type": "WORD", "content": "C" }, { "type": "EXTRA", "content": " " }, { "type": "EQUALS", "content": "=" }, { "type": "EXTRA", "content": " " }, { "type": "WORD", "content": "D" }, { "type": "NEWLINES", "content": "\n" },
		])

	def test_nested(self):
		self.tokenizer_test("nested", [
			{ "type": "WORD", "content": "Foo" }, { "type": "EXTRA", "content": " " }, { "type": "EQUALS", "content": "=" }, { "type": "EXTRA", "content": " " }, { "type": "WORD", "content": "Bar" }, { "type": "NEWLINES", "content": "\n" },
			{ "type": "TABS", "content": "\t" }, { "type": "WORD", "content": "Baz" }, { "type": "EXTRA", "content": " " }, { "type": "EQUALS", "content": "=" }, { "type": "EXTRA", "content": " " }, { "type": "WORD", "content": "Bee" }, { "type": "NEWLINES", "content": "\n" },
		])

	def test_object_and_property(self):
		self.tokenizer_test("object_and_property", [
			{ "type": "WORD", "content": "Foo" }, { "type": "EXTRA", "content": " " }, { "type": "EQUALS", "content": "=" }, { "type": "EXTRA", "content": " " }, { "type": "WORD", "content": "Bar" }, { "type": "NEWLINES", "content": "\n" },
			{ "type": "TABS", "content": "\t" }, { "type": "WORD", "content": "Baz" }, { "type": "EXTRA", "content": " " }, { "type": "EQUALS", "content": "=" }, { "type": "EXTRA", "content": " " }, { "type": "WORD", "content": "Bee" }, { "type": "NEWLINES", "content": "\n\n" },
			{ "type": "WORD", "content": "IncludeFile" }, { "type": "EXTRA", "content": " " }, { "type": "EQUALS", "content": "=" }, { "type": "EXTRA", "content": " " }, { "type": "WORD", "content": "A.ini" }, { "type": "NEWLINES", "content": "\n" },
		])

	def test_path(self):
		self.tokenizer_test("path", [
			{ "type": "WORD", "content": "FilePath" }, { "type": "EXTRA", "content": " " }, { "type": "EQUALS", "content": "=" }, { "type": "EXTRA", "content": " " }, { "type": "WORD", "content": "A/B" }, { "type": "NEWLINES", "content": "\n" }, { "type": "WORD", "content": "AirResistance" }, { "type": "EXTRA", "content": " " }, { "type": "EQUALS", "content": "=" }, { "type": "EXTRA", "content": " " }, { "type": "WORD", "content": "0.05" }, { "type": "NEWLINES", "content": "\n" }
		])

	def test_simple(self):
		self.tokenizer_test("simple", [
			{ "type": "WORD", "content": "AddEffect" }, { "type": "EXTRA", "content": " " }, { "type": "EQUALS", "content": "=" }, { "type": "EXTRA", "content": " " }, { "type": "WORD", "content": "MOPixel" },
		])

	def test_spaces_at_start_of_line(self):
		self.tokenizer_test("spaces_at_start_of_line", [
			{ "type": "WORD", "content": "Foo" }, { "type": "EXTRA", "content": " " }, { "type": "EQUALS", "content": "=" }, { "type": "EXTRA", "content": " " }, { "type": "WORD", "content": "Bar" }, { "type": "NEWLINES", "content": "\n" },
			{ "type": "EXTRA", "content": "    " }, { "type": "WORD", "content": "Baz" }, { "type": "EXTRA", "content": " " }, { "type": "EQUALS", "content": "=" }, { "type": "EXTRA", "content": " " }, { "type": "WORD", "content": "Bee" },
		])

	def test_spaces(self):
		self.tokenizer_test("spaces", [
			{ "type": "WORD", "content": "Foo" }, { "type": "EXTRA", "content": " " }, { "type": "EQUALS", "content": "=" }, { "type": "EXTRA", "content": " " }, { "type": "WORD", "content": "Bar Baz" },
		])

	def test_traditional(self):
		self.tokenizer_test("traditional", [
			{ "type": "WORD", "content": "[Foo]" }, { "type": "NEWLINES", "content": "\n" },
			{ "type": "WORD", "content": "Bar" }, { "type": "EXTRA", "content": " " }, { "type": "EQUALS", "content": "=" }, { "type": "EXTRA", "content": " " }, { "type": "WORD", "content": "42" }, { "type": "NEWLINES", "content": "\n" },
		])

	def test_value_on_next_line(self):
		self.tokenizer_test("value_on_next_line", [
			{ "type": "WORD", "content": "Foo" }, { "type": "EXTRA", "content": " " }, { "type": "EQUALS", "content": "=" }, { "type": "NEWLINES", "content": "\n" }, { "type": "WORD", "content": "Bar" },
		])

	def tokenizer_test(self, filename, expected):
		filepath = test.get_test_path_from_filename(filename)

		tokens = ini_tokenizer.get_tokens(str(filepath))
		tokens_without_metadata = [ { "type": token["type"], "content": token["content"] } for token in tokens]

		self.assertEqual(tokens_without_metadata, expected)
