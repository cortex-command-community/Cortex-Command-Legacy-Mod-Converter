from Python.ini_converting import ini_tokenizer_tests
from Python.ini_converting import ini_cst_tests
from Python.ini_converting import ini_ast_tests


def run():
	ini_tokenizer_tests.tokenizer_tests()
	ini_cst_tests.cst_tests()
	ini_ast_tests.ast_tests()