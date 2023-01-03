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
        if token["type"] == "value" and token["content"] in values:
            return token["content"]
    return None


# Gets all children and their index with a property,
def get_children_with_property_shallow(section, prop) -> list:
    children = get_children(section)
    matches = []
    for i, x in enumerate(children):
        p = line_contains_property(x, prop)
        if p:
            matches.append((i, x))

    return matches


# Gets all children and their index with a property and value
def get_children_with_property_and_value_shallow(section, prop, val) -> list:
    children = get_children(section)
    return get_lines_with_property_and_value(children, prop, val)


def get_lines_with_property_and_value(children, prop, val) -> list:
    matches = []
    for i, child in enumerate(children):
        p = line_contains_property_and_value(child, prop, val)
        if p:
            matches.append((i, child))

    return matches


def get_section_property_value(section, property):
    for x in section:
        val = get_line_property_value(x, property)
        if val:
            return val

    return None


def get_line_property(line):
    for token in line:
        if token["type"] == "property":
            return token["content"]


def get_line_property_value(line, property):
    for x in line:
        t, c = (x["type"], x["content"])
        if t == "property" and c != property:
            return None
        if t == "value":
            return (c, line)

    return None


# removes all of a property from a section
def remove_property_from_section(section, property):
    children = get_children(section)

    for i in range(len(children) - 1, -1, -1):
        if line_contains_property(children[i], property):
            children.pop(i)


# removes all of any property in properties from a section
def remove_properties_from_section(section, properties):
    children = get_children(section)

    for i in range(len(children) - 1, -1, -1):
        prop = get_line_property(children[i])
        if prop in properties:
            children.pop(i)


def get_values_of_properties_of_children_shallowly(section, prop):
    matches = [None] * len(section)
    for i, child in enumerate(section):
        c_props = get_children(child)
        if c_props:
            matches[i] = get_section_property_value(c_props, prop)

    return matches


def set_line_value(line, val):
    for i, x in enumerate(line):
        t, c = (x["type"], x["content"])
        if t == "value":
            line[i]["content"] = str(val)


# Indent lines or sections
def indent(section: list, count=1, recursive=True):
    t, c = (section[0]["type"], section[0]["content"])
    if t == "extra" and "\t" in c:
        section[0]["content"] = c + ("\t" * count)
    else:
        section.insert(0, {"type": "extra", "content": ("\t" * count)})

    if not recursive:
        return

    children = get_children(section)
    if children:
        for x in children:
            indent(x, count)


def get_indent(line):
    if len(line) == 0:
        return
    t, c = (line[0]["type"], line[0]["content"])
    if t == "extra" and "\t" in c:
        return len(c)
    return 0


def get_children(section):
    if has_children(section):
        return section[-1]["content"]
    return None


def has_children(section):
    return "type" in section[-1] and section[-1]["type"] == "children"


def line_contains_property_and_value(line_tokens, prop, value):
    hasProp = False
    for token in line_tokens:
        if not hasProp and token["type"] == "property" and token["content"] == prop:
            hasProp = True
        elif token["type"] == "value" and token["content"] == value:
            return True

    return False


def children_contain_property_shallowly(children, prop):
    for line_tokens in children:
        for token in line_tokens:
            if token["type"] == "property" and token["content"] == prop:
                return True
    return False


def change_line_property(line, prop):
    for i, token in enumerate(line):
        if token["type"] == "property":
            line[i]["content"] = prop
            return
    # TODO
    raise ValueError("Property doesn't exist in the line!")


def change_line_value(line, val):
    for i, token in enumerate(line):
        if token["type"] == "value":
            line[i]["content"] = val
            return

    raise ValueError("Value doesn't exist in the line!")


# replace the value of line if property (and value) matches, ignores children
def replace_value_of_property(line, prop, val, oldVal=None):
    hasProp = False
    for i, token in enumerate(line):
        t = token["type"]
        c = token["content"]
        if not hasProp:
            if t == "children":
                return
            if t == "property" and c == prop:
                hasProp = True
        else:
            if t == "value":
                if (oldVal and oldVal == c) or not oldVal:
                    line[i][t] = val


def replace_property_names_of_children_shallowly(section, oldProp, newProp):
    children = get_children(section)
    for child in children:
        for i, token in enumerate(child):
            t = token["type"]
            c = token["content"]
            if t == "property":
                if c == oldProp:
                    child[i]["content"] = newProp
                break


def append(foo, depth):
    """
    This function should replace the .append() calls in ini_rules.py.
    This depth argument should be used to indent stuff the right amount.
    """
