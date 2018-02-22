"""
Autors: Yoann Gauthier and Thibaut Seys
Date: 21/02/2018

This file defines all the logic for criteria classes.
"""


class Criteria(object):

    def check(self, control_flow_graph, test_sets):
        """Generate all paths from test_sets list and then compare different paths."""
        execution_paths = control_flow_graph.get_all_paths(test_sets)
        return self.check_criteria_against_paths(control_flow_graph, execution_paths)

    def check_criteria_against_paths(self, control_flow_graph, execution_paths):
        """Should return True or False depending on the criteria"""
        raise NotImplementedError

    def __repr__(self):
        return "Criteria Type"


class TA(Criteria):
    """Get all the labels of the cover graph, and checks if they are all defined
    in the nodes of the programm"""

    def check_criteria_against_paths(self, control_flow_graph, execution_paths):
        assigned = []
        for path in execution_paths:
            for vertex in path:
                if vertex.operation == 'assignment':
                    assigned.append(vertex)

        for vertex in control_flow_graph.vertices:
            if vertex.operation == 'assignment' and vertex not in assigned:
                return False
        return True

    def __repr__(self):
        return "TA - All assignments"


class TD(Criteria):
    """Get all the edges of type "while" or "if" and checks that they are evaluated"""

    def check_criteria_against_paths(self, control_flow_graph, execution_paths):
        decided = []
        for path in execution_paths:
            for index, vertex in enumerate(path):
                if vertex.operation in ['if', 'while']:
                    decided.append(path[index + 1])

        for edge in control_flow_graph.edges:
            if edge.root_vertex.operation in ['if', 'while'] and edge.child_vertex not in decided:
                return False
        return True

    def __repr__(self):
        return "TD - All decisions"


class kTC(Criteria):
    """We get all the k paths from the cover graph (all the "small paths") and
    check if they are in the execution_paths we got from execution."""

    def __init__(self, k=1):
        self.k = k

    def check_criteria_against_paths(self, control_flow_graph, execution_paths):
        k_paths = []
        # we get all the possible paths
        for path in execution_paths:
            k_paths.append(path[:self.k])

        # if in all the k paths from the cover graph
        for path in control_flow_graph.get_all_k_paths(self.k):
            if path not in k_paths:
                return False
        return True

    def __repr__(self):
        return """k - TC - All {} paths""".format(self.k)
