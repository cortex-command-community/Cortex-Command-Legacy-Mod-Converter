# cc-legacy-mod-converter

`convert.py` attempts to convert the legacy `Cortex Command` mods to the modern `Cortex Command Community Project` mods,
but you'll likely have to do some final finishing touches to succesfully complete the conversion.

> There are going to be cases that require user intervention. Priority, for example, is one of them. Few things should be setting sound priority,
and the scale has completely changed such that 0 is highest and 128 (I think) is lowest.
The correct way to deal with this is, either at the time of or at the end,
show the user these cases and either tell them to deal with it manually, or give them a few options. -Gacyr

There are many edge cases that won't be covered by `convert.py`, but `mod-porting-guide.txt` has a check mark in front of every case that *is* handled automatically.

Feel free to make pull requests for any additional cases that you want `convert.py` to support,
but please add a check mark in front of every additionally supported case in `mod-porting-guide.txt` afterwards too. :)
