from copy import deepcopy
from model.abstract_syntax_tree import ASTree
from model.criteria import TA, TD, kTC, TC

if __name__ == "__main__":

    # load the programm into an ASTree
    # get the initial values of the variables

    tree = ASTree('Examples/pgcd.txt')
    test_sets = [
        {'X': 1, 'Y': 1},
        {'X': 15, 'Y': 5},
    ]
    CG = tree.to_control_flow_graph()

    criterias = [TA(), TD(), kTC(5), TC()]
    for criteria in criterias:
        criteria.check(CG, deepcopy(test_sets))
        print('\n', criteria)
