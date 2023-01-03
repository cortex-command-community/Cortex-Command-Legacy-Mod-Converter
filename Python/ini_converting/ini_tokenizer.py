import re

# Gets tokens using filepath
def get_tokens(filepath):

    with open(filepath, "r") as f:
        text = f.read().lstrip()

    return get_tokens_from_str(text, filepath)


def get_tokens_from_str(text, filepath=None):
    tokens = []
    text_len = len(text)

    i = 0
    while i < text_len:
        char = text[i]

        if char == "/":
            i = tokenize_comment(i, text_len, text, tokens, filepath)
        elif char == "\t":
            i = tokenize_tabs(i, text_len, text, tokens, filepath)
        elif char == " ":
            i = tokenize_spaces(i, text_len, text, tokens, filepath)
        elif char == "=":
            i = tokenize_equals(i, text_len, text, tokens, filepath)
        elif char == "\n":
            i = tokenize_newline(i, text_len, text, tokens, filepath)
        else:
            i = tokenize_word(i, text_len, text, tokens, filepath)

    return tokens


def get_token(type_, content, i, filepath):
    return {"type": type_, "content": content, "index": i, "filepath": filepath}


def tokenize_comment(i, text_len, text, tokens, filepath):
    if i + 1 < text_len and text[i + 1] == "/":
        return tokenize_single_line_comment(i, text_len, text, tokens, filepath)
    else:
        return tokenize_multi_line_comment(i, text_len, text, tokens, filepath)


def tokenize_single_line_comment(i, text_len, text, tokens, filepath):
    token = ""

    while i < text_len and text[i] != "\n":
        token += text[i]
        i += 1

    tokens.append(get_token("EXTRA", token, i, filepath))

    return i


def tokenize_multi_line_comment(i, text_len, text, tokens, filepath):
    token = ""

    while i < text_len and not (
        text[i] == "*" and i + 1 < text_len and text[i + 1] == "/"
    ):
        token += text[i]
        i += 1

    token += "*/"
    i += 2

    tokens.append(get_token("EXTRA", token, i, filepath))

    return i


def tokenize_tabs(i, text_len, text, tokens, filepath):
    token = ""

    while i < text_len and text[i] == "\t":
        token += text[i]
        i += 1

    tokens.append(get_token("TABS", token, i, filepath))

    return i


def tokenize_spaces(i, text_len, text, tokens, filepath):
    token = ""

    while i < text_len and text[i] == " ":
        token += text[i]
        i += 1

    tokens.append(get_token("EXTRA", token, i, filepath))

    return i


def tokenize_equals(i, text_len, text, tokens, filepath):
    token = ""

    while i < text_len and text[i] == "=":
        token += text[i]
        i += 1

    tokens.append(get_token("EQUALS", token, i, filepath))

    return i


def tokenize_newline(i, text_len, text, tokens, filepath):
    token = ""

    while i < text_len and text[i] == "\n":
        token += text[i]
        i += 1

    tokens.append(get_token("NEWLINES", token, i, filepath))

    return i


def tokenize_word(i, text_len, text, tokens, filepath):
    token = ""

    subtext = text[i:]

    token = re.match("(.+?)\s*(=|\/\/|\/\*|\n)", subtext + "\n").group(1)

    i += len(token)

    tokens.append(get_token("WORD", token, i, filepath))

    return i
