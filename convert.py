import os, time, pathlib, shutil, math

# 'replace_variables_list' and 'manually_edit_replace_variables_list' has uncommented cases that are empty.
# Those cases haven't been supported yet, but their descriptions can be found in 'mod-porting-guide.txt'.
# Please add those cases yourself if you know how to write Python code to support them fully.
# Don't forget to make a pull request on GitHub afterwards! :)

# When viewing this file with VS Code, you can collapse this dictionary by clicking on the arrow pointing downwards next to the variable name.
replace_variables_list = {
	# -- INI --

	# Sounds
	'= Sound': '= SoundContainer',
	'AddSample =': 'AddSound =',

	# Sound directories
	'Base.rte/Actors/Flesh3.wav': 'Base.rte/Sounds/Penetration/Flesh1.wav',
	'Base.rte/Devices/EmptyClick3.wav': 'Base.rte/Sounds/Devices/EmptyClick1.wav',
	'Base.rte/Devices/ReloadStart.wav': 'Base.rte/Sounds/Devices/ReloadStart.wav',
	'Base.rte/Devices/ReloadEnd.wav': 'Base.rte/Sounds/Devices/ReloadEnd.wav',
	'Base.rte/Actors/MetalHole1.wav': 'Base.rte/Sounds/Penetration/MetalHole1.wav',
	'Base.rte/Sounds/Explode1.wav': 'Base.rte/Sounds/Explosions/Explode1.wav',
	'Base.rte/Sounds/Explode2.wav': 'Base.rte/Sounds/Explosions/Explode2.wav',
	'Base.rte/Actors/Brains/BrainPop.wav': 'Base.rte/Actors/Brains/Case/Sounds/BrainPop.wav',
	'Base.rte/Actors/Brains/EnergyExplosion.wav': 'Base.rte/Actors/Brains/Case/Sounds/EnergyExplosion.wav',
	'Base.rte/Devices/Diggers/DiggerSound.wav': 'Base.rte/Devices/Tools/Digger/Sounds/DiggerActive.wav',
	'Base.rte/Actors/Rockets/BlastStart.wav': 'Base.rte/Sounds/Craft/BlastStart.wav',
	'Base.rte/Actors/Rockets/Blast.wav': 'Base.rte/Sounds/Craft/BlastLoop.wav',
	'Base.rte/Actors/Rockets/BlastEnd.wav': 'Base.rte/Sounds/Craft/BlastEnd.wav',
	'Base.rte/Actors/Rockets/ThrusterStart.wav': 'Base.rte/Sounds/Craft/ThrusterStart.wav',
	'Base.rte/Actors/Rockets/Thruster.wav': 'Base.rte/Sounds/Craft/ThrusterLoop.wav',
	'Base.rte/Actors/Rockets/ThrusterEnd.wav': 'Base.rte/Sounds/Craft/ThrusterEnd.wav',
	'Base.rte/Actors/Rockets/HatchOpen.wav': 'Base.rte/Sounds/Craft/HatchOpen.wav',
	'Base.rte/Actors/DropShips/JetLoop.wav': 'Base.rte/Sounds/Craft/JetLoop.wav',
	'Base.rte/Actors/DropShips/JetStart.wav': 'Base.rte/Sounds/Craft/JetStart.wav',
	'Base.rte/Actors/DropShips/JetEnd.wav': 'Base.rte/Sounds/Craft/JetEnd.wav',
	'Base.rte/Effects/Pyro/Jet.wav': 'Base.rte/Sounds/Actors/JetpackLoop.wav',
	'Base.rte/Effects/Pyro/JetStart.wav': 'Base.rte/Sounds/Actors/JetpackStart.wav',
	'Base.rte/Effects/Pyro/JetEnd.wav': 'Base.rte/Sounds/Actors/JetpackEnd.wav',
	'Base.rte/Actors/Dank.wav': 'Base.rte/Sounds/Physics/Dank.wav',
	'Base.rte/Actors/Duns.wav': 'Base.rte/Sounds/Physics/Duns.wav',
	'Base.rte/Actors/SmallThud.wav': 'Base.rte/Sounds/Physics/SmallThud.wav',
	'Base.rte/Devices/DeviceSwitch1.wav': 'Base.rte/Sounds/Devices/DeviceSwitch1.wav',
	'Base.rte/Devices/DeviceSwitch2.wav': 'Base.rte/Sounds/Devices/DeviceSwitch2.wav',
	'Base.rte/Devices/DeviceSwitch3.wav': 'Base.rte/Sounds/Devices/DeviceSwitch3.wav',
	'Base.rte/Effects/GlassImpactA.wav': 'Base.rte/Sounds/Penetration/GlassImpact1.wav',
	'Base.rte/Effects/GlassImpactB.wav': 'Base.rte/Sounds/Penetration/GlassImpact2.wav',
	'Base.rte/Effects/GlassImpactC.wav': 'Base.rte/Sounds/Penetration/GlassImpact3.wav',
	'Base.rte/Scenes/Objects/Bunkers/BunkerSystems/Teleport.wav': 'Base.rte/Scenes/Objects/Bunkers/BunkerSystems/Teleporters/Sounds/Teleport.wav',
	'Base.rte/Devices/Shotguns/BangRegular.wav': 'Base.rte/Devices/Weapons/Shotgun/Sounds/ShotgunFire.wav',
	'Base.rte/Devices/Cannons/BlamWhoshClick.wav': 'Base.rte/Sounds/Devices/BlamWhoshClick.wav',
	'Base.rte/Actors/SquishSplat.wav': 'Base.rte/Sounds/Physics/SquishSplat.wav',
	'Base.rte/Actors/Slish.wav': 'Base.rte/Sounds/Penetration/Slish.wav',
	'Base.rte/Actors/Squish.wav': 'Base.rte/Sounds/Penetration/Squish.wav',
	'Base.rte/Devices/Pistols/PistolBang.wav': 'Base.rte/Devices/Weapons/Pistol/Sounds/PistolFire.wav',
	'Base.rte/Devices/Shotguns/Blam.wav': 'Base.rte/Devices/Weapons/Shotgun/Sounds/ShotgunFireAlt.wav',
	'Base.rte/Devices/SMGs/Mp5 Single.wav': 'Base.rte/Devices/Weapons/SMG/Sounds/SMGFire005.wav',
	'Base.rte/Devices/Rifles/AK-47000.wav': 'Ronin.rte/Devices/Weapons/AK47/Sounds/Fire1.wav',
	'Base.rte/Devices/Rifles/AK-47001.wav': 'Ronin.rte/Devices/Weapons/AK47/Sounds/Fire2.wav',
	'Base.rte/Devices/Rifles/AK-47002.wav': 'Ronin.rte/Devices/Weapons/AK47/Sounds/Fire3.wav',
	'Base.rte/Devices/Rifles/AK-47003.wav': 'Ronin.rte/Devices/Weapons/AK47/Sounds/Fire4.wav',
	'Base.rte/Devices/Rifles/AK-47004.wav': 'Ronin.rte/Devices/Weapons/AK47/Sounds/Fire4.wav',
	'Base.rte/Devices/Rifles/AK-47005.wav': 'Ronin.rte/Devices/Weapons/AK47/Sounds/Fire4.wav',
	'Ronin.rte/Effects/Sounds/M16Fire.wav': 'Ronin.rte/Devices/Weapons/M16A2/Sounds/Fire1.wav',
	'Ronin.rte/Effects/Sounds/PumpgunFire.wav': 'Ronin.rte/Devices/Weapons/Model590/Sounds/Fire1.wav',
	'Base.rte/Devices/ShotgunShellIn.wav': 'Base.rte/Devices/Weapons/Shotgun/Sounds/ShotgunShellIn.wav',
	'Ronin.rte/Effects/Sounds/SniperFire.wav': 'Ronin.rte/Devices/Weapons/K98K/Sounds/Fire1.wav',
	'Ronin.rte/Effects/Sounds/RPGThrusterStart.wav': 'Ronin.rte/Devices/Weapons/RPG7/Sounds/RocketStart.wav',
	'Ronin.rte/Effects/Sounds/BazookaFire2.wav': 'Ronin.rte/Devices/Weapons/RPG7/Sounds/Fire1.wav',
	'Base.rte/Sounds/Taka.wav': 'Coalition.rte/Devices/Weapons/GatlingGun/Sounds/Fire1.wav',
	# '': '',

	# Image files, might be some missing
	'Base.rte/Actors/Rockets/RocketTinyNozzle.bmp': 'Base.rte/Craft/Shared/ThrusterNozzleA.bmp',
	'Ronin.rte/Devices/Sprites/Stone.bmp': 'Ronin.rte/Devices/Misc/Stone/Stone.bmp',
	'Base.rte/Actors/Brains/BrainCaseA.bmp': 'Base.rte/Actors/Brains/Case/BrainCaseA.bmp',
	'Base.rte/Effects/Pyro/JetFlameA.bmp': 'Base.rte/Effects/Pyro/Flashes/JetFlameA.bmp',
	'Base.rte/Effects/Pyro/TinySmoke01.bmp': 'Base.rte/Effects/Pyro/SmokeBallTinyA.bmp',
	'Base.rte/Effects/Pyro/Flame/Flame00.bmp': 'Base.rte/Effects/Pyro/Flame/Flame.bmp',
	'Base.rte/Effects/Pyro/Flame/FireBall01.bmp': 'Base.rte/Effects/Pyro/FireBallA.bmp',
	'Base.rte/Effects/Pyro/Flame/FireBall02.bmp': 'Base.rte/Effects/Pyro/FireBallB.bmp',
	'Base.rte/Effects/Pyro/Flame/FireBall03.bmp': 'Base.rte/Effects/Pyro/FireBallC.bmp',
	'Base.rte/Effects/Pyro/Flame/FireBall04.bmp': 'Base.rte/Effects/Pyro/FireBallD.bmp',
	'Base.rte/Effects/Pyro/Flame/FireBlast01.bmp': 'Base.rte/Effects/Pyro/FireBlastA.bmp',
	'Base.rte/Effects/Pyro/Flame/FireBlast02.bmp': 'Base.rte/Effects/Pyro/FireBlastB.bmp',
	'Base.rte/Effects/Pyro/Flame/FirePuff0.bmp': 'Base.rte/Effects/Pyro/FirePuff.bmp',
	'Base.rte/Effects/Pyro/Flame/SmallBlast01.bmp': 'Base.rte/Effects/Pyro/FireBlastSmallA.bmp',
	'Base.rte/Effects/Pyro/Flame/SmallSmoke01.bmp': 'Base.rte/Effects/Pyro/SmokeBallSmallA.bmp',
	'Base.rte/Effects/Pyro/Flame/TinySmoke01.bmp': 'Base.rte/Effects/Pyro/SmokeBallTinyA.bmp',
	'Missions.rte/Scenes/Items/RotatingPad.bmp': 'Missions.rte/Objects/RotatingPad/RotatingPad.bmp',
	'Missions.rte/Scenes/Items/ControlChipCase.bmp': 'Missions.rte/Objects/ControlChip/ControlChipCase.bmp',
	'Missions.rte/Scenes/Items/RotatingPadGibA.bmp': 'Missions.rte/Objects/RotatingPad/RotatingPadGibA.bmp',
	'Missions.rte/Scenes/Items/ControlChipCaseGibA.bmp': 'Missions.rte/Objects/ControlChip/Gibs/ControlChipCaseGibA.bmp',
	'Missions.rte/Scenes/Items/ControlChipCaseGibB.bmp': 'Missions.rte/Objects/ControlChip/Gibs/ControlChipCaseGibB.bmp',
	'Missions.rte/Scenes/Items/ControlChipCaseGibC.bmp': 'Missions.rte/Objects/ControlChip/Gibs/ControlChipCaseGibC.bmp',
	'Base.rte/Effects/Pyro/MuzzleFlash03.bmp': 'Base.rte/Effects/Pyro/Flashes/MuzzleFlash03.bmp',
	'Base.rte/Actors/Clones/Jetpack.bmp': 'Base.rte/Actors/Shared/Jetpack.bmp',
	'Base.rte/Devices/Pistols/MagPistol.bmp': 'Base.rte/Devices/Weapons/Pistol/PistolMagazine.bmp',
	# '': '',

	# Weapon groups
	'AddToGroup = Secondary Weapons': 'AddToGroup = Weapons - Secondary',
	'AddToGroup = Primary Weapons': 'AddToGroup = Weapons - Primary',
	'AddToGroup = Light Weapons': 'AddToGroup = Weapons - Light',
	'AddToGroup = Heavy Weapons': 'AddToGroup = Weapons - Heavy',
	'AddToGroup = Sniper Weapons': 'AddToGroup = Weapons - Sniper',
	'AddToGroup = Explosive Weapons': 'AddToGroup = Weapons - Explosive',
	'AddToGroup = Melee Weapons': 'AddToGroup = Weapons - Melee',
	'AddToGroup = Grenades': 'AddToGroup = Bombs - Grenades',
	'AddToGroup = Diggers': 'AddToGroup = Tools - Diggers',

	# Actors
	'AddToGroup = Light Infantry': 'AddToGroup = Actors - Light',
	'AddToGroup = Heavy Infantry': 'AddToGroup = Actors - Heavy',
	'AddToGroup = Snipers': 'AddToGroup = Actors - Sniper',
	'AddToGroup = Turret': 'AddToGroup = Actors - Turret',
	'AddToGroup = Mecha': 'AddToGroup = Actors - Mecha',

	# Effects
	'Fire Puff Small B': 'Fire Puff Small',
	'Particle Napalm Bomb 1': 'Particle Napalm Bomb',
	'Particle Napalm Bomb 2': 'Particle Napalm Bomb',
	'Particle Napalm Bomb 3': 'Particle Napalm Bomb',

	# Gibs
	'Ronin Gib A': 'Gib Ronin Weapon C',
	'Ronin Gib B': 'Gib Ronin Weapon A',
	'Ronin Gib C': 'Gib Ronin Weapon A',
	'Ronin Gib D': 'Gib Ronin Weapon H',
	'Ronin Gib E': 'Gib Ronin Weapon H',
	'Ronin Gib F': 'Gib Ronin Weapon B',
	'Ronin Gib G': 'Gib Ronin Weapon C',
	'Ronin Gib H': 'Gib Ronin Weapon D',
	'Ronin Gib I': 'Gib Ronin Weapon E',
	'Ronin Gib J': 'Gib Ronin Weapon F',
	'Ronin Gib K': 'Gib Ronin Weapon G',
	'Ronin Gib L': 'Gib Ronin Weapon H',
	'Ronin Gib M': 'Gib Ronin Weapon H',
	'Ronin Gib N': 'Gib Ronin Weapon B',
	'Ronin Gib O': 'Gib Ronin Weapon B',
	'Ronin Gib P': 'Gib Ronin Weapon B',

	'Coalition Weapons Gib A': 'Gib Weapon A',
	'Coalition Weapons Gib B': 'Gib Weapon B',
	'Coalition Weapons Gib C': 'Gib Weapon C',
	'Coalition Weapons Gib D': 'Gib Weapon D',
	'Coalition Weapons Gib E': 'Gib Weapon E',
	'Coalition Weapons Gib F': 'Uber Cannon Gib A',
	'Coalition Weapons Gib G': 'Gatling Gun Gib A',
	'Coalition Weapons Gib H': 'Assault Rifle Gib A',
	'Coalition Weapons Gib I': 'Gib Weapon F',
	'Coalition Weapons Gib J': 'Gib Weapon G',
	'Coalition Weapons Gib K': 'Gib Weapon H',
	'Coalition Weapons Gib L': 'Gib Weapon I',
	'Coalition Weapons Gib M': 'Missile Launcher Gib A',
	'Coalition Weapons Gib N': 'Missile Launcher Gib B',

	'Dummy Arm FG A': 'Dummy Light Arm FG',
	'Dummy Foot BG A': 'Dummy Light Foot BG',
	'Dummy Foot FG A': 'Dummy Light Foot FG',
	'Dummy Arm BG A': 'Dummy Light Arm BG',
	'Dummy Arm FG A': 'Dummy Light Arm FG',
	'Dummy Head A': 'Dummy Light Head',
	'Dummy Head Gib A': 'Dummy Light Head Gib A',
	'Dummy Head Gib B': 'Dummy Light Head Gib B',
	'Dummy Leg BG A': 'Dummy Light Leg BG',
	'Dummy Leg FG A': 'Dummy Light Leg FG',
	'Dummy Rib Cage Gib A': 'Dummy Light Rib Cage Gib A',
	'Dummy Rib Cage Gib B': 'Dummy Light Rib Cage Gib B',

	# Gib paths
	'Dummy.rte/Actors/Dummy/RibCageGibA.bmp': 'Dummy.rte/Actors/Infantry/DummyLight/Gibs/RibCageGibA.bmp',

	'Browncoats.rte/Actors/Soldier/MiscGibE.bmp': 'Browncoats.rte/Actors/Shared/Gibs/SoldierMiscGibE.bmp',
	'Browncoats.rte/Actors/Soldier/MiscGibF.bmp': 'Browncoats.rte/Actors/Shared/Gibs/SoldierMiscGibF.bmp',
	'Browncoats.rte/Actors/Soldier/MiscGibG.bmp': 'Browncoats.rte/Actors/Shared/Gibs/SoldierMiscGibG.bmp',

	# AI
	'Base.rte/Actors/AI/CrabAI.lua': 'Base.rte/AI/CrabAI.lua',
	'Base.rte/Actors/AI/HumanAI.lua': 'Base.rte/AI/HumanAI.lua',
	'Base.rte/Actors/AI/RocketAI.lua': 'Base.rte/AI/RocketAI.lua',
	'Base.rte/Actors/AI/DropShipAI.lua': 'Base.rte/AI/DropShipAI.lua',
	'Base.rte/Actors/AI/TurretAI.lua': 'Base.rte/AI/TurretAI.lua',

	# Atomgroups
	'CopyOf = Atom Group Null': 'CopyOf = Null AtomGroup',

	# Atomgroups common with Actors
	'CopyOf = HandGroup': 'CopyOf = Human Hand',
	'CopyOf = Foot': 'CopyOf = Human Foot',
	'CopyOf = CrabFootGroup': 'CopyOf = Crab Foot',
	'CopyOf = Rocket Landing Gear Foot Right': 'CopyOf = Rocket Landing Gear Foot',
	'CopyOf = Rocket Landing Gear Foot Left': 'CopyOf = Rocket Landing Gear Foot',

	# Scenes/Background layers
	'Near Layer': 'Default Front',
	'Sky Layer': 'Default Sky Layer',
	'Clouds Layer': 'Clouds Layer A',

	# Bunker parts
	'Concrete barrier': 'Concrete Barrier',
	'TutShaftEntry L Dark': 'TutShaft Entry L Dark',
	'TutShaftEntry L Light': 'TutShaft Entry L Light',

	# Miscellaneous
	'Round AK-47': 'Round Ronin AK-47',
	'Tracer AK-47': 'Tracer Ronin AK-47',
	'Shell Smoking': 'Smoking Large Casing',
	# '': '',
	'Small MG Turret': 'Small Turret',
	# '': '',
	# '': '',
	# '': '',
	# '': '',
	# '': '',
	'Dummy Head Gib A': 'Dummy Light Head Gib A',
	'Dummy Head Gib B': 'Dummy Light Head Gib B',

	# Ronin weapons
	'CopyOf = Glock': 'CopyOf = Luger P08',
	'CopyOf = Pumpgun': 'CopyOf = Model 590',
	'CopyOf = Spas 12': 'CopyOf = SPAS 12',
	'CopyOf = Kar98': 'CopyOf = Kar98k',
	'CopyOf = M16': 'CopyOf = M16A2',
	'CopyOf = Thumper': 'CopyOf = M79',
	'CopyOf = Uzi': 'CopyOf = UZI',

	# -- LUA --

	# Miscellaneous
	'WithinBox': 'IsWithinBox',

	# Weapon groups
	'"Secondary Weapons"': '"Weapons - Secondary"',
	'"Primary Weapons"': '"Weapons - Primary"',
	'"Light Weapons"': '"Weapons - Light"',
	'"Heavy Weapons"': '"Weapons - Heavy"',
	'"Sniper Weapons"': '"Weapons - Sniper"',
	'"Explosive Weapons"': '"Weapons - Explosive"',
	'"Melee Weapons"': '"Weapons - Melee"',
	'"Grenades"': '"Bombs - Grenades"',
	'"Diggers"': '"Tools - Diggers"',
	
	# Actors
	'"Light Infantry"': '"Actors - Light"',
	'"Heavy Infantry"': '"Actors - Heavy"',
	'"Snipers"': '"Actors - Sniper"',
	'"Turret"': '"Actors - Turret"',
	'"Mecha"': '"Actors - Mecha"',

	# FrameMan
	'FrameMan:Draw': 'PrimitiveMan:Draw',
	'FrameMan.ResX': 'FrameMan.PlayerScreenWidth',
	'FrameMan.ResY': 'FrameMan.PlayerScreenHeight',

	# AudioMan
	# Regex is probably needed to support this case
	# '': '',
	
	# SoundContainer
	'IsPlaying(': 'IsBeingPlayed(',
	# '': '',

	# Copy this line and uncomment it, if you need to add extra cases
	# '': '',
}

