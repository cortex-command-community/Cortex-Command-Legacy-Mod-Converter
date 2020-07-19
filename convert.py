replace_variables = {
	"= Sound"    : "= SoundContainer", # ReloadEndSound *= Sound* -> ReloadEndSound *= SoundContainer*
	"= AddSample": "= AddSound",
}

replace_folders = {

}

# print(replace_variables)
# print(replace_folders)

with open("input\mario-b33-manual-conversion.rte\Mario.rte\Items\Feather\Feather.ini", "r") as fileIn:
	for line in fileIn:
		print(line, end="")