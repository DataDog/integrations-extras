import re
import argparse

parser=argparse.ArgumentParser()

parser.add_argument('--files', help="A list of modified files")
args=parser.parse_args()

for file in args.files.split(" "):
    print(file)