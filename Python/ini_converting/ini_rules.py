from Python.ini_converting import ini_rules_utils

from Python import thumbnail_generator
from Python import update_progress
from Python.ini_converting import ini_fix_duplicate_scripts, ini_cst, ini_tokenizer
from Python import shared_globals as cfg


"""
{
	"foo.rte": {
		"Foo.ini": ini_cst,
		"FolderName": {
			"Bar.ini": ini_cst,
		}
	}
}
"""


def apply_rules_on_ini_cst(ini_cst, output_folder_path):

    apply_rules_on_ini_cst_recursively(ini_cst, output_folder_path)
    ini_fix_duplicate_scripts.run(ini_cst)


def apply_rules_on_ini_cst_recursively(parsed_subset, output_folder_path):
    items = parsed_subset.items()
    for key, value in items:
        if isinstance(value, dict):
            apply_rules_on_ini_cst_recursively(value, output_folder_path)
        else:  # If it's a list of the sections of a file.
            if cfg.progress_bar:
                cfg.progress_bar.inc()
                cfg.progress_bar.setSubtext(f"applying rules on {key}")
            apply_rules_on_sections(value, output_folder_path)


def apply_rules_on_sections(parsed_subset, output_folder_path):
    for section in parsed_subset:
        for token in section:
            if token["type"] == "children":
                children = token["content"]

                if ini_rules_utils.children_contain_property_shallowly(
                    children, "MaxMass"
                ):
                    max_mass_to_max_inventory_mass(children)

                for line_tokens in children:
                    replace_property_and_value(
                        line_tokens,
                        "MinThrottleRange",
                        "NegativeThrottleMultiplier",
                        min_throttle_range_to_negative_throttle_multiplier,
                    )
                    replace_property_and_value(
                        line_tokens,
                        "MaxThrottleRange",
                        "PositiveThrottleMultiplier",
                        max_throttle_range_to_positive_throttle_multiplier,
                    )

                shovel_flash_fix(children)

        if ini_rules_utils.line_contains_property_and_value(section, "AddActor", "Leg"):
            for token in section:
                if token["type"] == "children":
                    children = token["content"]

                    max_length_to_offsets(children)

        add_grip_strength_if_missing(section)

        pie_menu_fix(section)

        remove_slterrain_properties(section)

        if output_folder_path != None:
            iconfile_path_to_thumbnail_generator(section, output_folder_path)


def max_mass_to_max_inventory_mass(children):
    """MaxInventoryMass = MaxMass - Mass"""

    mass = 0  # The Mass is optionally defined in the INI file.

    # TODO: Find a way to split these into subfunctions.
    for line_tokens in children:
        for token in line_tokens:
            if token["type"] == "property":
                if token["content"] == "Mass":
                    for token_2 in line_tokens:
                        if token_2["type"] == "value":
                            mass = float(token_2["content"])
                            break

                if token["content"] == "MaxMass":
                    for token_2 in line_tokens:
                        if token_2["type"] == "value":
                            max_mass = float(token_2["content"])
                            break

    max_inventory_mass = remove_excess_zeros(max_mass - mass)

    for line_tokens in children:
        for token in line_tokens:
            if token["type"] == "property":
                if token["content"] == "MaxMass":
                    token["content"] = "MaxInventoryMass"

                    for token_2 in line_tokens:
                        if token_2["type"] == "value":
                            token_2["content"] = max_inventory_mass
                            return


def remove_excess_zeros(string):
    return f"{string:g}"


def replace_property_and_value(
    line_tokens, old_property, new_property, new_value_function
):
    for token in line_tokens:
        if token["type"] == "property":
            if token["content"] == old_property:
                token["content"] = new_property
                for token_2 in line_tokens:
                    if token_2["type"] == "value":
                        token_2["content"] = new_value_function(token_2["content"])
                        return


def min_throttle_range_to_negative_throttle_multiplier(old_value):
    new_value = abs(1 - abs(float(old_value)))
    return remove_excess_zeros(new_value)


def max_throttle_range_to_positive_throttle_multiplier(old_value):
    new_value = abs(1 + abs(float(old_value)))
    return remove_excess_zeros(new_value)


