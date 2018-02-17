from model.criteria import TA
from model.cover_graph import CoverGraph

if __name__ == "__main__":

    # load the programm into an ASTree
    # get the initial values of the variables

    # convert the ASTree to a CoverGraph
    initial_values = [0, 1]
    cover_graph = CoverGraph()

    criterias = [TA]
    for criteria in criterias:
        for value in initial_values:
            print(criteria, " : ", criteria.check(cover_graph, value))
