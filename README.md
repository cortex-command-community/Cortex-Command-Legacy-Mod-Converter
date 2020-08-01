# Cortex Command Legacy Mod Converter

## Introduction
This project automates ***most*** of the conversion work required to convert the legacy `Cortex Command` mods into `Cortex Command Community Project` compatible mods.

![project-icon](cclmc-icon.png)

## Converting
Put the mods you want to convert in the `input` folder and run `convert.py`. After `convert.py` is done, the converted mods are found in the `output` folder and can then be tested in `CCCP`.

## Disclaimer
This program will do most of the conversion work for you, but some conversion steps are too hard to automate, so it's likely that `CCCP` will still crash and/or output errors into the console. If this happens, you'll have to manually make some final adjustments to the converted mods found in the `output` folder.

> "There are going to be cases that require user intervention. Priority, for example, is one of them. Few things should be setting sound priority, and the scale has completely changed such that 0 is highest and 128 (I think) is lowest. The correct way to deal with this is, either at the time of or at the end, show the user these cases and either tell them to deal with it manually, or give them a few options." -Gacyr

## How it works
### `safe_replace_dict`
`convert.py` has the `safe_replace_dict` variable declared at the top, which lists common properties, filepaths and functions that will automatically be replaced.

### `unsafe_replace_dict`
`convert.py` also contains the `unsafe_replace_dict` variable, which has the same function as `safe_replace_dict`, but will additionally write information about the lines it replaced into `manually-edit.txt`, which is found in the `output` folder after running `convert.py`.

## Contributing
Feel free to submit `Pull Requests` or `Issues` on this GitHub project for any additional cases that you'd like `convert.py` to support that haven't been listed at the top of `convert.py` as a `TODO` yet.