# TODO: Refactor max_length_to_offsets and max_length_to_offsets_2
def max_length_to_offsets(children):
    """
    If the parent line is AddActor = Leg:
    MaxLength = old_value
    ->
    ContractedOffset = Vector
            X = old_value / 2
            Y = 0
    ExtendedOffset = Vector
            X = old_value
            Y = 0
    """

    for index, line_tokens in enumerate(children):
        old_value = max_length_to_offsets_2(line_tokens)

        if old_value != None:
            # print(index, old_value)

            # TODO: Can this be done with .append() instead of .insert() ?
            children.insert(
                index + 1,
                [
                    {"type": "extra", "content": "\t"},
                    {"type": "property", "content": "ExtendedOffset"},
                    {"type": "extra", "content": " "},
                    {"type": "extra", "content": "="},
                    {"type": "extra", "content": " "},
                    {"type": "value", "content": "Vector"},
                    {"type": "extra", "content": "\n"},
                    {
                        "type": "children",
                        "content": [
                            [
                                {"type": "extra", "content": "\t\t"},
                                {"type": "property", "content": "X"},
                                {"type": "extra", "content": " "},
                                {"type": "extra", "content": "="},
                                {"type": "extra", "content": " "},
                                {
                                    "type": "value",
                                    "content": remove_excess_zeros(old_value),
                                },
                                {"type": "extra", "content": "\n"},
                            ],
                            [
                                {"type": "extra", "content": "\t\t"},
                                {"type": "property", "content": "Y"},
                                {"type": "extra", "content": " "},
                                {"type": "extra", "content": "="},
                                {"type": "extra", "content": " "},
                                {"type": "value", "content": remove_excess_zeros(0)},
                                {"type": "extra", "content": "\n"},
                            ],
                        ],
                    },
                ],
            )


def max_length_to_offsets_2(line_tokens):
    for token in line_tokens:
        if token["type"] == "property":
            if token["content"] == "MaxLength":
                token["content"] = "ContractedOffset"

                for token_2 in line_tokens:
                    if token_2["type"] == "value":
                        old_value = float(token_2["content"])
                        token_2["content"] = "Vector"

                        line_tokens.append(
                            {
                                "type": "children",
                                "content": [
                                    [
                                        {"type": "extra", "content": "\t\t"},
                                        {"type": "property", "content": "X"},
                                        {"type": "extra", "content": " "},
                                        {"type": "extra", "content": "="},
                                        {"type": "extra", "content": " "},
                                        {
                                            "type": "value",
                                            "content": remove_excess_zeros(
                                                old_value / 2
                                            ),
                                        },
                                        {"type": "extra", "content": "\n"},
                                    ],
                                    [
                                        {"type": "extra", "content": "\t\t"},
                                        {"type": "property", "content": "Y"},
                                        {"type": "extra", "content": " "},
                                        {"type": "extra", "content": "="},
                                        {"type": "extra", "content": " "},
                                        {
                                            "type": "value",
                                            "content": remove_excess_zeros(0),
                                        },
                                        {"type": "extra", "content": "\n"},
                                    ],
                                ],
                            }
                        )

                        return old_value


def iconfile_path_to_thumbnail_generator(section, output_folder_path):
    if {"type": "property", "content": "DataModule"} in section:
        for a in section:
            if a["type"] == "children":
                b = a["content"]
                for c in b:
                    if {"type": "property", "content": "IconFile"} in c and {
                        "type": "value",
                        "content": "ContentFile",
                    } in c:
                        for token in c:
                            if token["type"] == "children":
                                subchildren = token["content"]
                                # print(subchildren)

                                for subline_tokens in subchildren:
                                    if {
                                        "type": "property",
                                        "content": "FilePath",
                                    } in subline_tokens:
                                        # print(subline_tokens)
                                        for subtoken in subline_tokens:
                                            if subtoken["type"] == "value":
                                                # print(subtoken)
                                                iconfile_path = subtoken["content"]
                                                thumbnail_generator.generate_thumbnail(
                                                    iconfile_path, output_folder_path
                                                )


def duplicate_script_path(parsed_subset):
    pass


