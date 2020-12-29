import re

from Python import warnings


def regex_replace(all_lines):
	all_lines = simple_replace(all_lines, "Framerate = (.*)", "SpriteAnimMode = 7")
	all_lines = simple_replace(all_lines, "\tPlayerCount = (.*)\n", "")
	all_lines = simple_replace(all_lines, "\tTeamCount = (.*)\n", "")

	all_lines = specific_replace(all_lines, regex_replace_particle, False, "ParticleNumberToAdd = (.*)\n\tAddParticles = (.*)\n\t\tCopyOf = (.*)\n", "AddGib = Gib\n\t\tGibParticle = {}\n\t\t\tCopyOf = {}\n\t\tCount = {}\n")
	
	all_lines = specific_replace(all_lines, regex_replace_sound_priority, True, "SoundContainer(((?!SoundContainer).)*)Priority", "SoundContainer{}// Priority")

	# all_lines = specific_replace(all_lines, regex_replace_sound_priority, True, "AddSound(((?! AddSound).)*)Priority", "AddSound{}// Priority")
	
	all_lines = specific_replace(all_lines, regex_use_capture, False, "FundsOfTeam(.*) =", "Team{}Funds =")
	# all_lines = specific_replace(all_lines, regex_replace_playsound, False, "", "")

	return all_lines


def simple_replace(all_lines, pattern, replacement):
	matches = re.findall(pattern, all_lines)
	if len(matches) > 0:
		return re.sub(pattern, replacement, all_lines)
	return all_lines


def specific_replace(all_lines, fn, dotall, pattern, replacement):
	# TODO: Refactor so .findall takes re.DOTALL as an argument directly.
	if dotall:
		matches = re.findall(pattern, all_lines, re.DOTALL)
	else:
		matches = re.findall(pattern, all_lines)
	if len(matches) > 0:
		return fn(all_lines, pattern, replacement, matches)
	return all_lines


def regex_replace_particle(all_lines, pattern, replacement, matches):
	# matches == [(4, "foo", "bar"), (2, "baz", "bee")]
	new = [item for tup in matches for item in tup]
	# new == [4, "foo", "bar", 2, "baz", "bee"]

	# 0, 1, 2 -> 1, 2, 0
	new[0::3], new[1::3], new[2::3] = \
	new[1::3], new[2::3], new[0::3]
	
	# new == ["foo", "bar", 4, "baz", "bee", 2]
	return re.sub(pattern, replacement, all_lines).format(*new)


def regex_replace_sound_priority(all_lines, pattern, replacement, matches):
	# TODO: This pattern returns two items in each tuple, while we only need the first. Create a better pattern.
	# https://stackoverflow.com/a/406408/13279557
	# https://regex101.com/r/NdKaWs/2

	# matches == [(4, "foo"), (2, "bar")]
	new = [item for tup in matches for item in tup][::2]
	# new == [4, 2]
	return re.sub(pattern, replacement, all_lines, flags=re.DOTALL).format(*new)


def regex_use_capture(all_lines, pattern, replacement, matches):
	return re.sub(pattern, replacement, all_lines).format(*matches)


# def regex_replace_playsound(all_lines, pattern, replacement, matches):
# 	return all_lines
# 	# TODO:
# 	# AudioMan:PlaySound("ModName.rte/Folder/SoundName.wav", SceneMan:TargetDistanceScalar(self.Pos), false, true, -1)
# 	# to
#	# AudioMan:PlaySound("ModName.rte/Folder/SoundName.wav", self.Pos)	-- Cut everything and leave the thing inside the brackets after SceneMan:TargetDistanceScalar


def regex_replace_bmps_and_wavs(all_lines):
	# TODO: Combine these four patterns into two.
	all_lines = specific_replace(all_lines, regex_use_capture, False, "Base\.rte(.*?)\.bmp", "Base.rte{}.png")
	all_lines = specific_replace(all_lines, regex_use_capture, False, "base\.rte(.*?)\.bmp", "Base.rte{}.png")
	all_lines = specific_replace(all_lines, regex_use_capture, False, "Base\.rte(.*?)\.wav", "Base.rte{}.flac")
	all_lines = specific_replace(all_lines, regex_use_capture, False, "base\.rte(.*?)\.wav", "Base.rte{}.flac")
	return all_lines


def playsound_warning(line, file_path, line_number):
	pattern = "PlaySound(.*)"
	message = "No longer supported. Create a SoundContainer with CreateSoundContainer in the appropriate Create function."
	matches = re.findall(pattern, line)
	if len(matches) > 0 and matches[0].count(",") > 2:
		warnings.warning_results.append("'{}' line {}: {} -> {}".format(file_path, line_number, pattern, message))