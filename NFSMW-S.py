import sys
import os
import hashlib

print("Need for Speed: Most Wanted SaveFile Editor v1.0.0")
print("by Mian_Bilawal aka Dragneel")
print()
if (len(sys.argv) > 3 or (len(sys.argv) < 2)):
	print("Usage:")
	print("{} SaveFile [Argument]".format(sys.argv[0]))
	print()
	print("Argument:")
	print("-b: BackUp the original File")
	sys.exit(1)
	
inptr = open(sys.argv[1], "rb+")
bMAGIC = inptr.read(4)
MAGIC = int.from_bytes(bMAGIC, byteorder="little")
if (MAGIC != 0x4D433032):
	print("Not a Need for Speed: Most Wanted file...")
	sys.exit(2)
inptr.seek(0)

bFile = 0
if ((len(sys.argv) == 3) and (sys.argv[2] == "-b")):
	print("Making backup of the original File... ", end="")
	outptr = open(sys.argv[1] + ".bak", "wb")
	for line in inptr:
		outptr.write(line)
	outptr.close()
	print("Done!")

print("Account Info:")
inptr.seek(0x5A31)
bName = inptr.read(8)
Name = (bName).decode("utf-8")
print("Name: {}".format(Name))
inptr.seek(0x4039)
bOMoney = inptr.read(4)
OMoney = int.from_bytes(bOMoney, byteorder="little")
print("Money: {}".format(OMoney))

inptr.seek(0x4039)
bMoney = input("Modified Money: ")
print("Writing modified money... ", end="")
Money = int(bMoney)
if (Money > ((1 << 31) - 1)):
	Money = ((1 << 31) - 1)
inptr.write((Money).to_bytes(4, byteorder="little", signed=False))
print("Done!")

print("Calculating newer hash... ", end="")
inptr.seek(0x34)
HASH = int(hashlib.md5(inptr.read(0xF828)).hexdigest(), 16)
print("Done!")

print("Changing hash in the file's content... ", end="")
inptr.seek(0xF85C)
inptr.write((HASH).to_bytes(16, byteorder="big", signed=False))
print("Done!")
inptr.close()