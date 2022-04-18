<p align="center"><img src="Media/legacy-mod-converter-icon.png" alt="Legacy Mod Converter icon"></p>
<h1 align="center">Cortex Command Legacy Mod Converter</h1>

## Introduction
This project automates ***most*** of the conversion work required to convert the legacy (old) `Cortex Command` mods into `Cortex Command Community Project` compatible mods.

<p align="center"><img src="Media/legacy-mod-converter-screenshot.png" alt="Legacy Mod Converter screenshot"></p>

## Getting started
Follow the instructions for the latest release [here](https://github.com/cortex-command-community/Cortex-Command-Legacy-Mod-Converter/releases).

## Disclaimer
This program will do most of the conversion work for you, but even though this converter will already automatically apply more than 500 mod changes that have been made between Cortex Command and CCCP there are always more changes out there that haven't been added to the converter yet.

It's for this reason that it's almost guaranteed that CCCP will still crash with a crash message or with errors in the console after conversion, but the point of this converter is to do 99% of the work for you, 100% is only realistic for some tiny mods. You'll want to manually fix these issues using the instructions in the next section.

## What are conversion rules
Conversion rules are a way of informing the program of the changes that have been made between Cortex Command and CCCP and how it can fix them. These conversion rules are stored in JSON files in the `ConversionRules` folder. You absolutely don't need to have any programming experience to start adding conversion rules to any of the JSON files.

Take for example this line from `ConversionRules/Misc.json`:

`"Round M16": "Round Ronin M16",`

What this line of JSON says is that whenever the thing on the left is encountered in a mod, it should be replaced with whatever is on the right of it. So, this conversion rule says that whenever `Round M16` is encountered in a mod that's being converted it should be changed to `Round Ronin M16` by the converter.

<p align="center"><img src="Media/conversion-rules-screenshot.png" alt="Conversion rules screenshot"></p>

## How to add your own conversion rules
Follow [this tutorial on fixing CCCP crashes and errors with Fork](https://github.com/cortex-command-community/Cortex-Command-Legacy-Mod-Converter/wiki/Fixing-CCCP-crashes-and-errors-with-Fork).

## If you want to run the latest version of the converter
Clone or download this repository, run `pip install -r requirements.txt` and then run `python main.py`. Python version 3.10.1 or newer is recommended.

## Contributing
Feel free to submit `Pull Requests` or `Issues` on this GitHub project for any additional cases that you'd like to have supported.

## Getting help
If you need help with anything you can contact the creator of this repository directly (`#MyNameIsTrez1585` on Discord), or you can ask the friendly regulars in the CCCP Discord server in `#modding-discussion` for help. It helps us if you mention where you've gotten stuck while reading this tutorial, so please do that! :)
