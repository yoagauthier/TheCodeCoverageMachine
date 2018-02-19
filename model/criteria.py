from model.cover_graph import Vertex
from model.nodes import AssignmentNode, IfNode, WhileNode


class Criteria(object):

    def check(self, cover_graph, test_sets):
        execution_paths = cover_graph.get_all_paths(test_sets)
        return self.check_criteria_against_paths(cover_graph, execution_paths)

    def check_criteria_against_paths(self, cover_graph, execution_paths):
        """
        Should return True or False depending on the criteria
        """
        raise NotImplementedError

    def __repr__(self):
        return "Criteria Type"


class TA(Criteria):
    """
    Get all the labels of the cover graph, and checks if they are all defined
    in the nodes of the programm
    """

    def check_criteria_against_paths(self, cover_graph, execution_paths):
        assigned = []
        for path in execution_paths:
            for vertex in path:
                edges = vertex.get_edges(cover_graph)
                for edge in edges:
                    if isinstance(edge.operation, AssignmentNode):
                        assigned.append(edge)

        for edge in cover_graph.edges:
            if isinstance(edge.operation, AssignmentNode) and edge not in assigned:
                return False
        return True

    def __repr__(self):
        return "TA - All assignments"


class TD(Criteria):
    """
    Get all the edges of type "while" or "if" and checks that they are evaluated
    """

    def check_criteria_against_paths(self, cover_graph, execution_paths):
        decided = []
        for path in execution_paths:
            for vertex in path:
                edges = vertex.get_edges(cover_graph)
                for edge in edges:
                    if isinstance(edge.operation, IfNode) or isinstance(edge.operation, WhileNode):
                        decided.append(edge)

        for edge in cover_graph.edges:
            if isinstance(edge.operation, IfNode) or isinstance(edge.operation, WhileNode) \
                    and edge not in decided:
                return False
        return True

    def __repr__(self):
        return "TD - All decisions"


class kTC(Criteria):

    def __init__(self, k=1):
        self.k = k

    def check_criteria_against_paths(self, cover_graph, execution_path):
        for path in execution_paths:


    def __repr__(self):
        return """k - TC - All {} paths""".format(self.k)
