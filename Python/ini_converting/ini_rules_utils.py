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

# Checks if a line contains a value from a iterable of values
# Returns the value found, otherwise returns None
def line_contains_any_values(line_tokens, values):
	for token in line_tokens:
		if (token["type"] == "value" and token["content"] in values):
			return token["content"]
	return None
# Gets all children and their index with a property, 
def get_children_with_property_shallow(children, prop):
	matches = []
	for i,x in enumerate(children):
		p = line_contains_property(x, prop)
		if (p): 
			matches.append((i, x))
	
	return matches

def get_section_property_value(section, property):
	for x in section:
		val = get_line_property_value(x, property)		
		if (val): return val
	
	return None

def get_line_property_value(line, property):
	for x in line:
		t, c = (x["type"], x["content"])
		if (t == "property" and c != property):
			return None
		if (t == "value"): 
			return (c, line)
			
	return None

def get_values_of_properties_of_children_shallowly(children, prop):
	matches = [None] * len(children)
	for i,child in enumerate(children):
		c_props = get_children(child)
		if (c_props):
			matches[i] = get_section_property_value(c_props, prop)
			

	return matches

def set_line_value(line, val):
	for i, x in enumerate(line):
		t, c = (x["type"], x["content"])
		if (t == "value"):
			line[i]["content"] = str(val)

# Indent lines or sections
def indent(section: list, count=1, recursive=True):
	t,c = (section[0]["type"], section[0]["content"])
	if (t == "extra" and '\t' in c):
		section[0]["content"] = c + ('\t' * count)
	else:
		section.insert(0, {"type": "extra", "content": ("\t"*count) })
	
	if (not recursive): return

	children = get_children(section)
	if (children):
		for x in children:
			indent(x, count)


def get_indent(line):
	if len(line) == 0: return 
	t,c = (line[0]["type"], line[0]["content"])
	if t == "extra" and "\t" in c:
		return len(c)
	return 0
		

def get_children(section):
	if (has_children(section)):
		return section[-1]["content"]
	return None

def has_children(section):
	return section[-1]['type'] == 'children'

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