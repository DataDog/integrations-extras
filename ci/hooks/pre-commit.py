#!/usr/bin/env python

import fnmatch
import os
import sys

OK = 0
ERR = 1

def get_files(fname):
    matches = []
    for root, dirnames, filenames in os.walk('.'):
        for filename in fnmatch.filter(filenames, fname):
            matches.append(os.path.join(root, filename))

    return matches


def process_requirements(reqs, fname):
    SPECIFIERS = ['==', '!=' '<=', '>=', '<', '>']

    print "processing... {}".format(fname)
    with open(fname) as f:
        content = f.readlines()

    for line in content:
        line = "".join(line.split())
        for specifier in SPECIFIERS:
            idx = line.find(specifier)
            if idx < 0:
                continue

            req = line[:idx]
            specifier = line[idx:]

            if req in reqs and reqs[req][0] != specifier:
                # version mismatch
                print "There's a version mismatch with {req} " \
                    " {spec} and {prev_spec} defined in {src}.".format(
                        req=req,
                        spec=specifier,
                        prev_spec=reqs[req][0],
                        src=reqs[req][1]
                    )
                sys.exit(ERR)
            elif req not in reqs:
                reqs[req] = (specifier, fname)
                break


requirements = {}
files = get_files('requirements.txt')

for f in files:
    process_requirements(requirements, f)

print "No requirement version conflicts found. Looking good... ;)"
for req, spec in requirements.iteritems():
    print "{req}{spec} first found in {fname}".format(
        req=req,
        spec=spec[0],
        fname=spec[1]
    )

sys.exit(OK)