def pie_menu_fix(section: list):
    """FOR Actors ONLY (I don't believe other entities need this change)

    Conversion:

            AddActor = <Actor Type>
                    AddPieSlice = PieSlice
                            Direction = 2
                            ScriptPath = something.lua
    -->
            AddActor = <Actor Type>
                    PieMenu = PieMenu
                            CopyOf = <Default Pie Menu preset for actor type goes here>
                            AddPieSlice = PieSlice
                                    Direction = 2
                                    ScriptPath = something.lua

    """

    # TODO: Account for pie slices being added non-consecutively

    if not section:
        return
    if not ini_rules_utils.has_children(section):
        return
    if not ini_rules_utils.line_contains_property(section, "AddActor"):
        return

    # Pie constants (pulled from source)
    MAX_PIE_QUADRANT_SIZE = 5
    MAX_PIE_SLICES = MAX_PIE_QUADRANT_SIZE * 4
    DEFAULT_PIES = {
        # Sizes: number of slices in the preset
        # 0 = Up, 1 = Down, 2 = Left, 3 = Right, 4 = Any
        "Actor": {
            "sizes": [1, 0, 0, 0],
            "preset": "Default Actor Pie Menu",
        },
        "AHuman": {
            "sizes": [2, 2, 2, 2],
            "preset": "Default Human Pie Menu",
        },
        "ACrab": {
            "sizes": [2, 2, 2, 2],
            "preset": "Default Crab Pie Menu",
        },
        "Turret": {
            "sizes": [2, 0, 0, 1],
            "preset": "Default Turret Pie Menu",
        },
        "ACDropShip": {
            "sizes": [2, 1, 1, 1],
            "preset": "Default Craft Pie Menu",
        },
        "ACRocket": {
            "sizes": [2, 1, 1, 1],
            "preset": "Default Craft Pie Menu",
        },
    }

    # Make sure we're one of the actors that need pie menu adjustments
    s_val = ini_rules_utils.line_contains_any_values(section, DEFAULT_PIES)
    if not s_val or s_val not in DEFAULT_PIES:
        return

    # Get all added slices, if we have any.
    slices = ini_rules_utils.get_children_with_property_shallow(section, "AddPieSlice")
    if not slices:
        return

    sliceDirCounts = DEFAULT_PIES[s_val]["sizes"]
    sliceCount = sum(sliceDirCounts)

    # get the direction counts of the slices so we can change if need be.
    dirs = ini_rules_utils.get_values_of_properties_of_children_shallowly(
        [x[1] for x in slices], "Direction"
    )

    # TODO: Comment out pie slices when we're above the max pie slice limit.

    # Keep track of and update slice directions.
    for x in dirs:
        dir = int(x[0])
        line = x[1]
        if sliceDirCounts[dir] == MAX_PIE_QUADRANT_SIZE:
            ini_rules_utils.set_line_value(line, 4)
        else:
            sliceDirCounts[dir] += 1
        sliceCount += 1

    # get the indent of the first slice (we'll need it later)
    indent = ini_rules_utils.get_indent(slices[0][1])
    # Create the parent PieMenu and move everything inside it.
    PT = ini_tokenizer.get_tokens_from_str(("\t" * indent) + "PieMenu = PieMenu\n")
    PieMenu = ini_cst.get_cst(PT, depth=indent)[0]
    CT = ini_tokenizer.get_tokens_from_str(
        ("\t" * (indent + 1)) + f"CopyOf = {DEFAULT_PIES[s_val]['preset']}\n"
    )
    CopyOf = ini_cst.get_cst(CT, depth=indent + 1)[0]
    # indent all the existing slices by one so they can be
    # put in the pie menu appropriately
    for i, x in slices:
        ini_rules_utils.indent(x)

    PieMenu.append({"type": "children", "content": [CopyOf] + [x for i, x in slices]})

    # TODO: Don't assume the lines are read in-order.
    # Add the new PieMenu and remove the PieSlices from the section's children
    secChildren = ini_rules_utils.get_children(section)
    secChildren.insert(slices[0][0], PieMenu)

    for x in range(len(slices) - 1, -1, -1):
        ind = slices[x][0]
        secChildren.pop(ind + 1)

    # We should be done here.


def shovel_flash_fix(children):
    """
    SpriteFile = ContentFile
            FilePath = Ronin.rte/Effects/Pyro/Flashes/ShovelFlash.png
    FrameCount = 2
    ->
    SpriteFile = ContentFile
            FilePath = Ronin.rte/Devices/Tools/Shovel/Effects/ShovelFlash.png
    FrameCount = 1
    """

    # TODO: Make this recursive somehow.
    for line_tokens in children:
        for token in line_tokens:
            if token["type"] == "property":
                if token["content"] == "SpriteFile":
                    # TODO: Check if the value "ContentFile" is also used, because "SpriteFile" might be able to have other values in the future!

                    for token_2 in line_tokens:
                        if token_2["type"] == "children":
                            for subline_tokens in token_2["content"]:
                                for subtoken in subline_tokens:
                                    if (
                                        subtoken["type"] == "property"
                                        and subtoken["content"] == "FilePath"
                                    ):
                                        for subtoken in subline_tokens:
                                            if subtoken["type"] == "value" and subtoken[
                                                "content"
                                            ] in (
                                                "Ronin.rte/Devices/Sprites/ShovelFlash.bmp",
                                                "Ronin.rte/Effects/Pyro/Flashes/ShovelFlash.png",
                                            ):
                                                subtoken[
                                                    "content"
                                                ] = "Ronin.rte/Devices/Tools/Shovel/Effects/ShovelFlash.png"

                                                shovel_flash_fix_change_frame_count(
                                                    children
                                                )


