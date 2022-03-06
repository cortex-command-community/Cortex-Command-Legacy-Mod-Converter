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

		if state == "newline" and token["type"] == "EXTRA":
			parsed[-1].append( { "type": "extra", "content": token["content"] } )
			token_idx[0] += 1
		elif state == "newline" and token["type"] == "NEWLINES":
			parsed[-1].append( { "type": "extra", "content": token["content"] } )
			token_idx[0] += 1

		elif state == "newline" and token["type"] == "TABS" and is_deeper(depth, token):
			children = { "type": "children", "content": [] }
			parsed[-1].append(children)
			get_parsed_tokens(tokens, children["content"], token_idx, depth + 1)
		elif state == "newline" and is_less_deep(depth, token):
			return
		elif state == "newline":
			parsed.append([])
			state = "start"

		elif state == "start" and token["type"] == "WORD":
			parsed[-1].append( { "type": "property", "content": token["content"] } )
			state = "property"
			token_idx[0] += 1
		elif state == "property" and token["type"] == "EQUALS":
			parsed[-1].append( { "type": "extra", "content": token["content"] } )
			state = "equals"
			token_idx[0] += 1
		elif state == "equals" and token["type"] == "WORD":
			parsed[-1].append( { "type": "value", "content": token["content"] } )
			state = "value"
			token_idx[0] += 1
		elif state == "value" and token["type"] == "NEWLINES":
			parsed[-1].append( { "type": "extra", "content": token["content"] } )
			state = "newline"
			token_idx[0] += 1

		else:
			parsed[-1].append( { "type": "extra", "content": token["content"] } )
			token_idx[0] += 1

	return parsed


def is_less_deep(depth, token):
	return get_depth(token) < depth


def is_deeper(depth, token):
	new_depth = get_depth(token)
	if new_depth > depth + 1:
		line, column = get_token_pos(token)
		raise ValueError(f"Too many tabs found at line {line}, column {column} in {token['filepath']}")
	return new_depth > depth


def get_depth(token):
	return len(token["content"]) if token["type"] == "TABS" else 0


def get_token_pos(token):
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
