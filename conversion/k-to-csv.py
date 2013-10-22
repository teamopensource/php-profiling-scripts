import sys
import glob
import argparse
import re
import os

parser = argparse.ArgumentParser(description='Convert cachegrind to csv')

parser.add_argument('--cap', default="0", type=int, help="exclude function calls below this threshold (microseconds)")
parser.add_argument("--i", default=".", help="directory containing cachegrind files")
parser.add_argument("--o", default=".", help="directory to generate csv files to")

args = parser.parse_args()

if args.o == ".":
	args.o = args.i

if not os.path.exists(args.o):
	os.makedirs(args.o)

files = glob.glob("/".join([args.i, "cachegrind.*"]))

for filename in files:
	if ".csv" not in filename:
		inname = filename
		outname = "/".join([args.o, inname.split("/").pop() + '.csv'])

		def append (outfile, fl, fn, li, tm):
			if int(tm) >= args.cap: # only save the call, if it has taken more than args.cap microseconds
				outfile.write(",".join([fl, fn, li, tm]) + "\n")

		with open(inname, 'r') as infile, open(outname, 'w') as outfile:
			print "converting", inname, "-->", outname

			fl = ""
			fn = ""
			li = ""
			tm = ""

			for line in infile:
				numbers = re.match(r"([0-9]+)\ ([0-9]+)", line) # find linenumber and microseconds, like this: 26 26

				if numbers:
					li = numbers.group(1)
					tm = numbers.group(2)

				elif line.startswith("fl") or line.startswith("cfl"):
					# save the old one, if it exists

					if fl and fn and li and tm:
						append(outfile, fl, fn, li, tm)

					fl = line.replace("\n", '').split('=')[1] # get the function name

				elif line.startswith("fn") or line.startswith("cfn"):
					fn = line.replace("\n", '').split('=')[1] # get the function name


			if fl and fn and li and tm:
				append(outfile, fl, fn, li, tm)

