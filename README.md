# GBA Emulator Compilation Build Scripts

Modern Python3 builder scripts to replace the original Windows 32bit applications bundled with the following Gameboy Advance emulators:
- [PocketNES](https://github.com/Dwedit/PocketNES/releases) for Nintendo NES (by Loopy, Jan 2001?)
- [PCEAdvance](https://web.archive.org/web/20150430211123/http://www.ndsretro.com/gbadown.html) for PC Engine (by FluBBa, Apr 2003)
- [Goomba](http://goomba.webpersona.com) for the original Gameboy (by FluBBa, Oct 2003)
- [SMSAdvance](https://web.archive.org/web/20150430211123/http://www.ndsretro.com/gbadown.html) for SEGA Game Gear, Master System, SG-1000 (by FluBBa, Jul 2005)
- [Cologne](https://web.archive.org/web/20150430211123/http://www.ndsretro.com/gbadown.html) for ColecoVision (by FluBBa, Jan 2006)
- [Goomba Color](https://www.dwedit.org/gba/goombacolor.php) a Goomba fork to add Gameboy Color (by Dwedit, Jan 2006)
- [MSXAdvance](https://web.archive.org/web/20150430211123/http://www.ndsretro.com/gbadown.html) for MSX-1 (by FluBBa, Mar 2006)
- [NGPAdvance](https://web.archive.org/web/20150430211123/http://www.ndsretro.com/gbadown.html) for Neo Geo Pocket / NGP Color (by Flubba, Jul 2008)
- [Jagoomba](https://github.com/EvilJagaGenius/jagoombacolor/releases) the latest enhanced Goomba Color fork for Gameboy / Gameboy Color (by Jaga, Nov 2021)

The scripts combine the emulator binary with the game ROMs and their required metadata into a .gba ROM for Gameboy Advance. Although on many operating systems Python scripts don't support drag and drop operations, you can drag and drop multiple file selections onto the shell window in which you are preparing the command line. This makes these scripts nicely usable for building large compilations.

Each script has help information accessible via the -h command line option.
