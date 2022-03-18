def line_contains_property(line_tokens, prop):
	for token in line_tokens:
		if token["type"] == "property" and token["content"] == prop:
			return True
	return False


def line_contains_value(line_tokens, value):
	for token in line_tokens:
		if token["type"] == "value" and token["content"] == value:
			return True
	return False


def line_contains_property_and_value(line_tokens, prop, value):
	return line_contains_property(line_tokens, prop) and line_contains_value(line_tokens, value)


def children_contain_property_shallowly(children, prop):
	for line_tokens in children:
		for token in line_tokens:
			if token["type"] == "property" and token["content"] == prop:
				return True
	return False


def append(foo, depth):
	"""
	This function should replace the .append() calls in ini_rules.py.
	This depth argument should be used to indent stuff the right amount.
	"""