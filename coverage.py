"""
This file will be the cli for using our code.

Usage:
    coverage.py check-criteria <source_filepath> <testsets_filepath>
"""
from copy import deepcopy
from docopt import docopt
from json import load

from model.abstract_syntax_tree import ASTree
from model.criteria import TA, TD, kTC


if __name__ == '__main__':
    args = docopt(__doc__, version='The CCM Project 0.1')
    criterias = [TA(), TD(), kTC(2)]

    if args['check-criteria']:
        graph = ASTree(args['<source_filepath>']).to_control_flow_graph()
        with open(args['<testsets_filepath>'], 'r') as test_sets_file:
            test_sets = load(test_sets_file)

        for criteria in criterias:
            print(criteria, " : ", criteria.check(graph, deepcopy(test_sets)))
