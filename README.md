# GBA Emulator Compilation Build Scripts

Python 3 builder scripts for the following emulators for Gameboy Advance:
Emulator|Target System|Author(s)|Released
:-------|:------------|:--------|:---
[PocketNES](https://github.com/Dwedit/PocketNES/releases)|Nintendo NES|Loopy, later FluBBa, Dwedit|Jan 2001?
[PCEAdvance](https://web.archive.org/web/20150430211123/http://www.ndsretro.com/gbadown.html)|NEC PC Engine|FluBBa|Apr 2003
[Goomba](http://goomba.webpersona.com)|Nintendo Gameboy|FluBBa|Oct 2003
[SNESAdvance](https://web.archive.org/web/20080208234615/http://www.snesadvance.org/index.html)|Nintendo SNES|Loopy, FluBBa|Feb 2005
[SMSAdvance](https://web.archive.org/web/20150430211123/http://www.ndsretro.com/gbadown.html)|SEGA Master System, Game Gear, SG-1000|FluBBa|Jul 2005
[Cologne](https://web.archive.org/web/20150430211123/http://www.ndsretro.com/gbadown.html)|ColecoVision|FluBBa|Jan 2006
[Goomba Color](https://www.dwedit.org/gba/goombacolor.php)|a Goomba fork to add Gameboy Color|Dwedit|Jan 2006
[MSXAdvance](https://web.archive.org/web/20150430211123/http://www.ndsretro.com/gbadown.html)|MSX-1 (*version 0.2 is most compatible*)|FluBBa|Mar 2006
[NGPAdvance](https://web.archive.org/web/20150430211123/http://www.ndsretro.com/gbadown.html)|SNK Neo Geo Pocket / NGP Color|Flubba|Jul 2008
[Jagoomba](https://github.com/EvilJagaGenius/jagoombacolor/releases)|enhanced Goomba Color fork|Jaga|Nov 2021


## Purpose
The scripts combine the emulator binary with the game ROMs and their required metadata into a ```.gba``` executable for Gameboy Advance. Since the scripts are written in Python 3 they will run on most present-day platforms, helping to preserve these technical marvels.


## Usage
You can drag and drop multiple file selections onto the shell window in which you are preparing the command line. Most options are not needed since they have sensible defaults. This makes these scripts well suited for building large compilations very easily. Usually the shell will alphabetically sort multiple file selections.

Each script has help information accessible via the ```-h``` command line option. For example:
```
usage: pocketnes_compile.py [-h] [-s SPLASHSCREEN] [-e EMUBINARY]
                            [-db DATABASE] [-dbn] [-m] [-c] [-o OUTPUTFILE]
                            [-sav] [-pat]
                            romfile [romfile ...]

This script will assemble the PocketNES emulator and NES ROMs into a Gameboy
Advance ROM image. It is recommended to type the script name, then drag and
drop multiple ROM files onto the shell window, then add any additional
arguments as needed.

positional arguments:
  romfile          .nes ROM image to add to compilation. Drag and drop
                   multiple files onto your shell window.

optional arguments:
  -h, --help       show this help message and exit
  -s SPLASHSCREEN  76800 byte raw 240x160 15bit splashscreen image
  -e EMUBINARY     PocketNES binary, defaults to pocketnes.gba
  -db DATABASE     PocketNES Menu Maker Database file which stores optimal
                   flags and sprite follow settings for many games, defaults
                   to pnesmmw.mdb
  -dbn             use game titles from PocketNES Menu Maker database
  -m               mark small ROMs suitable for link transfer
  -c               clean brackets from ROM titles
  -o OUTPUTFILE    compilation output filename, defaults to pocketnes-
                   compilation.gba
  -sav             for EZ-Flash IV firmware 1.x - create a blank 64KB .sav
                   file for the compilation, store in the SAVER folder, not
                   needed for firmware 2.x which creates its own blank saves
  -pat             for EZ-Flash IV firmware 2.x - create a .pat file for the
                   compilation to force 64KB SRAM saves, store in the PATCH
                   folder

coded by patters in 2022
```


## Features
- All scripts:
  - Drag and drop a selection of ROMs onto the shell window after typing the script name, to easily add multiple ROMs
  - Blank SRAM save file of the appropriate size can now be created automatically using the ```-sav``` option
  - GSS patch file for EZ-Flash IV firmware 2.x (to force 64KB SRAM saves) can now be created automatically using the ```-pat``` option
  - Patch file data is encoded within the script body - no external dependency
  - Splash screen support
  - Optional overrides of file paths
  - Can clean brackets from ROM titles
- Many scripts (as applicable):
  - Auto-detection of ROM types for emulators that support multiple types with specific header requirements
  - Region options and PAL timings are now auto-detected based on ROM naming
  - Boot-to-BIOS support
  - Small ROMs suitable for link transfer (<192KB) can be marked in the game list
- PCEAdvance:
  - ISO and TCD tracklist support for PC Engine CD-ROM
  - Some sprite follow settings (those featured in gamelist.txt)
  - CD BIOS automatically added when an ISO image is added, and titled with the ISO name
- Goomba:
  - works around an [EZ-Flash issue](https://www.dwedit.org/dwedit_board/viewtopic.php?id=643) where some ROMs would cause duplicate game list entries
  - can prefer ROM filenames rather than original ROM game titles in the game list
- PocketNES:
  - can lookup ROM checksum in PocketNES Menu Maker database ([pnesmmw.mdb](https://web.archive.org/web/20060208115559/http://www.pocketnes.org/tools/pnesmmw12a.zip)) for optimal ROM settings, sprite/mem follow
  - can prefer game titles from PocketNES Menu Maker database
  - 256 byte alignment of all ROM data for [optimum performance](https://github.com/Dwedit/PocketNES/issues/5#issuecomment-1107541215)
- SNESAdvance:
  - SuperDAT database is mandatory ([snesadvance.dat](https://web.archive.org/web/20080208234615/http://www.snesadvance.org/files/superdat20060124-mog123.zip), some additional supported titles [here](https://github.com/m45t3r/snes9x4d/blob/master/snesadvance.dat))
  - default graphics assets are encoded in the script, external skin files are ingested if present
  - can accept headered or unheadered ROMs (.smc/.sfc)
  - can export header-stripped ROMs
  - can prefer game titles from SuperDAT database


## Automation
With a simple for loop the scripts can also create a standalone executable for each game in a folder.

**Bash**:

```for file in *.pce *.iso ; do ./pceadvance_compile.py "${file}" -o "${file%.*}.gba" ; done```

**Windows**:

```for %f in (*.pce *.iso) do @pceadvance_compile.py "%f" -o "%~nf.gba"```


## Emulator Tips
#### Cologne
- find the BIOS rom with the no-delay patch to speed up the boot time: "ColecoVision BIOS (1982) (No Title Delay Hack)"
- R+Start to bring up the virtual controller keypad
#### MSXAdvance
- the BIOS you need is "MSX System v1.0 + MSX BASIC (1983)(Microsoft)[MSX.ROM]"
- R+Start to bring up the virtual keyboard
- the emulator does not auto-select the correct mapper. You often need to change this (typically to Konami5) in Other Settings and restart the emulator for it to take effect
- [compatibility list](https://web.archive.org/web/20070612060046/http://boards.pocketheaven.com/viewtopic.php?t=3768)
- [versions 0.3 and 0.4 are broken](https://gbatemp.net/threads/msxadvance-compatibility-many-games-in-gamelist-txt-dont-work.609615/)
#### PCEAdvance
- audio tends to work pretty well in mixer mode, but you do need to restart the emulator after enabling it
- [CD-ROM ISO extracting](https://gbatemp.net/threads/pceadvance-cd-rom-support-howto-required.610542/
- [CD-ROM / Super CD-ROM titles list](https://gamicus.fandom.com/wiki/List_of_PC-Engine_CD-ROM²_video_games)
#### SMSAdvance
- BIOS booting (effectively a blank 16KB ROM image) requires the system type to be hard set to Master System, assuming Master System BIOS games, because without a ROM the emulator cannot guess which system BIOS (SMS or GG) should be loaded
#### SNESAdvance
- press Start+Select+A+B for the emulator menu
- press Select+Up/Down to change screen offset
- [list of best functioning games](https://web.archive.org/web/20050305113636/http://ygodm.tonsite.biz/snesadv/snesadv_gamelist.html)
