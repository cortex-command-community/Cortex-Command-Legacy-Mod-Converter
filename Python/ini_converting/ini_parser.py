def get_parsed_tokens(tokens, parsed, token_idx, depth=0):
	"""
	start -> tabs -> property -> equals -> value -> newline
    ^   v            ^                              v
	|   +------------+                              |
	+-----------------------------------------------+
	"""
	state = "start"

	while token_idx[0] < len(tokens):
		token = tokens[token_idx[0]]

		if state == "start" and token["type"] == "TABS" and is_deeper(depth, token):
			children = { "type": "children", "content": [] }
			parsed[-1].append(children)
			get_parsed_tokens(tokens, children["content"], token_idx, depth + 1)
		elif state == "start" and is_less_deep(depth, token):
			return

		elif state == "start":
			parsed.append([])
			state = "not-start"
		elif state == "not-start" and token["type"] == "TABS":
			parsed[-1].append( { "type": "extra", "content": token["content"] } )
			state = "tabs"
			token_idx[0] += 1
		elif (state == "not-start" or state == "tabs") and token["type"] == "WORD":
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
			state = "start"
			token_idx[0] += 1

		else:
			parsed[-1].append( { "type": "extra", "content": token["content"] } )
			token_idx[0] += 1

	return parsed


def is_less_deep(depth, token):
	return get_depth(token) < depth


def is_deeper(depth, token):
	# TODO: This should throw an error if it's deeper by more than 1.
	return get_depth(token) > depth


def get_depth(token):
	return len(token["content"]) if token["type"] == "TABS" else 0
