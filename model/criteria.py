"""
Autors: Yoann Gauthier and Thibaut Seys
Date: 21/02/2018

This file defines all the logic for criteria classes.
"""
from model.nodes import BooleanOperatorNode, BooleanComparatorNode, BooleanNode, NotNode
from model.error import ExecutionError


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


class TC(Criteria):
    """
    We get all the conditions from the cover graph (get all decisions, then
    extract conditions from these decisions) and check if they are in some of
    the condition of the execution_paths we got from execution.
    """

    def check(self, control_flow_graph, test_sets):
        """Generate all paths from test_sets list and then compare different paths."""
        conditions = self.get_conditions(control_flow_graph)
        conditions = {condition: {True: None, False: None} for condition in conditions}

        for test_set in test_sets:
            conditions = self.check_conditions_from_test_set(
                control_flow_graph,
                test_set,
                conditions
            )

        for condition in conditions.values():
            if not(condition[True] is not None and condition[False] is not None):
                return False

        return True

    def check_conditions_from_test_set(self, control_flow_graph, test_set, conditions):
        vertex = control_flow_graph.root_vertex
        while vertex.label != '_':
            out_edges = [edge for edge in control_flow_graph.edges if edge.root_vertex == vertex]
            for edge in out_edges:
                possible_conditions = []
                self.get_conditions_from_decision(edge.condition, possible_conditions)
                for condition in possible_conditions:
                    if condition.eval(test_set):
                        conditions[condition][True] = True
                    else:
                        conditions[condition][False] = True
                if edge.eval(test_set):
                    out_edge = edge
                    test_set = edge.eval(test_set)
                    break
            if not out_edge:
                raise ExecutionError
            vertex = out_edge.child_vertex
        return conditions

    def get_conditions(self, control_flow_graph):
        # get all conditions in cover graph
        decisions = [edge.condition for edge in control_flow_graph.edges]
        conditions = []
        for subdecision in decisions:
            if isinstance(subdecision, (BooleanOperatorNode, BooleanComparatorNode)):
                self.get_conditions_from_decision(subdecision, conditions)
        return conditions

    def get_conditions_from_decision(self, decision, conditions):
        if isinstance(decision, BooleanComparatorNode):
            conditions.append(decision)
        elif isinstance(decision, BooleanOperatorNode):
            self.get_conditions_from_decision(decision.left_expression, conditions)
            self.get_conditions_from_decision(decision.right_expression, conditions)
        elif isinstance(decision, NotNode):
            self.get_conditions_from_decision(decision.expression, conditions)
        elif isinstance(decision, BooleanNode):
            pass
        else:
            raise ExecutionError

    def __repr__(self):
        return """TC - All conditions"""
