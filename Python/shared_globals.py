# TODO: Move these to cfg.py
CONVERTER_VERSION = "1.1"
GAME_VERSION = "pre4.0"
NO_PATH_SET_COLOR = "#b35858"
VERSION_STRING = f"-v{CONVERTER_VERSION}-{GAME_VERSION}"
CONVERTER_FOLDER_NAME = "LegacyModConverter" + VERSION_STRING
WARNINGS_MOD_NAME_SEPARATOR = "-" * 50

NO_CHECKMARK = " "
CHECKMARK = "✓"

USER_SETTINGS_BUTTON_MAPPINGS = {
	"Skip conversion": "skip_conversion",
	"Output zips": "output_zips",
	"Play finish sound": "play_finish_sound"
}

NOT_RELEASE = True # This enables tests when set to True, as the release version shouldn't run tests.

sg = None
progress_bar = None