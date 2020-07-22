-- <Gruppe 8> <https://steamcommunity.com/sharedfiles/filedetails/?id=1722986298> by <루스키>
-- Faction file by <Weegee>
-- 
-- Unique Faction ID
local factionid = "Gruppe 8";
print ("Loading "..factionid)

CF_Factions[#CF_Factions + 1] = factionid

CF_FactionNames[factionid] = "Gruppe 8";
CF_FactionDescriptions[factionid] = "Gruppe 8. Simply referred as 'Gruppe', is a transgalactic private millitary corporation founded by military enterprises from old Earth.  Gruppe 8 is more likely to mechanized elite forces.";
CF_FactionPlayable[factionid] = true;

CF_RequiredModules[factionid] = {"csrt.rte"}
-- Available values ORGANIC, SYNTHETIC
CF_FactionNatures[factionid] = CF_FactionTypes.ORGANIC;


-- Define faction bonuses, in percents
-- Scan price reduction
CF_ScanBonuses[factionid] = 0
-- Relation points increase
CF_RelationsBonuses[factionid] = 0
-- Hew HQ build price reduction
CF_ExpansionBonuses[factionid] = 0

-- Gold per turn increase
CF_MineBonuses[factionid] = 0
-- Science per turn increase
CF_LabBonuses[factionid] = 0
-- Delivery time reduction
CF_AirfieldBonuses[factionid] = 30
-- Superweapon targeting reduction
CF_SuperWeaponBonuses[factionid] = 0
-- Unit price reduction
CF_FactoryBonuses[factionid] = 0
-- Body price reduction
CF_CloneBonuses[factionid] = 0
-- HP regeneration increase
CF_HospitalBonuses[factionid] = 0


-- Define brain unit
CF_Brains[factionid] = "Brain Robot";
CF_BrainModules[factionid] = "Base.rte";
CF_BrainClasses[factionid] = "AHuman";
CF_BrainPrices[factionid] = 500;

-- Define dropship
CF_Crafts[factionid] = "Drop Ship MK1";
CF_CraftModules[factionid] = "Base.rte";
CF_CraftClasses[factionid] = "ACDropShip";
CF_CraftPrices[factionid] = 120;

-- Define superweapon script
CF_SuperWeaponScripts[factionid] = "UnmappedLands2.rte/SuperWeapons/Bombing.lua"

-- Define buyable actors available for purchase or unlocks
CF_ActNames[factionid] = {}
CF_ActPresets[factionid] = {}
CF_ActModules[factionid] = {}
CF_ActPrices[factionid] = {}
CF_ActDescriptions[factionid] = {}
CF_ActUnlockData[factionid] = {}
CF_ActClasses[factionid] = {}
CF_ActTypes[factionid] = {}
CF_ActPowers[factionid] = {}
CF_ActOffsets[factionid] = {}

local i = 0
i = #CF_ActNames[factionid] + 1
CF_ActNames[factionid][i] = "Gruppe Scout"
CF_ActPresets[factionid][i] = "Gruppe Scout"
CF_ActModules[factionid][i] = "csrt.rte"
CF_ActPrices[factionid][i] = 145
CF_ActDescriptions[factionid][i] = "Light Gruppe 8 soldier without armor.  Lighter and more agile compared to the armored troop, ideal unit for reconnaissance missions."
CF_ActUnlockData[factionid][i] = 350
CF_ActTypes[factionid][i] = CF_ActorTypes.LIGHT;
CF_ActPowers[factionid][i] = 3

i = #CF_ActNames[factionid] + 1
CF_ActNames[factionid][i] = "Gruppe Troop"
CF_ActPresets[factionid][i] = "Gruppe Troop"
CF_ActModules[factionid][i] = "csrt.rte"
CF_ActPrices[factionid][i] = 170
CF_ActDescriptions[factionid][i] = "Standard Gruppe 8 soldier equipped with armor and a jetpack.  A bit heavier and a bit less agile than the normal troop, but more than makes up for it with its strength."
CF_ActUnlockData[factionid][i] = 0
CF_ActTypes[factionid][i] = CF_ActorTypes.HEAVY;
CF_ActPowers[factionid][i] = 6





-- Define buyable items available for purchase or unlocks
CF_ItmNames[factionid] = {}
CF_ItmPresets[factionid] = {}
CF_ItmModules[factionid] = {}
CF_ItmPrices[factionid] = {}
CF_ItmDescriptions[factionid] = {}
CF_ItmUnlockData[factionid] = {}
CF_ItmClasses[factionid] = {}
CF_ItmTypes[factionid] = {}
CF_ItmPowers[factionid] = {} -- AI will select weapons based on this value 1 - weakest, 10 toughest, 0 never use

-- Available weapon types
-- PISTOL, RIFLE, SHOTGUN, SNIPER, HEAVY, SHIELD, DIGGER, GRENADE

local i = 0
i = #CF_ItmNames[factionid] + 1
CF_ItmNames[factionid][i] = "Light Digger"
CF_ItmPresets[factionid][i] = "Light Digger"
CF_ItmModules[factionid][i] = "Base.rte"
CF_ItmPrices[factionid][i] = 10
CF_ItmDescriptions[factionid][i] = "Lightest in the digger family. Cheapest of them all and works as a nice melee weapon on soft targets."
CF_ItmUnlockData[factionid][i] = 0 -- 0 means available at start
CF_ItmTypes[factionid][i] = CF_WeaponTypes.DIGGER;
CF_ItmPowers[factionid][i] = 1

i = #CF_ItmNames[factionid] + 1
CF_ItmNames[factionid][i] = "Medium Digger"
CF_ItmPresets[factionid][i] = "Medium Digger"
CF_ItmModules[factionid][i] = "Base.rte"
CF_ItmPrices[factionid][i] = 40
CF_ItmDescriptions[factionid][i] = "Stronger digger. This one can pierce rocks with some effort and dig impressive tunnels and its melee weapon capabilities are much greater."
CF_ItmUnlockData[factionid][i] = 500
CF_ItmTypes[factionid][i] = CF_WeaponTypes.DIGGER;
CF_ItmPowers[factionid][i] = 4

i = #CF_ItmNames[factionid] + 1
CF_ItmNames[factionid][i] = "Heavy Digger"
CF_ItmPresets[factionid][i] = "Heavy Digger"
CF_ItmModules[factionid][i] = "Base.rte"
CF_ItmPrices[factionid][i] = 100
CF_ItmDescriptions[factionid][i] = "Heaviest and the most powerful of them all. Eats concrete with great hunger and allows you to make complex mining caves incredibly fast. Shreds anyone unfortunate who stand in its way."
CF_ItmUnlockData[factionid][i] = 1000
CF_ItmTypes[factionid][i] = CF_WeaponTypes.DIGGER;
CF_ItmPowers[factionid][i] = 8

i = #CF_ItmNames[factionid] + 1
CF_ItmNames[factionid][i] = "Light Scanner"
CF_ItmPresets[factionid][i] = "Light Scanner"
CF_ItmModules[factionid][i] = "Base.rte"
CF_ItmPrices[factionid][i] = 10
CF_ItmDescriptions[factionid][i] = "Lightest in the scanner family. Cheapest of them all and can only scan a small area."
CF_ItmUnlockData[factionid][i] = 150
CF_ItmTypes[factionid][i] = CF_WeaponTypes.TOOL;
CF_ItmPowers[factionid][i] = 0

i = #CF_ItmNames[factionid] + 1
CF_ItmNames[factionid][i] = "Medium Scanner"
CF_ItmPresets[factionid][i] = "Medium Scanner"
CF_ItmModules[factionid][i] = "Base.rte"
CF_ItmPrices[factionid][i] = 40
CF_ItmDescriptions[factionid][i] = "Medium scanner. This scanner is stronger and can reveal a larger area."
CF_ItmUnlockData[factionid][i] = 250
CF_ItmTypes[factionid][i] = CF_WeaponTypes.TOOL;
CF_ItmPowers[factionid][i] = 0

i = #CF_ItmNames[factionid] + 1
CF_ItmNames[factionid][i] = "Heavy Scanner"
CF_ItmPresets[factionid][i] = "Heavy Scanner"
CF_ItmModules[factionid][i] = "Base.rte"
CF_ItmPrices[factionid][i] = 70
CF_ItmDescriptions[factionid][i] = "Strongest scanner out of the three. Can reveal a large area."
CF_ItmUnlockData[factionid][i] = 450
CF_ItmTypes[factionid][i] = CF_WeaponTypes.TOOL;
CF_ItmPowers[factionid][i] = 0

i = #CF_ItmNames[factionid] + 1
CF_ItmNames[factionid][i] = "Balistic Shield"
CF_ItmPresets[factionid][i] = "Balistic Shield"
CF_ItmModules[factionid][i] = "csrt.rte"
CF_ItmPrices[factionid][i] = 50
CF_ItmDescriptions[factionid][i] = "This metal shield for SRT provides excellent frontal protection to the user and it can stop numerous hits."
CF_ItmUnlockData[factionid][i] = 50
CF_ItmClasses[factionid][i] = "HeldDevice"
CF_ItmTypes[factionid][i] = CF_WeaponTypes.SHIELD;
CF_ItmPowers[factionid][i] = 4

i = #CF_ItmNames[factionid] + 1
CF_ItmNames[factionid][i] = "HG-85"
CF_ItmPresets[factionid][i] = "HG-85"
CF_ItmModules[factionid][i] = "csrt.rte"
CF_ItmPrices[factionid][i] = 15
CF_ItmDescriptions[factionid][i] = "Explosive fragmentation grenade from Switzerland. Heavy but powerful. Blows up after a 4 second delay."
CF_ItmUnlockData[factionid][i] = 0
CF_ItmClasses[factionid][i] = "TDExplosive"
CF_ItmTypes[factionid][i] = CF_WeaponTypes.GRENADE;
CF_ItmPowers[factionid][i] = 2

i = #CF_ItmNames[factionid] + 1
CF_ItmNames[factionid][i] = "Glock 18C"
CF_ItmPresets[factionid][i] = "Glock 18C"
CF_ItmModules[factionid][i] = "csrt.rte"
CF_ItmPrices[factionid][i] = 20
CF_ItmDescriptions[factionid][i] = "Developed to fulfill a military counter-terrorism role."
CF_ItmUnlockData[factionid][i] = 750
CF_ItmTypes[factionid][i] = CF_WeaponTypes.PISTOL;
CF_ItmPowers[factionid][i] = 2

i = #CF_ItmNames[factionid] + 1
CF_ItmNames[factionid][i] = "OTs-33"
CF_ItmPresets[factionid][i] = "OTs-33"
CF_ItmModules[factionid][i] = "csrt.rte"
CF_ItmPrices[factionid][i] = 25
CF_ItmDescriptions[factionid][i] = "Machine pistol, designed for special operations."
CF_ItmUnlockData[factionid][i] = 1000
CF_ItmTypes[factionid][i] = CF_WeaponTypes.PISTOL;
CF_ItmPowers[factionid][i] = 2

i = #CF_ItmNames[factionid] + 1
CF_ItmNames[factionid][i] = "Colt Python"
CF_ItmPresets[factionid][i] = "Colt Python"
CF_ItmModules[factionid][i] = "csrt.rte"
CF_ItmPrices[factionid][i] = 30
CF_ItmDescriptions[factionid][i] = ".45 Magnum, Double-action."
CF_ItmUnlockData[factionid][i] = 0
CF_ItmTypes[factionid][i] = CF_WeaponTypes.PISTOL;
CF_ItmPowers[factionid][i] = 3

i = #CF_ItmNames[factionid] + 1
CF_ItmNames[factionid][i] = "Micro Uzi"
CF_ItmPresets[factionid][i] = "Micro Uzi"
CF_ItmModules[factionid][i] = "csrt.rte"
CF_ItmPrices[factionid][i] = 30
CF_ItmDescriptions[factionid][i] = "Submachine Gun with a extremely high rate of fire.  The Uzi can be wielded with a shield."
CF_ItmUnlockData[factionid][i] = 700
CF_ItmTypes[factionid][i] = CF_WeaponTypes.RIFLE;
CF_ItmPowers[factionid][i] = 3

i = #CF_ItmNames[factionid] + 1
CF_ItmNames[factionid][i] = "P90"
CF_ItmPresets[factionid][i] = "P90"
CF_ItmModules[factionid][i] = "csrt.rte"
CF_ItmPrices[factionid][i] = 40
CF_ItmDescriptions[factionid][i] = "An Europian PDW with unique mechanism and huge magazine capacity."
CF_ItmUnlockData[factionid][i] = 850
CF_ItmTypes[factionid][i] = CF_WeaponTypes.RIFLE;
CF_ItmPowers[factionid][i] = 4

i = #CF_ItmNames[factionid] + 1
CF_ItmNames[factionid][i] = "AKS-74U"
CF_ItmPresets[factionid][i] = "AKS-74U"
CF_ItmModules[factionid][i] = "csrt.rte"
CF_ItmPrices[factionid][i] = 45
CF_ItmDescriptions[factionid][i] = "Carbinated AK-74. Light and compact."
CF_ItmUnlockData[factionid][i] = 50
CF_ItmTypes[factionid][i] = CF_WeaponTypes.RIFLE;
CF_ItmPowers[factionid][i] = 5

i = #CF_ItmNames[factionid] + 1
CF_ItmNames[factionid][i] = "M16A1"
CF_ItmPresets[factionid][i] = "M16A1"
CF_ItmModules[factionid][i] = "csrt.rte"
CF_ItmPrices[factionid][i] = 55
CF_ItmDescriptions[factionid][i] = "Accurate and deadly.  Good standard weapon for basic infantryman."
CF_ItmUnlockData[factionid][i] = 750
CF_ItmTypes[factionid][i] = CF_WeaponTypes.RIFLE;
CF_ItmPowers[factionid][i] = 6

i = #CF_ItmNames[factionid] + 1
CF_ItmNames[factionid][i] = "G36C"
CF_ItmPresets[factionid][i] = "G36C"
CF_ItmModules[factionid][i] = "csrt.rte"
CF_ItmPrices[factionid][i] = 60
CF_ItmDescriptions[factionid][i] = "Carbinated G36."
CF_ItmUnlockData[factionid][i] = 850
CF_ItmTypes[factionid][i] = CF_WeaponTypes.RIFLE;
CF_ItmPowers[factionid][i] = 6

i = #CF_ItmNames[factionid] + 1
CF_ItmNames[factionid][i] = "AKM"
CF_ItmPresets[factionid][i] = "AKM"
CF_ItmModules[factionid][i] = "csrt.rte"
CF_ItmPrices[factionid][i] = 65
CF_ItmDescriptions[factionid][i] = "An Russian assault rifle. Pull the trigger, Bullet out. No matter where you are."
CF_ItmUnlockData[factionid][i] = 0
CF_ItmTypes[factionid][i] = CF_WeaponTypes.RIFLE;
CF_ItmPowers[factionid][i] = 6

i = #CF_ItmNames[factionid] + 1
CF_ItmNames[factionid][i] = "OTs-14-1A-01"
CF_ItmPresets[factionid][i] = "OTs-14-1A-01"
CF_ItmModules[factionid][i] = "csrt.rte"
CF_ItmPrices[factionid][i] = 65
CF_ItmDescriptions[factionid][i] = "Russian bullpup assault rifle."
CF_ItmUnlockData[factionid][i] = 700
CF_ItmTypes[factionid][i] = CF_WeaponTypes.RIFLE;
CF_ItmPowers[factionid][i] = 6

i = #CF_ItmNames[factionid] + 1
CF_ItmNames[factionid][i] = "G36A1"
CF_ItmPresets[factionid][i] = "G36A1"
CF_ItmModules[factionid][i] = "csrt.rte"
CF_ItmPrices[factionid][i] = 70
CF_ItmDescriptions[factionid][i] = "Light and accurate.  It's ergonomic design makes it easy-to-use weapon."
CF_ItmUnlockData[factionid][i] = 950
CF_ItmTypes[factionid][i] = CF_WeaponTypes.RIFLE;
CF_ItmPowers[factionid][i] = 7

i = #CF_ItmNames[factionid] + 1
CF_ItmNames[factionid][i] = "AUG A1"
CF_ItmPresets[factionid][i] = "AUG A1"
CF_ItmModules[factionid][i] = "csrt.rte"
CF_ItmPrices[factionid][i] = 70
CF_ItmDescriptions[factionid][i] = "Reliable European bullpup rifle.  Equipped with an optic."
CF_ItmUnlockData[factionid][i] = 850
CF_ItmTypes[factionid][i] = CF_WeaponTypes.RIFLE;
CF_ItmPowers[factionid][i] = 7

i = #CF_ItmNames[factionid] + 1
CF_ItmNames[factionid][i] = "FN FAL 50.00"
CF_ItmPresets[factionid][i] = "FN FAL 50.00"
CF_ItmModules[factionid][i] = "csrt.rte"
CF_ItmPrices[factionid][i] = 75
CF_ItmDescriptions[factionid][i] = "Stand battle rifle."
CF_ItmUnlockData[factionid][i] = 750
CF_ItmTypes[factionid][i] = CF_WeaponTypes.RIFLE;
CF_ItmPowers[factionid][i] = 7

i = #CF_ItmNames[factionid] + 1
CF_ItmNames[factionid][i] = "AS Val"
CF_ItmPresets[factionid][i] = "AS Val"
CF_ItmModules[factionid][i] = "csrt.rte"
CF_ItmPrices[factionid][i] = 85
CF_ItmDescriptions[factionid][i] = "Special purpose silenced Automatic rifle."
CF_ItmUnlockData[factionid][i] = 1000
CF_ItmTypes[factionid][i] = CF_WeaponTypes.RIFLE;
CF_ItmPowers[factionid][i] = 8

i = #CF_ItmNames[factionid] + 1
CF_ItmNames[factionid][i] = "M16A4"
CF_ItmPresets[factionid][i] = "M16A4"
CF_ItmModules[factionid][i] = "csrt.rte"
CF_ItmPrices[factionid][i] = 95
CF_ItmDescriptions[factionid][i] = "Designed for special operations. Press F to use under barrel grenade launcher."
CF_ItmUnlockData[factionid][i] = 1200
CF_ItmTypes[factionid][i] = CF_WeaponTypes.RIFLE;
CF_ItmPowers[factionid][i] = 9

i = #CF_ItmNames[factionid] + 1
CF_ItmNames[factionid][i] = "KS-23"
CF_ItmPresets[factionid][i] = "KS-23"
CF_ItmModules[factionid][i] = "csrt.rte"
CF_ItmPrices[factionid][i] = 40
CF_ItmDescriptions[factionid][i] = "23mm special carbin."
CF_ItmUnlockData[factionid][i] = 100
CF_ItmTypes[factionid][i] = CF_WeaponTypes.SHOTGUN;
CF_ItmPowers[factionid][i] = 4

i = #CF_ItmNames[factionid] + 1
CF_ItmNames[factionid][i] = "SPAS-12"
CF_ItmPresets[factionid][i] = "SPAS-12"
CF_ItmModules[factionid][i] = "csrt.rte"
CF_ItmPrices[factionid][i] = 90
CF_ItmDescriptions[factionid][i] = "SPAS-12, the shotgun of tommorow.  It has amazing firepower and high ammo capacity."
CF_ItmUnlockData[factionid][i] = 850
CF_ItmTypes[factionid][i] = CF_WeaponTypes.SHOTGUN;
CF_ItmPowers[factionid][i] = 7

i = #CF_ItmNames[factionid] + 1
CF_ItmNames[factionid][i] = "USAS-12"
CF_ItmPresets[factionid][i] = "USAS-12"
CF_ItmModules[factionid][i] = "csrt.rte"
CF_ItmPrices[factionid][i] = 95
CF_ItmDescriptions[factionid][i] = "Combat shotgun.  Provide sustained firepower in close-combat senarios."
CF_ItmUnlockData[factionid][i] = 1000
CF_ItmTypes[factionid][i] = CF_WeaponTypes.SHOTGUN;
CF_ItmPowers[factionid][i] = 8

i = #CF_ItmNames[factionid] + 1
CF_ItmNames[factionid][i] = "Dragunov"
CF_ItmPresets[factionid][i] = "Dragunov"
CF_ItmModules[factionid][i] = "csrt.rte"
CF_ItmPrices[factionid][i] = 130
CF_ItmDescriptions[factionid][i] = "Russian DMR designed for close fire support. It seems that the rumor on the gun's accuracy is not true."
CF_ItmUnlockData[factionid][i] = 850
CF_ItmTypes[factionid][i] = CF_WeaponTypes.SNIPER;
CF_ItmPowers[factionid][i] = 8

i = #CF_ItmNames[factionid] + 1
CF_ItmNames[factionid][i] = "M70"
CF_ItmPresets[factionid][i] = "M70"
CF_ItmModules[factionid][i] = "csrt.rte"
CF_ItmPrices[factionid][i] = 150
CF_ItmDescriptions[factionid][i] = "Powerful sniper rifle.  Long range and precision combined make this a deadly weapon."
CF_ItmUnlockData[factionid][i] = 50
CF_ItmTypes[factionid][i] = CF_WeaponTypes.SNIPER;
CF_ItmPowers[factionid][i] = 5

i = #CF_ItmNames[factionid] + 1
CF_ItmNames[factionid][i] = "WA2000"
CF_ItmPresets[factionid][i] = "WA2000"
CF_ItmModules[factionid][i] = "csrt.rte"
CF_ItmPrices[factionid][i] = 250
CF_ItmDescriptions[factionid][i] = "Extremely accurate, extremely expensive."
CF_ItmUnlockData[factionid][i] = 1100
CF_ItmTypes[factionid][i] = CF_WeaponTypes.SNIPER;
CF_ItmPowers[factionid][i] = 9

i = #CF_ItmNames[factionid] + 1
CF_ItmNames[factionid][i] = "RPD"
CF_ItmPresets[factionid][i] = "RPD"
CF_ItmModules[factionid][i] = "csrt.rte"
CF_ItmPrices[factionid][i] = 85
CF_ItmDescriptions[factionid][i] = "One of the early Squad Automatic Weapons.  Provide sustain fire power for fierce battle."
CF_ItmUnlockData[factionid][i] = 750
CF_ItmTypes[factionid][i] = CF_WeaponTypes.HEAVY;
CF_ItmPowers[factionid][i] = 5

i = #CF_ItmNames[factionid] + 1
CF_ItmNames[factionid][i] = "M249"
CF_ItmPresets[factionid][i] = "M249"
CF_ItmModules[factionid][i] = "csrt.rte"
CF_ItmPrices[factionid][i] = 150
CF_ItmDescriptions[factionid][i] = "Standard light machine gun.  It's portability combined with moderate rate of fire and large ammo capacity makes it a deadly support weapon."
CF_ItmUnlockData[factionid][i] = 950
CF_ItmTypes[factionid][i] = CF_WeaponTypes.HEAVY;
CF_ItmPowers[factionid][i] = 7

i = #CF_ItmNames[factionid] + 1
CF_ItmNames[factionid][i] = "M72 LAW"
CF_ItmPresets[factionid][i] = "M72 LAW"
CF_ItmModules[factionid][i] = "csrt.rte"
CF_ItmPrices[factionid][i] = 30
CF_ItmDescriptions[factionid][i] = "Standard shoulder-fired anti-armor weapon for basic infantryman.  The launch tube was not designed to be reusable."
CF_ItmUnlockData[factionid][i] = 770
CF_ItmTypes[factionid][i] = CF_WeaponTypes.GRENADE;
CF_ItmPowers[factionid][i] = 5

i = #CF_ItmNames[factionid] + 1
CF_ItmNames[factionid][i] = "RPG-7"
CF_ItmPresets[factionid][i] = "RPG-7"
CF_ItmModules[factionid][i] = "csrt.rte"
CF_ItmPrices[factionid][i] = 150
CF_ItmDescriptions[factionid][i] = "Allah's magic wand, modified for anti-helicopter use.  Fires accelerating rockets that cause massive damage with a direct hit."
CF_ItmUnlockData[factionid][i] = 900
CF_ItmTypes[factionid][i] = CF_WeaponTypes.HEAVY;
CF_ItmPowers[factionid][i] = 7

i = #CF_ItmNames[factionid] + 1
CF_ItmNames[factionid][i] = "Milkor MGL"
CF_ItmPresets[factionid][i] = "Milkor MGL"
CF_ItmModules[factionid][i] = "csrt.rte"
CF_ItmPrices[factionid][i] = 300
CF_ItmDescriptions[factionid][i] = "Multiple grenade launcher. Deals massive damage rapidly."
CF_ItmUnlockData[factionid][i] = 950
CF_ItmTypes[factionid][i] = CF_WeaponTypes.HEAVY;
CF_ItmPowers[factionid][i] = 8

i = #CF_ItmNames[factionid] + 1
CF_ItmNames[factionid][i] = "M202 FLASH"
CF_ItmPresets[factionid][i] = "M202 FLASH"
CF_ItmModules[factionid][i] = "csrt.rte"
CF_ItmPrices[factionid][i] = 550
CF_ItmDescriptions[factionid][i] = "Quad-barrel shoulder-fired thermobaric rocket launcher.  Fires inciderate rocket that explode on impact."
CF_ItmUnlockData[factionid][i] = 1200
CF_ItmTypes[factionid][i] = CF_WeaponTypes.HEAVY;
CF_ItmPowers[factionid][i] = 10

