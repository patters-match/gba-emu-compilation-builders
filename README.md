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

## Usage
You can drag and drop multiple file selections onto the shell window in which you are preparing the command line. Most options are not needed since they have sensible defaults. This makes these scripts well suited for building large compilations very easily. Usually the shell will alphabetically sort multiple file selections.

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

## Features
- Drag and drop a selection of ROMs onto the shell window after typing the script name to easily add multiple ROMS
- Auto-detection of ROM types for emulators that support multiple types with specific header requirements (sms/gg, pce/iso)
- Region options and PAL timings are now auto-detected based on ROM naming
- Blank ```.sav``` SRAM save files of the appropriate size can now be created automatically using the ```-sav``` option
- ```.pat``` files for EZ-Flash IV firmware 2.0 (to force 64KB SRAM saves) can now be created automatically using the ```-pat``` option
- Patch file data is encoded within the script body - no external dependency
- Splash screen support
- Optional overrides of file paths
- Boot-to-BIOS support
- Small ROMs suitable for link transfer (<192KB) can optionally be marked in the game list
- PCEAdvance:
  - ISO and TCD tracklist support for PC Engine CD-ROM
  - Some sprite follow settings for PC Engine (those featured in gamelist.txt)
  - CD BIOS automatically added when an ISO image is added, and titled with the ISO name
- Goomba:
  - works around an EZ4 issue where some ROMs would cause duplicate game list entries
  - optionally allows ROM filenames to replace the original ROM header names in the game list
- PocketNES:
  - will compare the ROM checksum with the PocketNES Menu Maker database (pnesmmw.mdb, when present) for optimal ROM settings, sprite follow value etc.

## Automation
With a simple for loop the scripts can also create a standalone executable for each game in a folder.

**Bash**:

```for file in *.pce *.iso ; do ./pceadvance_compile.py "${file}" -o "${file%.*}.gba" ; done```

**Windows**:

```for %f in (*.pce *.iso) do @pceadvance_compile.py "%f" -o "%~nf.gba"```
