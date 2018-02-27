"""
Autors: Yoann Gauthier and Thibaut Seys
Date: 21/02/2018

This file defines all the logic for criteria classes.
"""
from model.nodes import BooleanOperatorNode, BooleanComparatorNode, BooleanNode, NotNode
from model.error import ExecutionError


class Criteria(object):

    def __init__(self):
        self.to_cover = []
        self.covered = []

    def check(self, control_flow_graph, test_sets):
        """Generate all paths from test_sets list and then compare different paths."""
        execution_paths = control_flow_graph.get_all_paths(test_sets)
        return self.check_criteria_against_paths(control_flow_graph, execution_paths)

    def check_criteria_against_paths(self, control_flow_graph, execution_paths):
        """Should return True or False depending on the criteria"""
        raise NotImplementedError

    def __repr__(self):
        return "Criteria Type"

    def __str__(self):
        to_return = self.__repr__()
        to_return += '\n======================================\n'
        try:
            to_return += 'Overall coverage : {:.2f}%'.format(
                100 * len(self.covered) / len(self.to_cover)
            )
        except ZeroDivisionError:
            to_return += 'Overall coverage : 100.00%'
        for elt in self.to_cover:
            if elt in self.covered:
                to_return += '\nElement {} -- o'.format(elt)
            else:
                to_return += '\nElement {} -- x'.format(elt)
        return to_return


class TA(Criteria):
    """Get all the labels of the cover graph, and checks if they are all defined
    in the nodes of the programm"""

    def check_criteria_against_paths(self, control_flow_graph, execution_paths):
        for vertex in control_flow_graph.vertices:
            if vertex.operation == 'assignment':
                self.to_cover.append(vertex)

        for path in execution_paths:
            for vertex in path:
                if vertex.operation == 'assignment' and vertex not in self.covered:
                    self.covered.append(vertex)

    def __repr__(self):
        return 'TA - All assignments'


class TD(Criteria):
    """Get all the edges of type "while" or "if" and checks that they are evaluated"""

    def check_criteria_against_paths(self, control_flow_graph, execution_paths):
        for edge in control_flow_graph.edges:
            if edge.root_vertex.operation in ['if', 'while']:
                self.to_cover.append(edge.child_vertex)

        for path in execution_paths:
            for index, vertex in enumerate(path):
                if vertex.operation in ['if', 'while'] and path[index + 1] not in self.covered:
                    self.covered.append(path[index + 1])

    def __repr__(self):
        return 'TD - All decisions'


class kTC(Criteria):
    """We get all the k paths from the cover graph (all the "small paths") and
    check if they are in the execution_paths we got from execution."""

    def __init__(self, k=1):
        super().__init__()
        self.k = k

    def check_criteria_against_paths(self, control_flow_graph, execution_paths):
        # all the k paths from the cover graph
        self.to_cover = control_flow_graph.get_all_k_paths(self.k)

        # we get all the possible paths
        for path in execution_paths:
            self.covered.append(path) if len(path) <= self.k and path not in self.covered else None

    def __repr__(self):
        return 'k - TC - All {} paths'.format(self.k)


class TC(Criteria):
    """
    We get all the conditions from the cover graph (get all decisions, then
    extract conditions from these decisions) and check if they are in some of
    the condition of the execution_paths we got from execution.
    """
    def __init__(self):
        self.to_cover = 0
        self.covered = 0

    def check(self, control_flow_graph, test_sets):
        """Generate all paths from test_sets list and then compare different paths."""
        self.conditions = self.get_conditions(control_flow_graph)
        self.conditions = {condition: {True: None, False: None} for condition in self.conditions}

        for test_set in test_sets:
            self.check_conditions_from_test_set(control_flow_graph, test_set)

        for evaluation in self.conditions.values():
            self.to_cover += 2
            if evaluation[True]:
                self.covered += 1
            if evaluation[False]:
                self.covered += 1

    def check_conditions_from_test_set(self, control_flow_graph, test_set):
        vertex = control_flow_graph.root_vertex
        while vertex.label != '_':
            out_edges = [edge for edge in control_flow_graph.edges if edge.root_vertex == vertex]
            for edge in out_edges:
                possible_conditions = []
                self.get_conditions_from_decision(edge.condition, possible_conditions)
                for condition in possible_conditions:
                    if condition.eval(test_set):
                        self.conditions[condition][True] = True
                    else:
                        self.conditions[condition][False] = True
                if edge.eval(test_set):
                    out_edge = edge
                    test_set = edge.eval(test_set)
                    break
            if not out_edge:
                raise ExecutionError
            vertex = out_edge.child_vertex

    def get_conditions(self, control_flow_graph):
        # get all conditions in cover graph
        decisions = [edge.condition for edge in control_flow_graph.edges]
        conditions = []
        for subdecision in decisions:
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
        return 'TC - All conditions'

    def __str__(self):
        to_return = self.__repr__()
        to_return += '\n======================================\n'
        to_return += 'Overall coverage : {:.2f}%'.format(100 * self.covered / self.to_cover)
        for condition, evaluation in self.conditions.items():
            to_return += '\nCondition {} is evaluated to:'.format(condition)
            to_return += '\n\tTrue: o' if evaluation[True] else '\n\tTrue: x'
            to_return += '\n\tFalse: o' if evaluation[False] else '\n\tFalse: x'
        return to_return


