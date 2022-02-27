def get_parsed_tokens(tokens, i=0, parsed=[], depth=0):
	"""
	start -> tabs -> property -> equals -> value -> newline
    ^   v            ^                              v
	|   +------------+                              |
	+-----------------------------------------------+
	"""
	state = "start"

	while i < len(tokens):
		token = tokens[i]

		if state == "start" and token.type == "TABS" and is_deeper(depth, token):
			_, i = get_parsed_tokens(tokens, i + 1, parsed[-1], depth + 1)
		elif state == "start" and token.type == "WORD":
			parsed.append( { "type": "property", "content": token.content } )
			state = "property"
			i += 1
		elif state == "property" and token.type == "EQUALS":
			parsed.append( { "type": "extra", "content": token.content } )
			state = "equals"
			i += 1
		elif state == "equals" and token.type == "WORD":
			parsed.append( { "type": "value", "content": token.content } )
			state = "value"
			i += 1
		elif state == "value" and token.type == "NEWLINES":
			parsed.append( { "type": "extra", "content": token.content } )
			state = "start"
			i += 1

	return parsed, i


def is_deeper(depth, token):
	return get_depth(token.content) > depth


def get_depth(content):
	return len(content)