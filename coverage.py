"""
This file will be the cli for using our code.

Usage:
    coverage.py <source_filepath> <testsets_filepath> [--kTC=<k>] [--iTB=<i>]

Options:
    -h --help      Show this screen.
    -k --kTC=<k>   Length of k-path to check [default: 2].
    -i --iTB=<i>   Length of i-loop to check [default: 1].
"""
from copy import deepcopy
from docopt import docopt
from json import load

from model.abstract_syntax_tree import ASTree
from model.criteria import TA, TD, kTC, TC, iTB, TDef, TU


if __name__ == '__main__':
    args = docopt(__doc__, version='The CCM Project 0.1')
    criterias = [TA(), TD(), kTC(int(args['--kTC'])), iTB(int(args['--iTB'])), TDef(), TU(), TC()]

    graph = ASTree(args['<source_filepath>']).to_control_flow_graph()
    with open(args['<testsets_filepath>'], 'r') as test_sets_file:
        test_sets = load(test_sets_file)

    for criteria in criterias:
        criteria.check(graph, deepcopy(test_sets))
        print()
        print(criteria)
