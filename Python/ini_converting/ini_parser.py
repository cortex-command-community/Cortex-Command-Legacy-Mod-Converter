def get_parsed_tokens(tokens, parsed=None, token_idx=None, depth=0):
	"""
	newline -> start -> property -> equals -> value
	^                                         v
	+-----------------------------------------+
	"""

	if parsed == None:
		parsed = []
	if token_idx == None:
		token_idx = [0]

	state = "newline"

	while token_idx[0] < len(tokens):
		token = tokens[token_idx[0]]

		if   state == "newline" and is_deeper(depth, token, tokens, token_idx[0] + 1):
			children = { "type": "children", "content": [], "index": token["index"], "filepath": token["filepath"] }
			append(children, parsed)
			get_parsed_tokens(tokens, children["content"], token_idx, depth + 1)
			# "state" is deliberately not being changed here.
		elif state == "newline" and is_same_depth(depth, token, tokens, token_idx[0] + 1):
			parsed.append([])
			state = "start"
		elif state == "newline" and is_shallower(depth, token, tokens, token_idx[0] + 1):
			return
		elif state == "newline" and (len(parsed) == 0 or token["type"] == "WORD"):
			parsed.append([])
			state = "start"

		elif state == "start" and token["type"] == "WORD":
			append( { "type": "property", "content": token["content"] }, parsed )
			state = "property"
			token_idx[0] += 1
		elif state == "property" and token["type"] == "EQUALS":
			append( { "type": "extra", "content": token["content"] }, parsed )
			state = "equals"
			token_idx[0] += 1
		elif state == "property" and token["type"] == "NEWLINES":
			append( { "type": "extra", "content": token["content"] }, parsed )
			state = "newline"
			token_idx[0] += 1
		elif state == "equals" and token["type"] == "WORD":
			append( { "type": "value", "content": token["content"] }, parsed )
			state = "value"
			token_idx[0] += 1
		elif state == "value" and token["type"] == "NEWLINES":
			append( { "type": "extra", "content": token["content"] }, parsed )
			state = "newline"
			token_idx[0] += 1

		else:
			append( { "type": "extra", "content": token["content"] }, parsed )
			token_idx[0] += 1

	return parsed


def append(token, parsed):
	if len(parsed) == 0:
		token_error(token, "Incorrect tabbing at {line}, column {column} in {filepath}")

	parsed[-1].append(token)


def token_error(token, message):
	line, column = get_token_position(token)
	raise ValueError(message.format(line=line, column=column, filepath=token["filepath"]))


def is_deeper(depth, token, tokens, next_token_idx):
	new_depth = get_depth(token, tokens, next_token_idx)

	if new_depth > depth + 1:
		token_error(token, "Too many tabs found at line {line}, column {column} in {filepath}")
	
	return new_depth > depth


def get_depth(token, tokens, next_token_idx):
	if token["type"] == "NEWLINES":
		return -1
	elif token["type"] == "WORD":
		return 0
	elif token["type"] == "TABS":
		tabs_seen = len(token["content"])
	else:
		tabs_seen = 0

	while next_token_idx < len(tokens):
		next_token = tokens[next_token_idx]

		if next_token["type"] == "WORD":
			return tabs_seen
		elif next_token["type"] == "TABS":
			tabs_seen += len(next_token["content"])
		elif next_token["type"] == "NEWLINES":
			return -1

		next_token_idx += 1
	
	return -1 # Reached when the while-loop read the last character of the file and didn't return.


def is_same_depth(depth, token, tokens, next_token_idx):
	return token["type"] == "TABS" and get_depth(token, tokens, next_token_idx) == depth


def is_shallower(depth, token, tokens, next_token_idx):
	new_depth = get_depth(token, tokens, next_token_idx)
	return new_depth != -1 and new_depth < depth


def get_token_position(token):
	with open(token["filepath"], "r") as f:
		text = f.read()

	line = 1
	column = 1

	for char in text[:token["index"]]:
		if char == '\n':
			line += 1
			column = 0
		else:
			column += 1

	return line, column
