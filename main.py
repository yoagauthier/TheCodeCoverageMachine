import math

if __name__ == "__main__":
    E = [
        (0, 1, 'x =< 0')
    ]
    V = [
        0,
        1,
        2,
        3,
        4,
        5,
    ]

class ASTree(object):



    def to_cover_graph(self):
        """Converts this ASTree to a cover graph"""

        return cover_graph


class CoverGraph(object):

    def __init__(self, nodes, verteces):
        self.nodes = nodes
        self.verteces = verteces

    def to_execution_path_tree(self):
        return execution_path_tree


class Node(object):

    def __init__(self, label=''):
        self.label = label
        # Needed here ?
        # self.operation = operation (dans assign, skip, while, if)


class Vertex(object):

    def __init__(self, root_node, child_node, condition, operation):
        self.root_node = root_node
        self.child_node = child_node
        self.condition = condition # boolean expression
        self.operation = operation # assign, skip


# Need to generate the Tree from the coverGraph.
class ExecutionPathsTree(object):
    """This tree will be generated from the CoverGraph.
    It will contain all the possible paths to the possible states of the
    programm.
    """

    def check_criteria(self, criteria):
        """
        """
        return covered_paths_percentage, ens_uncovered_paths


# class Criteria(object):
#
#     def get_list(self, graph):
#         """Give the list that will be useful to the criteria"""
