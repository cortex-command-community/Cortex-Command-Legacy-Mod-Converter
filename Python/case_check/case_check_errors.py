# from Python import warnings


def error_could_not_locate(file_name, line_number, couldnt_be_located):
	# This warning doesn't account for the fact that most of the time they are either in files that aren't used, or in commented out lines.
	# warnings.append_mod_warning(file_name, line_number, "Could not locate", couldnt_be_located)
	pass


def error_failed_to_find_module(file_name, line_number, module):
	# This warning doesn't account for the fact that most of the time they are either in files that aren't used, or in commented out lines.
	# warnings.append_mod_warning(file_name, line_number, "Failed to find module", module)
	pass
