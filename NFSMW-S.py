import sys
import hashlib

print("Need for Speed: Most Wanted SaveFile Editor v1.1.0")
print("by Dragneel1234")
print()

'''
Checking the arguments
'''
if (len(sys.argv) > 3 or (len(sys.argv) < 2)):
	print("Usage:")
	print("{} SaveFile [Argument]".format(sys.argv[0]))
	print()
	print("Argument:")
	print("-b: BackUp the original File")
	sys.exit(1)
	
'''
Open the File and
Check if it is valid i.e. 20CM
'''
inptr = open(sys.argv[1], "rb+")
bMAGIC = inptr.read(4)
MAGIC = int.from_bytes(bMAGIC, byteorder="little")
if (MAGIC != 0x4D433032):
	print("Not a Need for Speed: Most Wanted file...")
	sys.exit(2)
inptr.seek(0)

'''
Check for backup paremeter then make a backup
'''
if ((len(sys.argv) == 3) and (sys.argv[2] == "-b")):
	print("Making backup of the original File... ", end="")
	outptr = open(sys.argv[1] + ".bak", "wb")
	for line in inptr:
		outptr.write(line)
	outptr.close()
	print("Done!")

'''
Getting Safe File Info
'''
print()
print("Account Info:")
inptr.seek(0x5A31)
bName = inptr.read(8)
Name = (bName).decode("utf-8")
print("Name: {}".format(Name))
inptr.seek(0x4039)
bOMoney = inptr.read(4)
OMoney = int.from_bytes(bOMoney, byteorder="little")
print("Money: {}".format(OMoney))

'''
This loop works like that
At 0xE2ED, first car is found
If it is sold then its ID is FF else it starts from 00 upward
Bounty of that car is found 0xF after ID
Next Car is found 0x37 from ID
'''
inptr.seek(0xE2ED)
while(1):
	bCar = inptr.read(1)
	Car = int.from_bytes(bCar, byteorder="little")
	if (Car == 0xFF):
		inptr.seek(0x37, 1)
		continue
	else:
		break
inptr.seek(0xF, 1)
bOBounty = inptr.read(4)
OBounty = int.from_bytes(bOBounty, byteorder="little")
print("Bounty(1st Car only): {}".format(OBounty))
print()

'''
Change the money specified by user
Giving 0 will not change the money to 0 but it will keep the current money
-1 will do that (negative one)
'''
inptr.seek(0x4039)
bMoney = input("Modified Money: ")
print("Writing modified money... ", end="")
Money = int(bMoney)
if (Money > ((1 << 31) - 1)):
	Money = ((1 << 31) - 1)
if (Money == 0):
	Money = OMoney
elif (Money == -1):
	Money = 0
inptr.write((Money).to_bytes(4, byteorder="little", signed=False))
print("Done!")

'''
Change the bounty of the first car
Giving 0 will not change the bounty to 0 but it will keep the current bounty
-1 will do that (negative one)
'''
inptr.seek(0xE2ED)
while(1):
	bCar = inptr.read(1)
	Car = int.from_bytes(bCar, byteorder="little")
	if (Car == 0xFF):
		inptr.seek(0x37, 1)
		continue
	else:
		break
inptr.seek(0xF, 1)
bBounty = input("Modified Bounty: ")
print("Writing modified bounty... ", end="")
Bounty = int(bBounty)
if (Bounty > ((1 << 31) - 1)):
	Bounty = ((1 << 31) - 1)
if (Bounty == 0):
	Bounty = OBounty
elif (Bounty == -1):
	Bounty = 0
inptr.write((Bounty).to_bytes(4, byteorder="little", signed=False))
print("Done!")

'''
EA used md5 of the portion
0x34 to F8FC for checking the validity of the savefile
Calculating the modified md5
'''
print("Calculating newer hash... ", end="")
inptr.seek(0x34)
HASH = int(hashlib.md5(inptr.read(0xF828)).hexdigest(), 16)
print("Done!")

'''
Storing the new md5 at the end
'''
print("Changing hash in the file's content... ", end="")
inptr.seek(0xF85C)
inptr.write((HASH).to_bytes(16, byteorder="big", signed=False))
print("Done!")
inptr.close()
