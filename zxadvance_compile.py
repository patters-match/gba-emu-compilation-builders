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
#  unsigned char romtype      # 0=SNA, 1=Z80
#  unsigned char              # unused?
#  unsigned char controls[10] # A,B,Select,Start,Right,Left,Up,Down,R,L

# same ordering as ZX Spectrum keyboard polling http://www.breakintoprogram.co.uk/hardware/computers/zx-spectrum/keyboard
control_map = {
    'JOY FIRE':45,   'JOY UP':44, 'JOY DOWN':43, 'JOY LEFT':42, 'JOY RIGHT':41,
       'SHIFT':40,        'Z':39,        'X':38,        'C':37,         'V':36,
           'A':35,        'S':34,        'D':33,        'F':32,         'G':31,
           'Q':30,        'W':29,        'E':28,        'R':27,         'T':26,
           '1':25,        '2':24,        '3':23,        '4':22,         '5':21,
           '0':20,        '9':19,        '8':18,        '7':17,         '6':16,
           'P':15,        'O':14,        'I':13,        'U':12,         'Y':11,
       'ENTER':10,        'L': 9,        'K': 8,        'J': 7,         'H': 6,
       'SPACE': 5,'SYM SHIFT': 4,        'M': 3,        'N': 2,         'B': 1, '<unassigned>':0
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
        emubin[780] = 0 # patch to disable intro (already 0 in v1.0.1a)
        writefile(default_emubinary, emubin)
        print("...wrote", default_emubinary) 
        quit()

    roms = bytearray()
    headers = bytearray()
    # there is one blank header between the last header and the first ROM data
    headers_size = (len(args.romfile) + 1 ) * EMU_HEADER
    offset = headers_size

    for item in args.romfile:
        romname = os.path.split(item.name)[1]
        romfilename = os.path.splitext(romname)[0]
        romfileext = os.path.splitext(romname)[1]

        if romfileext.lower() == ".sna":
            romtype = 0
        elif romfileext.lower() == ".z80":
            romtype = 1
        else:
            print("Error: unsupported filetype for compilation -", romfilename)
            sys.exit(1)

        keys = default_controls
        controlscheme = ""

        if os.path.exists(args.inifile):
            # read controls mappings from ZXA.INI, if present
            config = configparser.ConfigParser()
            config.read(args.inifile)
            if romfilename in config:
                gameconfig = config[romfilename]
                controlscheme = gameconfig['control']
                if controlscheme == 'Custom':
                    keys = dict(gameconfig)
                else:
                    schemesectionname = 'Control_' + controlscheme
                    schemeconfig = config[schemesectionname]
                    keys = dict(schemeconfig)

        rom = item.read()
        rom += b"\0" * ((4 - (len(rom)%4))%4) # 4 byte alignment
        name = romfilename[:15].ljust(15)

        fileheader = struct.pack(
            header_struct_format, name.encode('ascii'), offset, romtype,
            control_map[keys['button a']], control_map[keys['button b']], control_map[keys['select']], control_map[keys['start']],
            control_map[keys['dpad right']], control_map[keys['dpad left']], control_map[keys['dpad up']], control_map[keys['dpad down']],
            control_map[keys['back right']], control_map[keys['back left']]
        )

        headers += fileheader
        roms += rom
        offset += len(rom)
        print('{:<16}{:<4}{}'.format(name,romfileext.strip('.').lower(),controlscheme))

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
