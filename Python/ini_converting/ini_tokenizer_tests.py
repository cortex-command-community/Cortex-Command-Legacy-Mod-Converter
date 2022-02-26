from pathlib import Path

from Python import tests
from Python.ini_converting import ini_tokenizer


def tokenizer_tests():
	test("1", {})


def test(filename, expected):
	file_text = read_test(filename)
	tests.test(file_text, ini_tokenizer.get_tokens(file_text), expected)


def read_test(filename):
	return ("Python/ini_converting/ini_tokenizer_test_files" / Path(filename + ".ini")).read_text()