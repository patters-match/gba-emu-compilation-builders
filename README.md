# GBA Emulator Compilation Build Scripts

The emulators written for the Gameboy Advance were technically astounding considering the limited specifications of the host platform. In roughly chronological order, some of the best were:
- PocketNES for Nintendo NES (by Loopy, Jan 2001?)
- PCEAdvance for PC Engine (by FluBBa, Apr 2003)
- Goomba for the original Gameboy (by FluBBa, Oct 2003)
- SMSAdvance for SEGA Game Gear, Master System, SG-1000 (by FluBBa, Jul 2005)
- Cologne for ColecoVision (by FluBBa, Jan 2006)
- MSXAdvance for MSX-1 (by FluBBa, Mar 2006)
- NGPAdvance for Neo Geo Pocket/NGP Color (by Flubba, Jul 2008)

Each of these emulators had builder applications to combine the emulator binary with the ROMs and their required headers, however these were invariably Windows 32bit applications.

To try these emulators today is tricky if you are a macOS or Linux user, so I decided to write these Python3 builder scripts which mostly achieve feature parity with the old Win32 binaries.

Though on many operating systems Python scripts don't support drag and drop operations, you can drag and drop multiple file selections onto the shell window in which you are preparing the command line, which makes these scripts nicely usable for building large compilations.
