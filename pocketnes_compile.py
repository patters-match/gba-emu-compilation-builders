#!/usr/bin/python3

import sys, os.path, struct, argparse, bz2, base64

SRAM_SAVE = 65536

default_outputfile = "pocketnes-compilation.gba"
default_emubinary = "pocketnes.gba"
header_struct_format = "<31sc4I" # https://docs.python.org/3/library/struct.html

# ROM header
#
# from gba.h in the PocketNES source code and FORMATS.txt in the binary distribution, and testing with the Win32 builder
#
#typedef struct {
#	char name[32] null terminated;
#	u32 filesize;
#	u32 flags;
#		Bit 0: 1=Enable PPU speed hack (1 in decimal);
#		Bit 1: 1=Disable CPU Speedhacks (2 in decimal);
#		Bit 2: 1=Use PAL timing (4 in decimal);
#		Bit 5: 0=spritefollow, 1=addressfollow (32 in decimal);
#	u32 address/sprite to follow;
#	u32 reserved;
#} romheader;

def readfile(name):
	try:
		fd = open(name, "rb")
		contents = fd.read()
		fd.close()
	except IOError:
		print("Error reading", name)
		sys.exit(1)
	return contents

def writefile(name, contents):
	try:
		fd = open(name, "wb")
		fd.write(contents)
		fd.close()
	except IOError:
		print("Error writing", name)
		sys.exit(1)
	else:
		if name == default_outputfile:
			print("...wrote", name)


#def get_bit(value, n):
#    return ((value >> n & 1) != 0)

def set_bit(value, n):
    return value | (1 << n)

#def clear_bit(value, n):
#    return value & ~(1 << n)


if __name__ == "__main__":
	parser = argparse.ArgumentParser(
		description="This script will assemble the PocketNES emulator and NES ROMs into a Gameboy Advance ROM image. It is recommended to type the script name, then drag and drop multiple ROM files onto the shell window, then add any additional arguments as needed.",
		epilog="coded by patters in 2022"
	)

	parser.add_argument(
		dest = 'romfile',
		help = ".nes image to add to compilation. Drag and drop multiple files onto your shell window.",
		type = argparse.FileType('rb'),
		nargs = '+'
	)
	parser.add_argument(
		'-s',
		dest = 'splashscreen',
		help = "76800 byte raw 240x160 15bit splashscreen image",
		type = argparse.FileType('rb')
	)
	parser.add_argument(
		'-e', 
		dest = 'emubinary',
		help = "PocketNES binary, defaults to " + default_emubinary,
		type = argparse.FileType('rb'),
		default = default_emubinary
	)
	parser.add_argument(
		'-m',
		help = "mark small ROMs suitable for link transfer",
		action = 'store_true'
	)	

	# don't use FileType('wb') here because it writes a zero-byte file even if it doesn't parse the arguments correctly
	parser.add_argument(
		'-o',
		dest = 'outputfile',
		help = "compilation output filename, defaults to " + default_outputfile,
		type = str,
		default = default_outputfile
	)
	parser.add_argument(
		'-sav',
		help = "for EZ-Flash IV firmware 1.x - create a blank 64KB .sav file for the compilation, store in the SAVER folder, not needed for firmware 2.x which creates its own blank saves",
		action = 'store_true'
	)
	parser.add_argument(
		'-pat',
		help = "for EZ-Flash IV firmware 2.x - create a .pat file for the compilation to force 64KB SRAM saves, store in the PATCH folder",
		action = 'store_true'
	)
	args = parser.parse_args()


	compilation = args.emubinary.read()

	if args.splashscreen:
		compilation = compilation + args.splashscreen.read()

	for item in args.romfile:

		flags = 0
		follow = 0 # sprite or address follow for Unscaled (Auto) display mode

		romfilename = os.path.split(item.name)[1]
		romtype = os.path.splitext(romfilename)[1]
		if args.m:
			print(os.path.getsize(item.name))
			if os.path.getsize(item.name) <= 196608:
				romtitle = "* " + os.path.splitext(romfilename)[0][:29]
			else:
				romtitle = "  " + os.path.splitext(romfilename)[0][:29]
		else:
			romtitle = os.path.splitext(romfilename)[0][:31]

		if romtype.lower() == ".nes":

			if "(E)" in romtitle or "(Europe)" in romtitle or "(EUR)" in romtitle:
				flags = set_bit (flags, 2) # set PAL timing for EUR-only titles

		else:
			print("Error: unsupported filetype for compilation -", romfilename)
			sys.exit(1)

		rom = item.read()
		rom = rom + b"\0" * (len(rom)%4)
		romheader = struct.pack(header_struct_format, romtitle.encode('ascii'), b"\0", len(rom), flags, follow, 0)
		compilation = compilation + romheader + rom

		print (romfilename)

	writefile(args.outputfile, compilation)

	if args.pat:
		# EZ-Flash IV fw2.x GSS patcher metadata to force 64KB SRAM saves - for PATCH folder on SD card
		patchname = os.path.splitext(args.outputfile)[0] + ".pat"
		patchdata = b'QlpoOTFBWSZTWRbvmZEAAAT44fyAgIAAEUAAAACIAAQAAAQESaAAVEIaaGRoxBKeqQD1GTJoks40324rSIskHSFhIywXzTCaqwSzf4exCBTgBk/i7kinChIC3fMyIA=='
		writefile(patchname, bz2.decompress(base64.b64decode(patchdata)))

	if args.sav:
		# EZ-Flash IV fw1.x blank save - for SAVER folder on SD card
		savename = os.path.splitext(args.outputfile)[0] + ".sav"
		saveempty = b"\xff" * SRAM_SAVE
		if not os.path.exists(savename): # careful not to overwrite an existing save
			writefile(savename, saveempty)
