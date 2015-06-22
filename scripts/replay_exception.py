#!/usr/bin/env python
"""
Loads a saved evaluation exception and replays the error
"""

import argparse
import cPickle as pkl
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('exception_file',
                    help="The path of the saved evaluation exception file"
                         " ('evaluation_exception.pkl')")
args = parser.parse_args()

import sys
sys.path.append('/home/tclose/git/purkinje/tuning')

with open(args.exception_file, 'rb') as f:
    (objective, simulation, candidate,
     analysis, error_type, error_message) = pkl.load(f)

print "Replaying evaluation exception for {}:".format(candidate)
print "It threw '{}': {}".format(error_type, error_message)

if analysis is None:
    simulation.run_all(candidate)
else:
    print "fitness: {}".format(objective.fitness(analysis))
