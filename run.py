import sys
import glob
import subprocess
import argparse
import os

""" Usage: python ./run.py [type] [input dir] [output dir]"""

parser = argparse.ArgumentParser(description='Make awesome graphs')

parser.add_argument('--type', default="accumulation", choices=["development", "accumulation"], help="type of visualization")
parser.add_argument('--cap', default="0", help="exclude function calls below this threshold (microseconds)")
parser.add_argument('--i', default=".", help="input directory containing the cachegrind files")
parser.add_argument('--o', default=".", help="output directory to generate the diagram into")

args = parser.parse_args()

if args.o == ".":
	args.o = args.i

if not os.path.exists(args.o):
	os.makedirs(args.o)

print "### CONVERTING ###"

subprocess.call(["python", "./conversion/k-to-csv.py", "--i", args.i, "--cap", args.cap])

print "### VISUALIZATION ###"

all_files = glob.glob(args.i + "/cachegrind.*.csv")
set_files = set([])

for filename in all_files:
	set_files.add('.'.join(filename.split('.')[:-2]))

for filename in set_files:
	#print filename + '.*.csv'
	#print ["Rscript", "./visualization/" + args.type + ".r", args.o, filename] + glob.glob(args.i + '/' + filename + '.*.csv')
	subprocess.call(["Rscript", "./visualization/" + args.type + ".r", args.o, filename] + glob.glob(filename + '.*.csv'))