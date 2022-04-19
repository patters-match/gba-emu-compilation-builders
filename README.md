# GBA Emulator Compilation Build Scripts

Modern Python3 builder scripts to replace the original Windows 32bit applications bundled with the following Gameboy Advance emulators, in order of initial release date:
- [PocketNES](https://github.com/Dwedit/PocketNES/releases) for Nintendo NES (by Loopy, Jan 2001?)
- [PCEAdvance](https://web.archive.org/web/20150430211123/http://www.ndsretro.com/gbadown.html) for PC Engine (by FluBBa, Apr 2003)
- [Goomba](http://goomba.webpersona.com) for the original Gameboy (by FluBBa, Oct 2003)
- [SMSAdvance](https://web.archive.org/web/20150430211123/http://www.ndsretro.com/gbadown.html) for SEGA Game Gear, Master System, SG-1000 (by FluBBa, Jul 2005)
- [Cologne](https://web.archive.org/web/20150430211123/http://www.ndsretro.com/gbadown.html) for ColecoVision (by FluBBa, Jan 2006)
- [Goomba Color](https://www.dwedit.org/gba/goombacolor.php) a Goomba fork to add Gameboy Color (by Dwedit, Jan 2006)
- [MSXAdvance](https://web.archive.org/web/20150430211123/http://www.ndsretro.com/gbadown.html) for MSX-1 (by FluBBa, Mar 2006)
- [NGPAdvance](https://web.archive.org/web/20150430211123/http://www.ndsretro.com/gbadown.html) for Neo Geo Pocket / NGP Color (by Flubba, Jul 2008)
- [Jagoomba](https://github.com/EvilJagaGenius/jagoombacolor/releases) enhanced Goomba Color fork for Gameboy / Gameboy Color (by Jaga, Nov 2021)

The scripts combine the emulator binary with the game ROMs and their required metadata into a .gba ROM for Gameboy Advance. Although on many operating systems Python scripts don't support drag and drop operations, you can drag and drop multiple file selections onto the shell window in which you are preparing the command line. This makes these scripts nicely usable for building large compilations.

Each script has help information accessible via the -h command line option. For example:
```
usage: smsadvance_compile.py [-h] [-s SPLASHSCREEN] [-b BIOS [BIOS ...]] [-bb] [-e EMUBINARY] [-m] [-o OUTPUTFILE] [-ez4v1] [-ez4v2]
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
  -o OUTPUTFILE       Compilation output filename, defaults to smsadv-compilation.gba
  -ez4v1              For EZ-Flash IV firmware 1.x. Create a blank 64KB .sav file for the compilation, needed for the SAVER folder. Not
                      needed for firmware 2.x which creates its own blank saves
  -ez4v2              For EZ-Flash IV firmware 2.x. Create a .pat file for the compilation to force 64KB SRAM saves, store in the PATCH
                      folder

coded by patters in 2022
```
