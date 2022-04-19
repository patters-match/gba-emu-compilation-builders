#!/usr/bin/python3

import sys, os.path, struct, argparse

EMUID = int(0x1A53454E) # "NES",0x1A - probably unintentional
SRAM_SAVE = 8192

default_outputfile = "pceadv-compilation.gba"
default_emubinary = "pceadvance.gba"
default_cdrombios = "bios.bin"
header_struct_format = "<31sc5I12s" # https://docs.python.org/3/library/struct.html

# ROM header
#
# from gba.h in the PCEAdvance source code, flags deduced by testing with the Win32 builder
# 
#typedef struct {
#	char name[32] null terminated;
#	u32 filesize;
#	u32 flags;
#		Bit 0: 0=Full CPU, 1=50% CPU throttle (1 in decimal)
#		Bit 1: 0=CPU Speedhacks enabled, 1=Disable CPU Speedhacks (2 in decimal)
#		Bit 2: 0=JP rom, 1=USA rom (4 in decimal)
#		Bit 5: 0=spritefollow, 1=addressfollow (32 in decimal)
#	u32 address/sprite to follow;
#	u32 identifier;
#	char unknown[12];
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
		description="This script will assemble the PCEAdvance emulator, PC Engine/Turbografx-16 .pce ROM images, and .iso CD-ROM data tracks into a Gameboy Advance ROM image. It is recommended to type the script name, then drag and drop multiple ROM files onto the shell window, then add any additional arguments as needed.",
		epilog="coded by patters in 2022"
	)

	parser.add_argument(
		dest = 'romfile',
		help = ".pce or .iso image to add to compilation. Drag and drop multiple files onto your shell window. Note that PCEAdvance supports only one CD-ROM game per compilation.",
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
		'-b',
		dest = 'cdrombios',
		help = "CD-ROM / Super CD-ROM BIOS rom image, defaults to " + default_cdrombios,
		type = argparse.FileType('rb'),
	)
	parser.add_argument(
		'-e',
		dest = 'emubinary',
		help = "PCEAdvance binary, defaults to " + default_emubinary,
		type = argparse.FileType('rb'),
		default = default_emubinary
	)
	parser.add_argument(
		'-t',
		dest = 'tcdfile',
		help = "CD-ROM track index file, needed for games with multiple data tracks, defaults to <iso_name>.tcd",
		type = argparse.FileType('rb'),
	)
	# don't use FileType('wb') here because it writes a zero-byte file even if it doesn't parse the arguments correctly
	parser.add_argument(
		'-o',
		dest = 'outputfile',
		help = "Compilation output filename, defaults to " + default_outputfile,
		type = str,
		default = default_outputfile
	)
	parser.add_argument(
		'-ez4v1',
		help = "For EZ-Flash IV firmware 1.x. Create a blank 8KB .sav file for the compilation, needed for the SAVER folder. Not needed for firmware 2.x which creates its own blank saves",
		action = 'store_true'
	)
#   not needed for PCEAdvance since it uses 8KB SRAM saves
#	parser.add_argument(
#		'-ez4v2',
#		help = "For EZ-Flash IV firmware 2.x. Create a .pat file for the compilation to force 64KB SRAM saves, store in the PATCH folder",
#		action = 'store_true'
#	)

	args = parser.parse_args()


	compilation = args.emubinary.read()

	if args.splashscreen:
		compilation = compilation + args.splashscreen.read()

	iso_count = 0

	for item in args.romfile:

		flags = 0
		follow = 0 # sprite or address follow for 'Unscaled (Auto)' display mode

		romfilename = os.path.split(item.name)[1]
		romtitle = os.path.splitext(romfilename)[0][:31]
		romtype = os.path.splitext(romfilename)[1]

		# HuCard
		if romtype.lower() == ".pce":
			rom = item.read()
			rom = rom + b"\0" * (len(rom)%4)

			# USA ROMs need this specific flag - remember, most will need to be decrypted first using PCEToy
			if "(U)" in romtitle or "(USA)" in romtitle:
				flags = set_bit (flags, 2)

			# sprite follow settings for display mode: Unscaled (Auto)
			if "1943" in romtitle:
				follow = 9
			if "aero blasters" in romtitle.lower():
				follow = 6
			if "atomic robokid special" in romtitle.lower():
				follow = 0
			if "devil crash" in romtitle.lower():
				follow = 11
			if "devil's crush" in romtitle.lower():
				follow = 11
			if "kyuukyoku tiger" in romtitle.lower():
				follow = 3
			if "legendary axe" in romtitle.lower():
				follow = 14
			if "raiden" in romtitle.lower():
				follow = 5

			# unsure why 16 bytes are added to len(rom), but the original builder does this, despite that it pads the roms a lot more than 16b
			# however, you can't add more than one rom to the compilation unless this is done
			romheader = struct.pack(header_struct_format, romtitle.encode('ascii'), b"\0", len(rom)+16, flags, follow, 0, EMUID, b"@           ")

			compilation = compilation + romheader + rom

		# CD-ROM
		elif romtype.lower() == ".iso":
			# only a single CD-ROM image is supported per compilation
			if iso_count == 0:
				# first data track ISO needs a CD-ROM BIOS + optional TCD tracklist first
				if args.cdrombios:
					cdbios = args.cdrombios.read()
				else:
					cdbios = readfile(default_cdrombios)

				cdbios = cdbios + b"\0" * (len(cdbios)%4)

				# use the ISO name for the cdbios entry in the rom list
				cdromheader = struct.pack(header_struct_format, romtitle.encode('ascii'), b"\0", len(cdbios)+16, flags, follow, 0, EMUID, b"@           ")
				compilation = compilation + cdromheader + cdbios

				if args.tcdfile:
					tracklist = args.tcdfile.read()
				elif os.path.exists(romtitle + ".tcd"):
					tracklist = readfile(romtitle + ".tcd")
				else:
					tracklist = b""

				cdrom = tracklist

			# append data track (any subsequent tracks are simply concatenated - a TCD file is required for multiple data tracks)
			cdrom = cdrom + item.read()
			iso_count = iso_count + 1
			if iso_count == 2 and tracklist == b"":
				print("Error: multiple ISO data tracks require a TCD tracklist, either named to match the first ISO, or defined via -t")
				print("       Note that PCEAdvance supports only a single CD-ROM game per compilation")
				sys.exit(1)

		else:
			print("Error: unsupported filetype for compilation -", romfilename)
			sys.exit(1)

		print (romfilename)

	#finished iterating rom list, append any CD-ROM data
	if iso_count:
		compilation = compilation + cdrom

	writefile(args.outputfile, compilation)

#   not needed for PCEAdvance since it uses 8KB SRAM saves
#	if args.ez4v2:
#		# EZ-Flash IV fw2.x GSS patcher metadata to force 64KB SRAM saves - for PATCH folder on SD card
#		patchname = os.path.splitext(args.outputfile)[0] + ".pat"
#		patchdata = b'QlpoOTFBWSZTWRbvmZEAAAT44fyAgIAAEUAAAACIAAQAAAQESaAAVEIaaGRoxBKeqQD1GTJoks40324rSIskHSFhIywXzTCaqwSzf4exCBTgBk/i7kinChIC3fMyIA=='
#		writefile(patchname, bz2.decompress(base64.b64decode(patchdata)))

	if args.ez4v1:
		# EZ-Flash IV fw1.x blank save - for SAVER folder on SD card
		savename = os.path.splitext(args.outputfile)[0] + ".sav"
		saveempty = b"\xff" * SRAM_SAVE
		if not os.path.exists(savename): # careful not to overwrite an existing save
			writefile(savename, saveempty)
