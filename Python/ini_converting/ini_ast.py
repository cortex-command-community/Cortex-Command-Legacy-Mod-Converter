def get_ast(cst):
	ast = []

	for a in cst:
		ast.append({})
		b = ast[-1]

		for c in a:
			if c["type"] == "property":
				b["property"] = c["content"]
				break
		for c in a:
			if c["type"] == "value":
				b["value"] = c["content"]
				break
		for c in a:
			if c["type"] == "children":
				b["children"] = get_ast(c["content"])
				break

	return ast
