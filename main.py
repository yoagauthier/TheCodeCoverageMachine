from model.criteria import TA, TD, kTC, TC, TDef
from model.astree import ASTree

if __name__ == "__main__":

    # load the programm into an ASTree
    # get the initial values of the variables

    tree = ASTree('Examples/exemple.txt')
    test_sets = [{'X': 12}]
    CG = tree.to_cover_graph()

    criterias = [TA(), TD(), kTC(5), TC(), TDef()]
    for criteria in criterias:
        print(criteria, " : ", criteria.check(CG, test_sets))