def shovel_flash_fix_change_frame_count(children):
    for line_tokens2 in children:
        for token2 in line_tokens2:
            if token2["type"] == "property":
                if token2["content"] == "FrameCount":
                    for token3 in line_tokens2:
                        if token3["type"] == "value":
                            if token3["content"] == "2":
                                token3["content"] = "1"


def add_grip_strength_if_missing(section):
    """
    TODO: Check if this description is accurate to what *actually* was decided between me and Gacyr regarding the future behavior of GripStrength.

    GripStrength was added in pre4 as an optional property to Arms.
    It defaulted to JointStrength if it wasn't defined for an Arm, but this suddenly caused a lot of actors in old mods to throw their HeldDevices away.
    In response, pre4.1 made JointStrength a non-optional property, with the idea being that this function could then fix old mods by adding GripStrength = <high_value> to them.
    """

    # TODO: Make this recursive somehow.
    if ini_rules_utils.line_contains_property_and_value(section, "AddActor", "Arm"):
        for token in section:
            if token["type"] == "children":
                children = token["content"]

                # The second condition will make sure that GripStrength isn't added to an Arm without a GripStrength
                # that CopyOfs an Arm that *does* have a GripStrength.
                if not ini_rules_utils.children_contain_property_shallowly(
                    children, "GripStrength"
                ) and not ini_rules_utils.children_contain_property_shallowly(
                    children, "CopyOf"
                ):
                    children.append(
                        [
                            {"type": "extra", "content": "\t"},
                            {"type": "property", "content": "GripStrength"},
                            {"type": "extra", "content": " "},
                            {"type": "extra", "content": "="},
                            {"type": "extra", "content": " "},
                            {
                                "type": "value",
                                "content": str(
                                    cfg.ARBITRARILY_HIGH_DEFAULT_GRIP_STRENGTH
                                ),
                            },
                            {"type": "extra", "content": "\n"},
                        ]
                    )


def remove_slterrain_properties(section):
    """
    Remove 'Offset' and 'ScrollRatio' property from SLTerrain objects.
    Fixes PlaceTerrainObject's
    Remove's DrawTransparent

    Conversion Rule:
           Terrain = SLTerrain
           PresetName = Some Terrain
           BitmapFile = ContentFile
                   FilePath = Base.rte/Scenes/Terrains/Some_Scene.png
           Offset = Vector
                   X = 1667
                   Y = 462
           WrapX = 0
           WrapY = 0
           DrawTransparent = 1
           ScrollRatio = Vector
                   X = 1
                   Y = -1

           ->

           Terrain = SLTerrain
           PresetName = Some Terrain
           BitmapFile = ContentFile
                   FilePath = Base.rte/Scenes/Terrains/Some_Scene.png
           WrapX = 0
           WrapY = 0
    """

    if not section:
        return
    if not ini_rules_utils.has_children(section):
        return
    # Scene objects can have terrain as children, and those need to be changed too.
    if ini_rules_utils.line_contains_value(section, "Scene"):
        children = ini_rules_utils.get_children_with_property_and_value_shallow(
            section, "Terrain", "SLTerrain"
        )
        for i, child in children:
            remove_slterrain_properties(child)
    if not ini_rules_utils.line_contains_property_and_value(
        section, "Terrain", "SLTerrain"
    ):
        return

    ini_rules_utils.remove_properties_from_section(
        section, ["Offset", "ScrollRatio", "DrawTransparent", "ScaleFactor"]
    )

    # get terrainobjects of this terrain ent, if any, replace their loc with pos
    ptoChildren = ini_rules_utils.get_children_with_property_shallow(
        section, "PlaceTerrainObject"
    )
    for i, child in ptoChildren:
        ini_rules_utils.replace_property_names_of_children_shallowly(
            child, "Location", "Position"
        )


# this might belong in utils but i'm keeping it here for now
# this can work recursively if needed in case the entity might
# be nested inside a section (material presets, for example)
def rename_section_preset(section, entity, old, new, recursive=False):
    """Renames a preset name from old to new of specified entity.
    Ideally, we should be able to put these in a JSON file, but for now, it'll be in here.

    AddBackgroundLayer = <entity>
            PresetName = <old>
            AddToGroup = Near Backdrops
    ->
    AddBackgroundLayer = <entity>
            PresetName = <new>
            AddToGroup = Near Backdrops
    """

    if not section:
        return
    if not ini_rules_utils.has_children(section):
        return

    children = ini_rules_utils.get_children(section)
    if recursive:
        for line in children:
            rename_section_preset(line, entity, old, new, recursive)

    if not ini_rules_utils.line_contains_value(section, entity):
        return

    for line in children:
        ini_rules_utils.replace_value_of_property(line, "PresetOf", new, old)
