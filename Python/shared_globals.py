# TODO: Move these to cfg.py
CONVERTER_VERSION = "1.2"
GAME_VERSION = "pre4.0"
NO_PATH_SET_COLOR = "#b35858"

VERSION_STRING = f"-v{CONVERTER_VERSION}-{GAME_VERSION}"
# TODO: Use this for pre4.1!
# VERSION_STRING = f"-{GAME_VERSION}-v{CONVERTER_VERSION}"

CONVERTER_FOLDER_NAME = "LegacyModConverter" + VERSION_STRING
WARNINGS_MOD_NAME_SEPARATOR = "-" * 50
ARBITRARILY_HIGH_DEFAULT_GRIP_STRENGTH = 424242

INPUT_DIR = "Input"
OUTPUT_DIR = "Output"

INPUT_DIR_USES_CC_FOLDER = False
OUTPUT_DIR_IS_RELATIVE_TO_INPUT = False

NOT_RELEASE = True  # This enables tests when set to True, as the release version shouldn't run tests.

sg = None
progress_bar = None
