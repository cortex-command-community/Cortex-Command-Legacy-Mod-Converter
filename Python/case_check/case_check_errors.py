from Python import warnings


def error_could_not_locate(file_name, line_number, couldnt_be_located):
	warnings.warning_results.append(get_error_line(file_name, line_number, "Could not locate", couldnt_be_located))


def error_failed_to_find_module(file_name, line_number, module):
	warnings.warning_results.append(get_error_line(file_name, line_number, "Failed to find module", module))


def get_error_line(file_name, line_number, error, error_subject):
	return f"\nLine {line_number} at {file_name}\n\t{error}: {error_subject}"