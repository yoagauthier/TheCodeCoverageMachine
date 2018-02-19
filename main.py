# from model.criteria import TA
from model.cover_graph import CoverGraph
from model.astree import ASTree

if __name__ == "__main__":

    # load the programm into an ASTree
    # get the initial values of the variables

    tree = ASTree('Examples/exemple.txt')
    CG = tree.to_cover_graph()
    CG.get_all_paths([{'X': 12}])

    # criterias = [TA]
    # for criteria in criterias:
    #     for value in initial_values:
    #         print(criteria, " : ", criteria.check(cover_graph, value))
