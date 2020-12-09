<p align="center"><img src="Media/cclmc-icon.png" alt="Legacy Mod Converter icon"></p>
<h1 align="center">Cortex Command Legacy Mod Converter</h1>

## Introduction
This project automates ***most*** of the conversion work required to convert the legacy (old) `Cortex Command` mods into `Cortex Command Community Project` compatible mods.

## Getting started
Download the [***Legacy Mod Converter***](http://www.mediafire.com/file/7dd1xecs5sgvd7t/Legacy_Mod_Converter.exe/file) program. Create a new folder and put your legacy mods that you want to convert in it. Run the Legacy Mod Converter program.

If you get a "`Microsoft Defender SmartScreen prevented an unrecognized app from starting. Running this app might put your PC at risk.`" popup message when trying to run the program you should press `More info` and then `Run anyway`.

<p align="center"><img src="Media/cclmc-screenshot.png" alt="Legacy Mod Converter screenshot"></p>

## Disclaimer
This program will do most of the conversion work for you, but some conversion steps are too hard to automate, so it's likely that `CCCP` will still crash or print errors in the console. If this happens you'll have to manually fix these issues in the legacy mod folder. If you want to properly fix these errors then you should download this repository and follow the instructions below so you can add your own conversion cases to `conversion_rules.py`.

## How to add your own conversion rules
* Download Python 3 and this GitHub repository.
* Change your directory to the `cc-legacy-mod-converter` repository in your terminal.
* Run `python main.py` when you want to convert old mods.
* `conversion_rules.py` has the `conversion_rules` dictionary inside of it. The dictionary contains entries that look like `'foo': 'bar',` which means means that any time `foo` is encountered in a legacy mod it will be replaced with `bar`. You can also add extra conversion cases to it; see the next sections on how to do this in detail.

## Tutorials on constructing conversion rules efficiently
* [Fixing CCCP crashes/errors with the program Everything](https://github.com/cortex-command-community/Cortex-Command-Legacy-Mod-Converter/wiki/Fixing-CCCP-crashes-errors-with-the-program-Everything)

## Contributing
Feel free to submit `Pull Requests` or `Issues` on this GitHub project for any additional cases that you'd like to have supported.

**You don’t need all of these programs to get started and feel free to use alternative programs:**
* [Download “Everything”](https://voidtools.com/) - Like File Explorer on Windows. Very fast.
* [Download “SourceTree”](https://www.sourcetreeapp.com/) - Like GitHub Desktop. Allows searching for specific words across all commits.
* [Download “NotePad++”](https://notepad-plus-plus.org/downloads/) - Like Notepad. Allows mass replacing across many files. You can also use an IDE like [VS Code](https://code.visualstudio.com/) instead for this.

## Getting help
If you need help with anything, you can contact the creator of this repository directly (`#MyNameIsTrez1585` on Discord), or you can ask the friendly regulars in the CCCP Discord server in `#modding-discussion` for help. It helps us if you mention where you've gotten stuck while reading this tutorial, so please do that! :)