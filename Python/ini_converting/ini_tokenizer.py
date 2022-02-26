


def get_token_cst(subfolder_path, mod_names):
	"""
	The "cst" in this function's name stands for Concrete Syntax Tree.
	"""
	mod_names = get_mod_names(input_folder_path)

	parsed_portion = {}

	for name in os.listdir(subfolder_path):
		p = subfolder_path / Path(name)

		if not is_mod_folder(p):
			continue
		elif not part_of_mod(p, mod_names): # TODO: Remove this once CCCP has a Mods folder that can be iterated over.
			continue
		elif p.is_file() and p.suffix == ".ini" and p.stem != "desktop": # Skip the desktop.ini Windows metadata file.
			parsed_portion[name] = get_tokens(p.read_text())
		elif p.is_dir():
			parsed_portion[name] = parse(p, mod_names)

	return parsed_portion


def get_mod_names(input_folder_path):
	return [p.name for p in Path(input_folder_path).iterdir() if p.suffix == ".rte" and p.is_dir()]


def part_of_mod(p, mod_names):
	return any(mod_name in str(p) for mod_name in mod_names)


def get_tokens(text):
	tokens = []

	i = 0
	while i < len(text):
		if text[i] == '\t':
			i = tokenize_tabs(i, tokens)
		elif text[i] == ' ':
			i = tokenize_spaces(i, tokens)
		else:
			raise ValueError("This line in the Python code is supposed to be unreachable.")

	return tokens


def tokenize_tabs(i, tokens):
	return i


def tokenize_spaces(i, tokens):
	return i
