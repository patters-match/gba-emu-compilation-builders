# GBA Emulator Compilation Build Scripts

Python 3 builder scripts for the following emulators for Gameboy Advance:
Emulator|Target System|Author(s)|1st Release
:-------|:------------|:--------|:---
[PocketNES](https://github.com/Dwedit/PocketNES/releases)|Nintendo NES|Loopy, later FluBBa, Dwedit|Jan 2001?
[ZXAdvance](https://www.gamebrew.org/wiki/ZXAdvance_GBA)|Sinclair ZX Spectrum 48K|TheHiVE|May 2001
[PCEAdvance](https://web.archive.org/web/20150430211123/http://www.ndsretro.com/gbadown.html)|NEC PC Engine / Super CD-ROM²|FluBBa|Apr 2003
[Goomba](http://goomba.webpersona.com)|Nintendo Gameboy|FluBBa|Oct 2003
[HVCA](https://www.gamebrew.org/wiki/HVCA_GBA)|Nintendo NES / Famicom Disk System|outside-agb?|Sep 2004
[Wasabi](https://github.com/FluBBaOfWard/WasabiGBA)|Watara Supervision|FluBBa|Nov 2004
[SNESAdvance](https://web.archive.org/web/20080208234615/http://www.snesadvance.org/index.html)|Nintendo SNES|Loopy, FluBBa|Feb 2005
[SMSAdvance](https://web.archive.org/web/20150430211123/http://www.ndsretro.com/gbadown.html)|SEGA Master System / Game Gear / SG-1000|FluBBa|Jul 2005
[Cologne](https://web.archive.org/web/20150430211123/http://www.ndsretro.com/gbadown.html)|ColecoVision|FluBBa|Jan 2006
[Goomba Color](https://www.dwedit.org/gba/goombacolor.php)|Nintendo Gameboy / Gameboy Color|FluBBa, Dwedit|Jan 2006
[MSXAdvance](https://github.com/patters-syno/msxadvance)|MSX-1 *(version 0.2 is most compatible)*|FluBBa|Mar 2006
[Snezziboy](https://sourceforge.net/projects/snezziboy/files/snezziboy%20%28binaries%2Bsource%29/v0.26/)|Nintendo SNES|bubble2k|May 2006
[NGPGBA](https://github.com/FluBBaOfWard/NGPGBA)|SNK Neo Geo Pocket / Pocket Color|Flubba|Jul 2008
[Jagoomba](https://github.com/EvilJagaGenius/jagoombacolor/releases)|An enhanced Goomba Color fork|FluBBa, Dwedit, Jaga + various|Nov 2021


## Purpose
The scripts combine the emulator binary with the game ROMs and their required metadata into a ```.gba``` executable for Gameboy Advance. Since the scripts are written in Python 3 they will run on most present-day platforms, helping to preserve these technical marvels.

## Usage
```git clone https://github.com/patters-syno/gba-emu-compilation-builders```

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
  - ```-h``` for help
  - Drag and drop a selection of ROMs onto the shell window after typing the script name, to easily add multiple ROMs
  - Blank SRAM save file of the appropriate size can now be created automatically using ```-sav``` option
  - GSS patch file for EZ-Flash IV firmware 2.x (to force 64KB SRAM saves) can now be created automatically using ```-pat``` option
  - Patch file data is encoded within the script body - no external dependency
  - Optional overrides of file paths
  - Can clean brackets from ROM titles with ```-c``` option
- Some scripts (as applicable):
  - Splash screen support with ```-s``` option
  - Auto-detection of ROM types for emulators that support multiple types with specific header requirements
  - Region options and PAL timings are now auto-detected based on ROM naming
  - Boot-to-BIOS support with ```-bb``` option
  - Small ROMs suitable for link transfer (<192KB) can be marked in the game list with ```-m``` option
- MSXAdvance:
  - Detects appropriate mapper for added ROMs and records this in a previously unused byte in the header, can opt out using ```-nomap``` option
  - Use [my new fork of MSXAdvance v0.2](https://github.com/patters-syno/msxadvance) which adds auto mapper selection
- PCEAdvance:
  - ISO and TCD tracklist support for PC Engine CD-ROM²
  - Some sprite follow settings for "Unscaled (Auto)" display mode (those featured in gamelist.txt)
  - CD BIOS automatically added when an ISO image is added, and titled with the ISO name
  - Can trim compilation to fit within 16MB PSRAM with ```-trim``` option (needed for certain CD-ROM² titles)
- Goomba:
  - Works around an [EZ-Flash issue](https://www.dwedit.org/dwedit_board/viewtopic.php?id=643) where some ROMs would cause duplicate game list entries
  - Can prefer ROM filenames in the game list rather than original ROM game titles, with ```-f``` option
- PocketNES:
  - Will, if present, lookup ROM checksums in PocketNES Menu Maker database ([pnesmmw.mdb](https://web.archive.org/web/20060208115559/http://www.pocketnes.org/tools/pnesmmw12a.zip)) for optimal game settings, sprite/memory follow for "Unscaled (Follow)" display mode 
  - Can prefer game titles from PocketNES Menu Maker database with ```-dbn``` option
  - 256 byte alignment of all ROM data for [optimum performance](https://github.com/Dwedit/PocketNES/issues/5#issuecomment-1107541215)
- SNESAdvance:
  - SuperDAT database is mandatory ([snesadvance.dat](https://web.archive.org/web/20080208234615/http://www.snesadvance.org/files/superdat20060124-mog123.zip), some additional supported titles [here](https://github.com/m45t3r/snes9x4d/blob/master/snesadvance.dat))
  - Default graphics assets are encoded in the script, external skin files are ingested if present
  - Can accept headered or unheadered ROMs (.smc/.sfc)
  - Can export header-stripped ROMs with ```-strip``` option
  - Can prefer game titles from SuperDAT database with ```-dbn``` option
  - Verbose mode with ```-v``` option
- Snezziboy:
  - Each game must be bundled with its own emulator instance, though multiple games can be processed in one command line
  - Dat file database is mandatory ([snezzi.dat](https://web.archive.org/web/20090430142302/wiki.pocketheaven.com/Snezzi_dat)), but can use SNESAdvance SuperDAT also ([snesadvance.dat](https://web.archive.org/web/20080208234615/http://www.snesadvance.org/files/superdat20060124-mog123.zip), some additional supported titles [here](https://github.com/m45t3r/snes9x4d/blob/master/snesadvance.dat))
  - Can accept headered or unheadered ROMs (.smc/.sfc)
  - Can export header-stripped ROMs with ```-strip``` option
  - Verbose mode, to mimic original snezzi.exe builder with ```-v``` option
- HVCA:
  - Reconstructs FDS ROM headers if they are missing, which HVCA requires
  - Adds an exit function for EZ-Flash IV / 3in1 / Omega flashcarts
- ZXAdvance:
  - On first run use the ```-e``` builder option to extract the emulator from the original ZXAdvance exe file, will accept v1.0.1 or v1.0.1a
  - Adds an exit function for EZ-Flash IV / 3in1 / Omega flashcarts
  - Will retrieve game-specific controls configurations from ZXA.INI
  - Can create a Pogoshell plugin integrating the game configurations from ZXA.INI with the ```-p``` builder option
  - Can clean and sort the inifile using the ```-c``` option

## Automation
With a simple FOR loop the scripts can also create a standalone executable for each game in a folder.

**Bash**:

```for file in *.pce *.iso ; do ./pceadvance_compile.py "${file}" -o "${file%.*}.gba" ; done```

**Windows**:

```for %f in (*.pce *.iso) do @pceadvance_compile.py "%f" -o "%~nf.gba"```

If you own an EZ-Flash IV flashcart my curated collection of [exit-patched emulator binaries](https://github.com/patters-syno/gba-ezflash-iv-emulators) will be of interest.

---
## Emulator Tips
#### Cologne
- Find the BIOS rom with the no-delay patch to speed up the boot time: "ColecoVision BIOS (1982) (No Title Delay Hack)"
- R+Start to bring up the virtual controller keypad
#### MSXAdvance
- The BIOS you need is "MSX System v1.0 + MSX BASIC (1983)(Microsoft)[MSX.ROM]"
- R+Start to bring up the virtual keyboard
- Use [my new fork of MSXAdvance v0.2](https://github.com/patters-syno/msxadvance) which adds auto mapper selection
- An early [compatibility list](https://web.archive.org/web/20070612060046/http://boards.pocketheaven.com/viewtopic.php?t=3768)
- Versions 0.3 and 0.4 [are broken](https://gbatemp.net/threads/msxadvance-compatibility-many-games-in-gamelist-txt-dont-work.609615/)
#### PCEAdvance
- Audio tends to work pretty well in mixer mode, but you do need to restart the emulator after enabling it
- [CD-ROM ISO extracting info](https://github.com/patters-syno/pceadvance#pc-engine-cd-rom-support), and [this forum thread](https://gbatemp.net/threads/pceadvance-cd-rom-support-howto-required.610542/)
- [CD-ROM² / Super CD-ROM² / Arcade CD-ROM² titles lists, and TOCs](https://www.necstasy.net/)
- [Speedhacks howto](https://web.archive.org/web/20060508083011/http://boards.pocketheaven.com/viewtopic.php?t=27)
- Use [my new fork of PCEAdvance v7.5](https://github.com/patters-syno/pceadvance) to get additional RAM support for EZ-Flash IV and EZ-Flash 3in1 flashcarts 
#### SMSAdvance
- BIOS booting (effectively a blank 16KB ROM image) requires the system type to be hard set to Master System, assuming Master System BIOS games, because without a ROM the emulator cannot guess which system BIOS (SMS or GG) should be loaded
- "Lock toprows" is an option for Full Screen display mode useful for certain Master System games, such as Outrun, which can keeps the score/speedometer on screen despite cropping the image to the GBA resolution
#### SNESAdvance
- Start+Select+A+B for the emulator menu
- Select+Up/Down to change screen offset
- [List of best functioning games](https://web.archive.org/web/20050305113636/http://ygodm.tonsite.biz/snesadv/snesadv_gamelist.html)
#### Snezziboy
- L+R+Start for the emulator menu
- L+R+Select+Up to cycle BG Priority Sets
- L+R+Select+Down to cycle Forced BG Modes
- [Wiki page](https://web.archive.org/web/20090503124323/http://wiki.pocketheaven.com/Snezziboy)
- [Compatibility list](https://web.archive.org/web/20090508192702/http://wiki.pocketheaven.com/Snezziboy_Compatibility_List)
#### HVCA:
- A .cfg filename must match the filename of the game it targets
- Hold L+R in the menu to exit back to the flashcart menu
- This requires the ```-x``` builder option to add a .sub file containing exit code for specific flashcart models. My own [hacked flash_ez4_ezo.sub](https://gbatemp.net/threads/multi-platform-builder-scripts-for-gba-emulators.611219/post-10138443) for EZ-Flash IV / 3in1 / Omega is included in this repo.
#### ZXAdvance:
- ZXA.INI has a \[section\] for each game filename (lower case without file extension), the 'filename=' key is in fact how the game title will be displayed in the ZXAdvance ROM list. 'Config' can be Custom, or can refer to one of the sections prefixed with 'Config_' at the top of the file - e.g. Config=Kempston
