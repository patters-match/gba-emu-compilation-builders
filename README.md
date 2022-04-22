# GBA Emulator Compilation Build Scripts

Python 3 builder scripts for the following Gameboy Advance emulators, in date order of initial release:
- [PocketNES](https://github.com/Dwedit/PocketNES/releases) for Nintendo NES (by Loopy, Jan 2001?, later FluBBa, Dwedit)
- [PCEAdvance](https://web.archive.org/web/20150430211123/http://www.ndsretro.com/gbadown.html) for PC Engine (by FluBBa, Apr 2003)
- [Goomba](http://goomba.webpersona.com) for the original Gameboy (by FluBBa, Oct 2003)
- [SMSAdvance](https://web.archive.org/web/20150430211123/http://www.ndsretro.com/gbadown.html) for SEGA Master System, Game Gear, SG-1000 (by FluBBa, Jul 2005)
- [Cologne](https://web.archive.org/web/20150430211123/http://www.ndsretro.com/gbadown.html) for ColecoVision (by FluBBa, Jan 2006)
- [Goomba Color](https://www.dwedit.org/gba/goombacolor.php) a Goomba fork to add Gameboy Color (by Dwedit, Jan 2006)
- [MSXAdvance](https://web.archive.org/web/20150430211123/http://www.ndsretro.com/gbadown.html) for MSX-1 (by FluBBa, Mar 2006 - v0.2 is best)
- [NGPAdvance](https://web.archive.org/web/20150430211123/http://www.ndsretro.com/gbadown.html) for Neo Geo Pocket / NGP Color (by Flubba, Jul 2008)
- [Jagoomba](https://github.com/EvilJagaGenius/jagoombacolor/releases) enhanced Goomba Color fork for Gameboy / Gameboy Color (by Jaga, Nov 2021)

## Purpose
The scripts combine the emulator binary with the game ROMs and their required metadata into a ```.gba``` executable for Gameboy Advance. Since they are Python 3 scripts they will run on most contemporary platforms, unlike the original 32bit Windows binaries.

With a simple for loop the scripts can also create a standalone executable for each game in a folder, for instance:
```for file in *.pce *.iso ; do ./pceadvance_compile.py "${file}" -o "${file%.*}.gba" ; done```

## Usage
You can drag and drop multiple file selections onto the shell window in which you are preparing the command line. This makes these scripts well suited for building large compilations. Usually the shell will alphabetically sort multiple file selections.

Each script has help information accessible via the ```-h``` command line option. For example:
```
usage: smsadvance_compile.py [-h] [-s SPLASHSCREEN] [-b BIOS [BIOS ...]] [-bb] [-e EMUBINARY] [-m] [-o OUTPUTFILE] [-sav] [-pat]
                             [romfile [romfile ...]]

This script will assemble the SMSAdvance emulator and Master System/Game Gear/SG-1000 ROMs into a Gameboy Advance ROM image. It is
recommended to type the script name, then drag and drop multiple ROM files onto the shell window, then add any additional arguments as
needed.

positional arguments:
  romfile             .sms/.gg/.sg ROM image to add to compilation. Drag and drop multiple files onto your shell window.

optional arguments:
  -h, --help          show this help message and exit
  -s SPLASHSCREEN     76800 byte raw 240x160 15bit splashscreen image
  -b BIOS [BIOS ...]  optional BIOS rom image(s). Since both a Master System and a Game Gear BIOS can be added, use this argument after
                      specifying the game ROMs
  -bb                 allow boot to BIOS-integrated games, via an '-- Empty --' romlist entry. Requires BIOS to be enabled in the
                      SMSAdvance options, and System must be changed from Auto to Master System since it cannot be autodetected when
                      there is no ROM
  -e EMUBINARY        SMSAdvance binary, defaults to smsadvance.gba
  -m                  mark small ROMs suitable for link transfer
  -o OUTPUTFILE       compilation output filename, defaults to smsadv-compilation.gba
  -sav                for EZ-Flash IV firmware 1.x - create a blank 64KB .sav file for the compilation, store in the SAVER folder, not
                      needed for firmware 2.x which creates its own blank saves
  -pat                for EZ-Flash IV firmware 2.x - create a .pat file for the compilation to force 64KB SRAM saves, store in the
                      PATCH folder

coded by patters in 2022

```
