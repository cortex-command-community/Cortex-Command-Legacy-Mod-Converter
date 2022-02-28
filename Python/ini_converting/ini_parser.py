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

		if state == "start" and token["type"] == "TABS" and is_less_deep(depth, token):
			return
		elif state == "start" and token["type"] == "TABS" and is_deeper(depth, token):
			parsed.append( { "type": "lines_tokens", "content": [] } )
			get_parsed_tokens(tokens, parsed[-1]["content"], token_idx, depth + 1)
		elif state == "start" and token["type"] == "TABS":
			parsed.append( [ { "type": "lines_tokens", "content": [] } ] )
			token_idx[0] += 1
			get_parsed_tokens(tokens, parsed[-1], token_idx, depth)
		elif (state == "start" or state == "tabs") and token["type"] == "WORD":
			parsed.append( { "type": "property", "content": token["content"] } )
			state = "property"
			token_idx[0] += 1
		elif state == "property" and token["type"] == "EQUALS":
			parsed.append( { "type": "extra", "content": token["content"] } )
			state = "equals"
			token_idx[0] += 1
		elif state == "equals" and token["type"] == "WORD":
			parsed.append( { "type": "value", "content": token["content"] } )
			state = "value"
			token_idx[0] += 1
		elif state == "value" and token["type"] == "NEWLINES":
			parsed.append( { "type": "extra", "content": token["content"] } )
			state = "start"
			token_idx[0] += 1
		else:
			parsed.append( { "type": "extra", "content": token["content"] } )
			token_idx[0] += 1

	return parsed


def is_less_deep(depth, token):
	return get_depth(token["content"]) < depth


def is_deeper(depth, token):
	# TODO: This should throw an error if it's deeper by more than 1.
	return get_depth(token["content"]) > depth


def get_depth(content):
	return len(content)