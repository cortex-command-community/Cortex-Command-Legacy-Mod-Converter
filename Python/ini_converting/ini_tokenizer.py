


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

	text_len = len(text)

	i = 0
	while i < text_len:
		if text[i] == "/":
			i = tokenize_comment(i, text_len, text, tokens)
		elif text[i] == "\t":
			i = tokenize_tabs(i, text_len, text, tokens)
		elif text[i] == " ":
			i = tokenize_spaces(i, text_len, text, tokens)
		elif text[i] == "=":
			i = tokenize_equals(i, text_len, text, tokens)
		elif text[i] == "\n":
			i = tokenize_newline(i, text_len, text, tokens)
		else:
			i = tokenize_word(i, text_len, text, tokens)

	return tokens


def get_token(type_, content):
	return { "type": type_, "content": content }


def tokenize_comment(i, text_len, text, tokens):
	if i + 1 < text_len and text[i + 1] == "/":
		return tokenize_single_line_comment(i, text_len, text, tokens)
	else:
		return tokenize_multi_line_comment(i, text_len, text, tokens)


def tokenize_single_line_comment(i, text_len, text, tokens):
	token = ""

	while i < text_len and text[i] != "\n":
		token += text[i]
		i += 1

	tokens.append(get_token("EXTRA", token))

	return i


def tokenize_multi_line_comment(i, text_len, text, tokens):
	token = ""

	while i < text_len and not (text[i] == "*" and i + 1 < text_len and text[i + 1] == "/"):
		token += text[i]
		i += 1

	token += "*/"
	i += 2

	tokens.append(get_token("EXTRA", token))

	return i


def tokenize_tabs(i, text_len, text, tokens):
	token = ""

	while i < text_len and text[i] == "\t":
		token += text[i]
		i += 1

	tokens.append(get_token("TABS", token))

	return i


def tokenize_spaces(i, text_len, text, tokens):
	token = ""

	while i < text_len and text[i] == " ":
		token += text[i]
		i += 1

	tokens.append(get_token("EXTRA", token))

	return i


def tokenize_equals(i, text_len, text, tokens):
	token = ""

	while i < text_len and text[i] == "=":
		token += text[i]
		i += 1

	tokens.append(get_token("EQUALS", token))

	return i


def tokenize_newline(i, text_len, text, tokens):
	token = ""

	while i < text_len and text[i] == "\n":
		token += text[i]
		i += 1

	tokens.append(get_token("NEWLINES", token))

	return i


def tokenize_word(i, text_len, text, tokens):
	token = ""

	while i < text_len and text[i] not in ("\t =\n") and not (text[i] == "/" and i + 1 < text_len and text[i + 1] == "/"):
		token += text[i]
		i += 1

	tokens.append(get_token("WORD", token))

	return i