class iTB(Criteria):
    def __init__(self, i=1):
        super().__init__()
        self.i = i

    def check_criteria_against_paths(self, control_flow_graph, execution_paths):
        self.to_cover = control_flow_graph.get_all_i_loop_paths(self.i)

        for path in execution_paths:
            if path in self.to_cover and path not in self.covered:
                self.covered.append(path)

    def __repr__(self):
        return 'i - TB - All {} loops'.format(self.i)


class TDef(Criteria):
    """
    We get all the vertices containing an assigment from the cover graph and
    check if they are in some of the path of the execution_paths we got from
    execution.
    """

    def check_criteria_against_paths(self, control_flow_graph, execution_paths):
        prog_vars = control_flow_graph.get_variables()
        # we get all the vertices where there is an reference in the graph
        ref_vertices = []
        ref_variables = set()
        for var in prog_vars:
            for vertex in control_flow_graph.vertices:
                if var in control_flow_graph.get_ref_variables(vertex):
                    ref_vertices.append((var, vertex))
                    if var not in ref_variables:
                        ref_variables.add(var)

        # we also get all the vertices where there is a definition in the graph
        def_vertices = []
        for var in ref_variables:
            for vertex in control_flow_graph.vertices:
                if var in control_flow_graph.get_def_variables(vertex):
                    def_vertices.append((var, vertex))

        # getting all vertices where variables are effectively defined during the
        # execution
        def_in_exec_path = []
        for var in prog_vars:
            for path in execution_paths:
                for vertex in path:
                    for var2, vertex2 in def_vertices:
                        if var == var2 and vertex == vertex2 and vertex not in self.to_cover:
                            def_in_exec_path.append(var)
                            self.to_cover.append(vertex)

        # checking that those variables are effectively used
        for var in def_in_exec_path:
            for path in execution_paths:
                for vertex in path:
                    for var2, vertex2 in ref_vertices:
                        if var == var2 and vertex == vertex2 and vertex in self.to_cover and vertex not in self.covered:
                            self.covered.append(vertex)

    def __repr__(self):
        return "TDef - All definitions"


class TU(Criteria):
    """
    We get the vertices where variables are assigned and references, then we
    get all the possible paths for those variables where there is no re-defintion
    of those varibles. The last step is ensuring that those possible paths are
    effectively used during the execution.
    """
    def check_criteria_against_paths(self, control_flow_graph, execution_paths):
        prog_vars = control_flow_graph.get_variables()
        # we get all the vertices where there is an reference in the graph
        ref_vertices = []
        ref_variables = set()
        for var in prog_vars:
            for vertex in control_flow_graph.vertices:
                if var in control_flow_graph.get_ref_variables(vertex):
                    ref_vertices.append((var, vertex))
                    ref_variables.add(var)

        # we also get all the vertices where there is a definition in the graph
        def_vertices = []
        for var in ref_variables:
            for vertex in control_flow_graph.vertices:
                if var in control_flow_graph.get_def_variables(vertex):
                    def_vertices.append((var, vertex))

        # we get all the path without re-defintion of variables
        for var, u in def_vertices:
            for var2, v in ref_vertices:
                if var == var2 and int(u.label) < int(v.label):  # just need to check the ref if the variables are def
                    self.to_cover += control_flow_graph.get_all_possible_paths(u, v)

        # we check that the path without redefinition is effectively executed
        for path in self.to_cover:
            for exec_path in execution_paths:
                if self.is_sublist(path, exec_path) and path not in self.covered:
                    self.covered.append(path)

    def is_sublist(self, small_lst, big_lst):
        for el in small_lst:
            if el not in big_lst:
                return False
        return True

    def __repr__(self):
        return """TU - All Uses"""
