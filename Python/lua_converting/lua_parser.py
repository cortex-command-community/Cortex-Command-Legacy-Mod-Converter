# TODO:
# Recreate ini_parser.py, ini_rules.py and ini_writer.py for lua_parser.py, lua_rules.py and lua_writer.py
# See this Activity.NOTEAM GitHub Issue:
# https://github.com/cortex-command-community/Cortex-Command-Legacy-Mod-Converter/issues/109

# from enum import Enum, auto


# class State(Enum):
# 	POSSIBLE_MULTI_ENDING = auto()


# def convert(line):
# 	parsed = parse(line)
# 	line = convert(parsed)
# 	return line


# def parse(line):
# 	"""
# 	local found = SceneMan:CastMORay(Vector(self.Pos.X, self.Pos.Y + self.gunOffset), Vector(distX, distY), self.ID, 128, false, 2);
# 	->
# 	[
# 		{ "type": "extra", "content": "local found = SceneMan:CastMORay(" },
# 		{ "type": "children", "content": [

# 		]},
# 		{ "type": "extra", "content": "\t" },
# 	]
# 	Vector(self.Pos.X, self.Pos.Y + self.gunOffset), Vector(distX, distY), self.ID, 128, false, 2);
# 	"""
# 	parsed = []

# 	state = State.NOT_IN_A_COMMENT
# 	for char in line:

# 	return parsed


# def convert(parsed):
# 	line = ""
# 	return line