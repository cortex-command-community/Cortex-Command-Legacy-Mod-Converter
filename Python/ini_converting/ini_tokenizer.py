def get_tokens(text):
	tokens = []

	text_len = len(text)

	i = 0
	while i < text_len:
		char = text[i]

		if char == "/":
			i = tokenize_comment(i, text_len, text, tokens)
		elif char == "\t":
			i = tokenize_tabs(i, text_len, text, tokens)
		elif char == " ":
			i = tokenize_spaces(i, text_len, text, tokens)
		elif char == "=":
			i = tokenize_equals(i, text_len, text, tokens)
		elif char == "\n":
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

	tokens.append(get_token("NEWLINES", token)) # TODO: Maybe use "NEWLINE" instead of the plural version?

	return i


def tokenize_word(i, text_len, text, tokens):
	token = ""

	while i < text_len and text[i] not in ("\t =\n") and not (text[i] == "/" and i + 1 < text_len and text[i + 1] == "/"):
		token += text[i]
		i += 1

	tokens.append(get_token("WORD", token))

	return i
