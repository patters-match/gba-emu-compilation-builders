#!/usr/bin/python3

import sys, os.path, struct, argparse, bz2, base64, configparser
from sys import argv

EMU_HEADER = 32
SRAM_SAVE = 65536

default_outputfile = "zxadv-compilation.gba"
default_emubinary = "zxa.gba"
default_inifile = "ZXA.INI"
original_binaries = [ "ZXAdvance 1.0.1.exe", "ZXAdvance 1.0.1a.exe" ]
header_struct_format = "<15sxIBx10B" # https://docs.python.org/3/library/struct.html

# ZXAdvance rom header (headers for all files are concatenated directly after the emulator binary)
# 
#  char name[16]              # null terminated
#  long offset                # from end of ZXAdvance binary
#  unsigned char filetype     # 0=SNA, 1=Z80
#  unsigned char              # unused?
#  unsigned char controls[10] # A,B,Select,Start,Right,Left,Up,Down,R,L

# same ordering as ZX Spectrum keyboard polling http://www.breakintoprogram.co.uk/hardware/computers/zx-spectrum/keyboard
control_map = {
	'JOY FIRE':0x2D,   'JOY UP':0x2C, 'JOY DOWN':0x2B, 'JOY LEFT':0x2A, 'JOY RIGHT':0x29,
	   'SHIFT':0x28,        'Z':0x27,        'X':0x26,        'C':0x25,         'V':0x24,
	       'A':0x23,        'S':0x22,        'D':0x21,        'F':0x20,         'G':0x1F,
	       'Q':0x1E,        'W':0x1D,        'E':0x1C,        'R':0x1B,         'T':0x1A,
	       '1':0x19,        '2':0x18,        '3':0x17,        '4':0x16,         '5':0x15,
	       '0':0x14,        '9':0x13,        '8':0x12,        '7':0x11,         '6':0x10,
	       'P':0x0F,        'O':0x0E,        'I':0x0D,        'U':0x0C,         'Y':0x0B,
	   'ENTER':0x0A,        'L':0x09,        'K':0x08,        'J':0x07,         'H':0x06,
	   'SPACE':0x05,'SYM SHIFT':0x04,        'M':0x03,        'N':0x02,         'B':0x01, '<unassigned>':0x0
}
default_controls = {
	 'back left':'S',
	'back right':'K',
	 'dpad left':'JOY LEFT',
	'dpad right':'JOY RIGHT',
	   'dpad up':'JOY UP',
	 'dpad down':'JOY DOWN',
	     'start':'0',
	    'select':'1',
	  'button a':'JOY FIRE',
	  'button b':'JOY FIRE'
}

def readfile(name):
	with open(name, "rb") as fh:
		contents = fh.read()
	return contents

def writefile(name, contents):
	with open(name, "wb") as fh:
		fh.write(contents)
		if name == default_outputfile:
			print("...wrote", name) 

#def get_bit(value, n):
#    return ((value >> n & 1) != 0)

#def set_bit(value, n):
#    return value | (1 << n)

#def clear_bit(value, n):
#    return value & ~(1 << n)


if __name__ == "__main__":

	if os.path.dirname(argv[0]) and os.path.dirname(argv[0]) != ".":
		localpath = os.path.dirname(argv[0]) + os.path.sep
	else:
		localpath = ""

	parser = argparse.ArgumentParser(
		description="This script will assemble the ZXAdvance emulator and Z80/SNA snapshots into a Gameboy Advance ROM image. It is recommended to type the script name, then drag and drop multiple ROM files onto the shell window, then add any additional arguments as needed.",
		epilog="coded by patters in 2023"
	)

	parser.add_argument(
		dest = 'romfile',
		help = ".z80/.sna files to add to the compilation. Drag and drop multiple files onto your shell window.",
		type = argparse.FileType('rb'),
		nargs = '*' # allow no romfile when extracting the emulator from the original .exe file 
	)
	parser.add_argument(
		'-e', 
		dest = 'emubinary',
		help = "ZXAdvance binary, defaults to " + localpath + default_emubinary + ". On first run, point this to the 'ZXAdvance 1.0.1.exe' injector tool to extract the emulator.",
		type = argparse.FileType('rb'),
		default = localpath + default_emubinary
	)
	parser.add_argument(
		'-i', 
		dest = 'inifile',
		help = "ZXAdvance INI file which stores control mappings, defaults to " + localpath + default_inifile,
		type = str,
		default = localpath + default_inifile
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

	emubinaryfilename = os.path.split(args.emubinary.name)[1]
	if emubinaryfilename in original_binaries:
		args.emubinary.seek(723716)
		emubin = bytearray(args.emubinary.read(146800))
		emubin[780] = 0 # patch to disable intro (already 0 in v1.0.1a, which is the only difference)
		writefile(default_emubinary, emubin)
		print("...wrote", default_emubinary) 
		quit()

	roms = bytes()
	headers = bytes()
	# there is one blank header between the last header and the first ROM data
	headers_size = (len(args.romfile) + 1 ) * EMU_HEADER
	offset = headers_size

	for item in args.romfile:
		romfilename = os.path.split(item.name)[1]
		romtitle = os.path.splitext(romfilename)[0]
		romtype = os.path.splitext(romfilename)[1]

		if romtype.lower() == ".sna":
			filetype = 0
		elif romtype.lower() == ".z80":
			filetype = 1
		else:
			raise Exception(f'unsupported filetype for compilation - {romfilename}')

		keys = default_controls
		controlscheme = ""

		if os.path.exists(args.inifile):
			# read controls mappings from ZXA.INI, if present
			config = configparser.ConfigParser()
			config.read(args.inifile)
			if romtitle in config:
				gameconfig = config[romtitle]
				controlscheme = gameconfig['control']
				if controlscheme == 'Custom':
					keys = dict(gameconfig)
				else:
					schemesectionname = 'Control_' + controlscheme
					schemeconfig = config[schemesectionname]
					keys = dict(schemeconfig)

		rom = item.read()
		rom += b"\0" * ((4 - (len(rom)%4))%4) # 4 byte alignment
		name = romtitle[:15].ljust(15)

		fileheader = struct.pack(
			header_struct_format, name.encode('ascii'), offset, filetype,
			control_map[keys['button a']], control_map[keys['button b']], control_map[keys['select']], control_map[keys['start']],
			control_map[keys['dpad right']], control_map[keys['dpad left']], control_map[keys['dpad up']], control_map[keys['dpad down']],
			control_map[keys['back right']], control_map[keys['back left']]
		)

		headers += fileheader
		roms += rom
		offset += len(rom)
		print('{:<16}{:<4}{}'.format(name,romtype.strip('.').lower(),controlscheme))

	blankheader = b'\0' * EMU_HEADER
	compilation = args.emubinary.read() + headers + blankheader + roms

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
