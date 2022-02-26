from pathlib import Path

from Python import utils
from Python import tests
from Python.ini_converting import ini_tokenizer


def tokenizer_tests():
	test("1", [
		("WORD", "AddEffect"), ("EXTRA", " "), ("EQUALS", "="), ("EXTRA", " "), ("WORD", "MOPixel"),
	])
	test("2", [
		("NEWLINES", "\n"),
		("EXTRA", "// foo"), ("NEWLINES", "\n"),
		("EXTRA", "/*a\nb\nc*/"), ("NEWLINES", "\n"),
		("WORD", "AddEffect"), ("EXTRA", "  "), ("EQUALS", "="), ("EXTRA", " "), ("WORD", "MOPixel"), ("EXTRA", "//bar"), ("NEWLINES", "\n"),
		("TABS", "\t"), ("WORD", "PresetName"), ("EXTRA", " "), ("EQUALS", "="), ("EXTRA", "  "), ("WORD", "red_dot_tiny"), ("NEWLINES", "\n"),
		("TABS", "\t\t"), ("WORD", "Mass"), ("EXTRA", "  "), ("EQUALS", "="), ("EXTRA", "  "), ("WORD", "0.0")
	])


def test(filename, expected):
	text = read_test(filename)
	tests.test(text, ini_tokenizer.get_tokens(text), expected)


def read_test(filename):
	return Path(utils.resource_path(f"Python/ini_converting/ini_test_files/{filename}.ini")).read_text()