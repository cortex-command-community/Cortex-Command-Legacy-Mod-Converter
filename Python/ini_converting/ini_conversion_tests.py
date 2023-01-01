import os
from Python.ini_converting import ini_writer
from Python.ini_converting import ini_cst
from Python.ini_converting import ini_tokenizer
from Python.ini_converting import ini_rules

INPUT_FILE_SUFFIX = "_in.ini"
EXPECTED_FILE_SUFFIX = "_out.ini"
RESULT_FILE_SUFFIX = "_result.ini"

TEST_DIR = "Python/ini_converting/ini_test_files/output_tests/"


class ConversionTestFailed(Exception):
    pass
class MissingInputTestFile(Exception):
    pass
class MissingOutputTestFile(Exception):
    pass

def conversion_tests():
    
    in_files = {}
    out_files = {}

    # Get all tests, raise an exception if one is missing.
    for filepath in os.listdir(TEST_DIR):
        if (filepath.endswith(INPUT_FILE_SUFFIX)):
            in_files[filepath] = True
        elif (filepath.endswith(EXPECTED_FILE_SUFFIX)):
            out_files[filepath] = True

    if (len(out_files) < len(in_files)):
        raise MissingOutputTestFile("Missing output test file(s):" + str(in_files - out_files))
    elif (len(out_files) > len(in_files)):
        raise MissingInputTestFile("Missing input test file(s): " + str(out_files - in_files))
    
    # Run all tests.
    for in_file in in_files:
        test_name = in_file.replace(INPUT_FILE_SUFFIX, "")
        out_file = in_file.replace(INPUT_FILE_SUFFIX, EXPECTED_FILE_SUFFIX)
        if (not os.path.isfile(TEST_DIR + out_file)):
            raise MissingOutputTestFile("Missing output test file: " + out_file)
        else:
            print("Running test " + test_name, end="...\n\t")
            with open(TEST_DIR + in_file, "r") as f:
                # We don't care about spaces at the end of a file
                in_str = f.read().rstrip()
            with open(TEST_DIR + out_file, "r") as f:
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
            result_file = TEST_DIR + in_file.replace(INPUT_FILE_SUFFIX, RESULT_FILE_SUFFIX)
            with(open(result_file, "w")) as f:
                f.write(result)

            if (result != out_str):
                raise ConversionTestFailed("Failed!")
            else:
                print("Passed!")


