# cc-legacy-mod-converter

![project-icon](cclmc-icon.png)

## Introduction
Running `convert.py` converts the legacy `Cortex Command` mods to the modern `Cortex Command Community Project` mods, but as some steps are too hard to automate you'll likely have to do some adjustments in your input folder to complete the conversion process.

## How it works
`convert.py` has the `replace_variables_list` variable at the top which lists common properties, filepaths and functions that will automatically be changed in order for an outdated mod to be usable in `Cortex Command Community Project`.

It also contains the `manual_replace_variables_list`, which has the same function as the `replace_variables_list` variable, but additionally will write any lines it changed into the automatically created `manually-edit-these-lines.txt` file found in the `output` folder after running `convert.py`. 

> "There are going to be cases that require user intervention. Priority, for example, is one of them. Few things should be setting sound priority, and the scale has completely changed such that 0 is highest and 128 (I think) is lowest. The correct way to deal with this is, either at the time of or at the end, show the user these cases and either tell them to deal with it manually, or give them a few options." -Gacyr

## Contributing
Feel free to make pull requests for any additional cases that you want `convert.py` to support, but please make sure to add the case to `mod-porting-guide.txt` with a check mark in front of it afterwards as well. :)
