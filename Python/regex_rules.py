import re

from Python import warnings


def regex_replace(all_lines):
	all_lines = replace_without_using_matches(all_lines, "Framerate = (.*)", "SpriteAnimMode = 7")
	all_lines = replace_without_using_matches(all_lines, "\tPlayerCount = (.*)\n", "")
	all_lines = replace_without_using_matches(all_lines, "\tTeamCount = (.*)\n", "")
	
	all_lines = replace_using_matches(all_lines, "ModuleName = (.*) Tech\n", "ModuleName = {}\n\tIsFaction = 1\n")
	all_lines = replace_using_matches(all_lines, "FundsOfTeam(.*) =", "Team{}Funds =")
	all_lines = replace_using_matches(all_lines, "[bB]ase\.rte(.*?)\.wav", "Base.rte{}.flac")

	all_lines = special_replace_using_matches(all_lines, regex_replace_particle, "ParticleNumberToAdd = (.*)\n\tAddParticles = (.*)\n\t\tCopyOf = (.*)\n", "AddGib = Gib\n\t\tGibParticle = {}\n\t\t\tCopyOf = {}\n\t\tCount = {}\n", dotall=False)
	all_lines = special_replace_using_matches(all_lines, regex_replace_sound_priority, "SoundContainer(((?!SoundContainer).)*)Priority", "SoundContainer{}// Priority", dotall=True)
	# all_lines = special_replace_using_matches(all_lines, regex_replace_sound_priority, "AddSound(((?! AddSound).)*)Priority", "AddSound{}// Priority", dotall=True)
	# all_lines = special_replace_using_matches(all_lines, regex_replace_playsound, "", "", dotall=False)
	
	# TODO: Clean this mess up.
	# Mass and MaxMass can be mentioned in either order, so that's why there are two nearly identical lines below.
	# all_lines = special_replace_using_matches(all_lines, regex_replace_max_mass_1,
	# 	"AddEffect = ACRocket(.*?)"\
	# 	"Mass = (.*?)\n"\
	# 	"(.*?)"\
	# 	"MaxMass = (.*?)\n",
	
	# 	"AddEffect = ACRocket{}"\
	# 	"Mass = {}\n"\
	# 	"{}MaxInventoryMass = {}\n",
	# dotall=True)

	# all_lines = special_replace_using_matches(all_lines, regex_replace_max_mass_2,
	# 	"AddEffect = ACRocket(.*?)"\
	# 	"MaxMass = (.*?)\n"\
	# 	"(.*?)"\
	# 	"Mass = (.*?)\n",
	
	# 	"AddEffect = ACRocket{}"\
	# 	"Mass = {}\n"\
	# 	"{}MaxInventoryMass = {}\n",
	# dotall=True)

	return all_lines


def replace_without_using_matches(all_lines, pattern, replacement):
	matches = re.findall(pattern, all_lines)
	if len(matches) > 0:
		return re.sub(pattern, replacement, all_lines)
	return all_lines


def replace_using_matches(all_lines, pattern, replacement):
	matches = re.findall(pattern, all_lines)
	if len(matches) > 0:
		return re.sub(pattern, replacement, all_lines).format(*matches)
	return all_lines


def special_replace_using_matches(all_lines, fn, pattern, replacement, dotall):
	matches = re.findall(pattern, all_lines, flags=re.DOTALL if dotall else 0)
	# print(matches)
	if len(matches) > 0:
		new = fn(all_lines, pattern, replacement, matches)
		return re.sub(pattern, replacement, all_lines, flags=re.DOTALL if dotall else 0).format(*new)
	return all_lines




def regex_replace_particle(all_lines, pattern, replacement, matches):
	# matches == [(4, "foo", "bar"), (2, "baz", "bee")]
	new = [item for tup in matches for item in tup]
	# new == [4, "foo", "bar", 2, "baz", "bee"]

	# 0, 1, 2 -> 1, 2, 0
	new[0::3], new[1::3], new[2::3] = \
	new[1::3], new[2::3], new[0::3]
	
	# new == ["foo", "bar", 4, "baz", "bee", 2]
	return new


def regex_replace_sound_priority(all_lines, pattern, replacement, matches):
	# TODO: This pattern returns two items in each tuple, while we only need the first. Create a better pattern.
	# https://stackoverflow.com/a/406408/13279557
	# https://regex101.com/r/NdKaWs/2

	# matches == [(4, "foo"), (2, "bar")]
	new = [item for tup in matches for item in tup][::2]
	# new == [4, 2]
	return new


# def regex_replace_playsound(all_lines, pattern, replacement, matches):
# 	return all_lines
# 	# TODO:
# 	# AudioMan:PlaySound("ModName.rte/Folder/SoundName.wav", SceneMan:TargetDistanceScalar(self.Pos), false, true, -1)
# 	# to
#	# AudioMan:PlaySound("ModName.rte/Folder/SoundName.wav", self.Pos)	-- Cut everything and leave the thing inside the brackets after SceneMan:TargetDistanceScalar


# def regex_replace_max_mass_1(all_lines, pattern, replacement, matches):
# 	new = []

# 	for tup in matches:
# 		filler1 = tup[0]
# 		filler2 = tup[2]

# 		mass = int(tup[1])
# 		max_mass = int(tup[3])
# 		max_inventory_mass = max_mass - mass

# 		new += [filler1, mass, filler2, max_inventory_mass]

# 	return new


# def regex_replace_max_mass_2(all_lines, pattern, replacement, matches):
# 	new = []

# 	for tup in matches:
# 		filler1 = tup[0]
# 		filler2 = tup[2]

# 		mass = int(tup[3])
# 		max_mass = int(tup[1])
# 		max_inventory_mass = max_mass - mass

# 		new += [filler1, mass, filler2, max_inventory_mass]

# 	return new


# TODO: Remove this function when PlaySound is automatically replaced.
def playsound_warning(line, file_path, line_number):
	pattern = "PlaySound(.*)" # TODO: PlaySound rule should probably be [whitespacehere]PlaySound so it doesn't false-flag on something like CF_PlaySound.
	message = "No longer supported. Create a SoundContainer with CreateSoundContainer in the appropriate Create function."
	matches = re.findall(pattern, line)

	# print(file_path, pattern, line, matches)

	if len(matches) > 0 and matches[0].count(",") > 2: # If there's a match and the PlaySound call has more than 3 arguments.
		# Print a warning.
		warnings.mods_warnings.append("'{}' line {}: {} -> {}".format(file_path, line_number, pattern, message))