# When viewing this file with VS Code, you can collapse this dictionary by clicking on the arrow pointing downwards next to the variable name.
manually_edit_replace_variables_list = {
	# -- INI --

	# Priority for sounds will work differently in the future, so it's best to disable them for now.
	'Priority =': '// Priority =',

	# -- LUA --

	# Copy this line and uncomment it, if you need to add extra cases
	# '': '',
}

replace_file_extensions = {
	'.ini',
	'.lua'
}

file_manual_path = "output/manually-edit-these-lines.txt"

time_start = time.time()

if os.path.exists(file_manual_path):
	os.remove(file_manual_path)

with open(file_manual_path, "w") as file_manual:
	for input_folder_path, input_subfolders, full_filenames in os.walk("input"):
		
		input_folder_path_tuple = pathlib.Path(input_folder_path).parts
		if len(input_folder_path_tuple) == 2:
			print("Converting '{}'...".format(input_folder_path_tuple[1]))
			file_manual.write("\n")

		output_folder = os.path.join("output", pathlib.Path(*pathlib.Path(input_folder_path).parts[1:]))
		if input_folder_path != "input":
			os.makedirs(output_folder)

		for full_filename in full_filenames:
			filename, file_extension = os.path.splitext(full_filename)

			if filename == ".empty":
				continue

			input_file_path  = os.path.join(input_folder_path , full_filename)
			output_file_path = os.path.join(output_folder, full_filename)

			if file_extension in replace_file_extensions:
				with open(input_file_path, "r") as file_in:
					line_number = 0
					lines = []
					for line in file_in.readlines():
						line_number += 1

						# Replace variables
						for old_str, new_str in replace_variables_list.items():
							line = line.replace(old_str, new_str)
						
						# Replace variables that may need to be manually edited afterwards
						for old_str, new_str in manually_edit_replace_variables_list.items():
							if line.find(old_str) != -1:
								line = line.replace(old_str, new_str)
								file_manual.write("path: {} | line: {} | edit this: {}\n".format(output_file_path, line_number, new_str))
						lines.append(line)
					with open(output_file_path, "w") as file_out:
						file_out.write("".join(lines))
			else:
				shutil.copyfile(input_file_path, output_file_path)

# Remove legacy mods from the input folder once they've been processed
# for filename in os.listdir("input"):
# 	if filename != ".empty":
# 		filepath = os.path.join("input", filename)
# 		shutil.rmtree(filepath)

elapsed = math.floor(time.time() - time_start)
print("Conversion finished in {} second{}!".format(elapsed, "" if elapsed == 1 else "s"))