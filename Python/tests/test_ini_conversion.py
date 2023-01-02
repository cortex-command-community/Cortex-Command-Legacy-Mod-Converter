import os, unittest

from Python.ini_converting import ini_writer, ini_cst, ini_tokenizer, ini_rules


class TestINIConversion(unittest.TestCase):
	INPUT_FILE_SUFFIX = "_in.ini"
	EXPECTED_FILE_SUFFIX = "_out.ini"
	RESULT_FILE_SUFFIX = "_result.ini"

	TEST_DIR = "Python/tests/ini_test_files/output_tests/"

	class MissingInputTestFile(Exception):
		pass
	class MissingOutputTestFile(Exception):
		pass

	def test_conversions(self):
		in_files = {}
		out_files = {}

		# Get all tests, raise an exception if one is missing.
		for filepath in os.listdir(self.TEST_DIR):
			if (filepath.endswith(self.INPUT_FILE_SUFFIX)):
				in_files[filepath] = True
			elif (filepath.endswith(self.EXPECTED_FILE_SUFFIX)):
				out_files[filepath] = True

		if (len(out_files) < len(in_files)):
			raise self.MissingOutputTestFile("Missing output test file(s):" + str(in_files - out_files))
		elif (len(out_files) > len(in_files)):
			raise self.MissingInputTestFile("Missing input test file(s): " + str(out_files - in_files))

		# Run all tests.
		for in_file in in_files:
			# test_name = in_file.replace(self.INPUT_FILE_SUFFIX, "")
			out_file = in_file.replace(self.INPUT_FILE_SUFFIX, self.EXPECTED_FILE_SUFFIX)
			if (not os.path.isfile(self.TEST_DIR + out_file)):
				raise self.MissingOutputTestFile("Missing output test file: " + out_file)
			else:
				with open(self.TEST_DIR + in_file, "r") as f:
					# We don't care about spaces at the end of a file
					in_str = f.read().rstrip()
				with open(self.TEST_DIR + out_file, "r") as f:
					# We don't care about spaces at the end of a file
					out_str = f.read().rstrip()

				# tokenize the file contents, generate CST for applying rules
				tokens = ini_tokenizer.get_tokens_from_str(in_str, in_file)
				cst = ini_cst.get_cst(tokens)
				ini_rules.apply_rules_on_sections([cst[0]], None)
				tokens = []
				for section in cst:
					ini_writer.write_recursively(section, tokens)

				result = "".join(tokens).rstrip()
				result_file = self.TEST_DIR + in_file.replace(self.INPUT_FILE_SUFFIX, self.RESULT_FILE_SUFFIX)
				with(open(result_file, "w")) as f:
					f.write(result)

				self.assertEqual(result, out_str)
