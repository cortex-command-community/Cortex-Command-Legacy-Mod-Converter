def get_parsed_tokens(tokens, parsed, i=0, depth=0):
	"""
	start -> tabs -> property -> equals -> value -> newline
    ^   v            ^                              v
	|   +------------+                              |
	+-----------------------------------------------+
	"""
	state = "start"

	while i < len(tokens):
		token = tokens[i]

		if state == "start" and token["type"] == "TABS" and is_less_deep(depth, token):
			return parsed, i
		elif state == "start" and token["type"] == "TABS" and is_deeper(depth, token):
		# elif state == "start" and token["type"] == "TABS":
			parsed.append( { "type": "lines_tokens", "content": [] } )
			_, i = get_parsed_tokens(tokens, parsed[-1]["content"], i, depth + 1)
		elif state == "start" and token["type"] == "TABS":
			parsed.append( { "type": "extra", "content": token["content"] } )
			state = "tabs"
			i += 1
		elif state == "tabs" and token["type"] == "WORD":
			parsed.append( { "type": "property", "content": token["content"] } )
			state = "property"
			i += 1
		elif state == "start" and token["type"] == "WORD" and depth == 0:
			parsed.append( { "type": "property", "content": token["content"] } )
			state = "property"
			i += 1
		elif state == "start" and token["type"] == "WORD":
			return parsed, i
		elif state == "property" and token["type"] == "EQUALS":
			parsed.append( { "type": "extra", "content": token["content"] } )
			state = "equals"
			i += 1
		elif state == "equals" and token["type"] == "WORD":
			parsed.append( { "type": "value", "content": token["content"] } )
			state = "value"
			i += 1
		elif state == "value" and token["type"] == "NEWLINES":
			parsed.append( { "type": "extra", "content": token["content"] } )
			state = "start"
			i += 1
		else:
			parsed.append( { "type": "extra", "content": token["content"] } )
			i += 1

	return [parsed], i


def is_less_deep(depth, token):
	return get_depth(token["content"]) < depth


# def is_deeper(depth, token):
# 	# TODO: This should throw an error if it's deeper by more than 1.
# 	return get_depth(token["content"]) > depth


def get_depth(content):
	return len(content)