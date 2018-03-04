from copy import deepcopy
from json import load
from os import path

from model.abstract_syntax_tree import ASTree
from model.criteria import TA, TD, kTC, iTB, TDef, TU, TC


def check_criterias(criterias, control_flow_graph, test_sets_path):
    with open(test_sets_path, 'r') as test_sets_file:
        test_sets = load(test_sets_file)

    print('Comparasion between criteria \'{}\' and \'{}\' for program {} with test_sets {}'.format(
        criterias[0].__repr__(),
        criterias[1].__repr__(),
        control_flow_graph.name,
        test_sets
    ))

    for criteria in criterias:
        criteria.check(control_flow_graph, deepcopy(test_sets))
        print(criteria, '\n')


if __name__ == "__main__":
    pgcd = ASTree(path.join('Examples', 'pgcd.txt')).to_control_flow_graph()
    pgcd_test_sets_1 = path.join('Examples', 'pgcd_test_sets_1.json')
    pgcd_test_sets_2 = path.join('Examples', 'pgcd_test_sets_2.json')
    pgcd_test_sets_3 = path.join('Examples', 'pgcd_test_sets_3.json')
    pgcd_test_sets_4 = path.join('Examples', 'pgcd_test_sets_4.json')
    pgcd_test_sets_5 = path.join('Examples', 'pgcd_test_sets_5.json')

    check_criterias([TA(), TD()], pgcd, pgcd_test_sets_1)
    check_criterias([TA(), TD()], pgcd, pgcd_test_sets_2)

    check_criterias([TD(), kTC(2)], pgcd, pgcd_test_sets_3)
    check_criterias([TD(), kTC(5)], pgcd, pgcd_test_sets_4)

    check_criterias([kTC(5), iTB(1)], pgcd, pgcd_test_sets_4)
    check_criterias([kTC(2), iTB(1)], pgcd, pgcd_test_sets_3)
    check_criterias([kTC(8), iTB(1)], pgcd, pgcd_test_sets_4)

    check_criterias([TDef(), TA()], pgcd, pgcd_test_sets_2)

    check_criterias([TU(), TA()], pgcd, pgcd_test_sets_2)
    check_criterias([TU(), TA()], pgcd, pgcd_test_sets_5)

    check_criterias([TD(), TC()], pgcd, pgcd_test_sets_1)
    check_criterias([TD(), TC()], pgcd, pgcd_test_sets_2)
