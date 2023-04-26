# HVCA exit code for EZ-Flash IV / 3in1 / Omega
# by patters in 2023
# 
# https://gbatemp.net/threads/multi-platform-builder-scripts-for-gba-emulators.611219/post-10138443

add   sb, pc, #0x48          @ sb = start of .BYTE definitions
ldm   sb, {r1, r2, r3, r4}
mov   r5, #0xd200
mov   r6, #0x1500
strh  r5, [r1]               @ 0x9fe0000 = 0xd200
strh  r6, [r2]               @ 0x8000000 = 0x1500
strh  r5, [r3]               @ 0x8020000 = 0xd200
strh  r6, [r4]               @ 0x8040000 = 0x1500
mov   r0, #0x8000
ldr   r1, [pc, #0x34]        @ 5th .BYTE
strh  r0, [r1]               @ 0x9880000 = 0x8000
mov   r0, #0x1500
ldr   r1, [pc, #0x2c]        @ 6th .BYTE
strh  r0, [r1]               @ 0x9fc0000 = 0x1500
mov   r0, #0
mov   r1, #0x4000000         @ 0x9fc0000 = 0x1500
strh  r0, [r1, #-6]          @ 0x3fffffa = 0x0000
mov   r0, #0xfc
svc   #0x10000
svc   #0
.BYTE 0x00, 0x00, 0xfe, 0x09
.BYTE 0x00, 0x00, 0x00, 0x08
.BYTE 0x00, 0x00, 0x02, 0x08
.BYTE 0x00, 0x00, 0x04, 0x08
.BYTE 0x00, 0x00, 0x88, 0x09
.BYTE 0x00, 0x00, 0xfc, 0x09
