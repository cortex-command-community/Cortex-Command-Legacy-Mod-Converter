import os, re
import pprint
from pathlib import Path
from enum import Enum, auto

from Python.reading_types import ReadingTypes


class CommentState(Enum):
	NOT_IN_A_COMMENT       = auto()
	POSSIBLE_COMMENT_START = auto()
	INSIDE_SINGLE_COMMENT  = auto()
	INSIDE_MULTI_COMMENT   = auto()
	POSSIBLE_MULTI_ENDING  = auto()


def parse_token_cst():
	pass


# TODO: Why does convert.py already have a function with the same name?
# def is_mod_folder(p):
# 	return ".rte" in str(p)


def parse_file_recursively(parsed_portion, f, depth_tab_count=0):
	"""
	# CC and CCCP use a custom INI format, so the configparser library can't be used to parse the INI files.
	# TODO: Check if the first line can be tabbed, because then prev_line_index needs to be initialized to 0.
	"""

	for line_number, line in enumerate(f, start=1):
		line = line.strip("\n")

		line_tokens, tab_count = get_tokenized_line(line, depth_tab_count)
		# print(line_tokens)

		if tab_count == depth_tab_count:
			parsed_portion.append(line_tokens)
		elif tab_count == depth_tab_count + 1:
			if parsed_portion == []:
				file_path = f.name
				raise TabError(f"\nWrong tabbing on line {line_number} in file {file_path} on line '{line}'")

			previous_appended_line_tokens = parsed_portion[-1]

			previous_appended_line_tokens.append( { "type": "lines_tokens", "content": [ line_tokens ] } )

			child_line_tokens = previous_appended_line_tokens[-1]["content"]

			child_return_values = parse_file_recursively(child_line_tokens, f, depth_tab_count+1)

			if child_return_values != None and child_return_values["tab_count"] == depth_tab_count:
				parsed_portion.append(child_return_values["line_tokens"])
			else:
				return child_return_values
		elif tab_count < depth_tab_count:
			child_return_values = { "line_tokens": line_tokens, "tab_count": tab_count }
			return child_return_values


# This global variable is necessary due to how a deep function call needs to be able to also change this variable for the less deep function calls.
# Passing it as a function argument would copy it by value instead of by reference.
# multiline = False

def get_tokenized_line(line, depth_tab_count):
	"""
	The returned line_tokens looks like this:
	[
		{ "type": "extra", "content": "\t" },
		{ "type": "property", "content": "Mass" },
		{ "type": "value", "content": "2400" },
		{ "type": "extra", "content": " /* */ foo /*" },
	]

	CCCP INI parser quirks to keep in mind:
	1.
		This works:
			Mass = 2400 /*
		foo
			*/ MaxInventoryMass = 3200

		while this crashes the game:
			Mass = 2400 // /*
		foo
			*/ MaxInventoryMass = 3200
	2.
		This works:
			/*
		foo
			// */ Mass = 2400

		while this crashes the game:
			/*
		foo
			// */ bar
	"""

	line_tokens = []

	comment_state = CommentState.NOT_IN_A_COMMENT

	string = ""
	unidentified_string = ""

	seen_equals = False
	added_property = False
	seen_non_whitespace = False

	for char in line:
		if   char == "/" and comment_state == CommentState.POSSIBLE_COMMENT_START and string != "" and seen_equals:
			comment_state = CommentState.INSIDE_SINGLE_COMMENT
			add_token(line_tokens, ReadingTypes.VALUE, string)
			unidentified_string += char
			string = ""
		elif char == "/" and comment_state == CommentState.POSSIBLE_COMMENT_START and string != "" and not seen_equals:
			comment_state = CommentState.INSIDE_SINGLE_COMMENT
			add_token(line_tokens, ReadingTypes.PROPERTY, string)
			unidentified_string += char
			string = ""
		elif char == "/" and comment_state == CommentState.POSSIBLE_COMMENT_START and string == "":
			comment_state = CommentState.INSIDE_SINGLE_COMMENT
			unidentified_string += char
		elif char == "*" and comment_state == CommentState.POSSIBLE_COMMENT_START:
			comment_state = CommentState.INSIDE_MULTI_COMMENT
			unidentified_string += char
		elif char == "*" and comment_state == CommentState.INSIDE_MULTI_COMMENT:
			comment_state = CommentState.POSSIBLE_MULTI_ENDING
			unidentified_string += char
		elif char == "/" and comment_state == CommentState.POSSIBLE_MULTI_ENDING:
			comment_state = CommentState.NOT_IN_A_COMMENT
			unidentified_string += char
		elif char == "/" and comment_state == CommentState.NOT_IN_A_COMMENT:
			comment_state = CommentState.POSSIBLE_COMMENT_START
			unidentified_string += char
		elif comment_state == CommentState.INSIDE_SINGLE_COMMENT or comment_state == CommentState.INSIDE_MULTI_COMMENT:
			unidentified_string += char
		elif char.isspace():
			unidentified_string += char
		elif char == "=":
			seen_equals = True
			unidentified_string += char
		elif unidentified_string != "" and seen_equals and not added_property:
			comment_state = CommentState.NOT_IN_A_COMMENT
			add_token(line_tokens, ReadingTypes.PROPERTY, string)
			added_property = True
			string = char
			add_token(line_tokens, ReadingTypes.EXTRA, unidentified_string)
			unidentified_string = ""
		elif seen_non_whitespace:
			comment_state = CommentState.NOT_IN_A_COMMENT
			string += unidentified_string + char
			unidentified_string = ""
		elif unidentified_string == "":
			seen_non_whitespace = True
			string += char
		else:
			seen_non_whitespace = True
			string += char
			add_token(line_tokens, ReadingTypes.EXTRA, unidentified_string)
			unidentified_string = ""

	if seen_equals and line != "" and unidentified_string != "" and string != "":
		add_token(line_tokens, ReadingTypes.VALUE, string)
		add_token(line_tokens, ReadingTypes.EXTRA, unidentified_string)
	elif seen_equals and line != "" and unidentified_string != "":
		add_token(line_tokens, ReadingTypes.EXTRA, unidentified_string)
	elif seen_equals and line != "" and string != "":
		add_token(line_tokens, ReadingTypes.VALUE, string)
	elif line != "" and unidentified_string != "" and string != "":
		add_token(line_tokens, ReadingTypes.PROPERTY, string)
		add_token(line_tokens, ReadingTypes.EXTRA, unidentified_string)
	elif line != "" and unidentified_string != "":
		add_token(line_tokens, ReadingTypes.EXTRA, unidentified_string)
	elif line != "" and string != "":
		add_token(line_tokens, ReadingTypes.PROPERTY, string)
	elif line == "":
		pass
	else:
		raise ValueError("This line in the Python code is supposed to be unreachable.")

	tab_count = depth_tab_count

	return line_tokens, tab_count


def add_token(line_tokens, type_, content):
	line_tokens.append({ "type": type_, "content": content })