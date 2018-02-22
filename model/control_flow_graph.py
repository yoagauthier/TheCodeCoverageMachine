"""
Autors: Yoann Gauthier and Thibaut Seys
Date: 21/02/2018

This file defines all logic needed for control flow graph object
"""
from model.error import ExecutionError


class ControlFlowGraph(object):
    """
    This class represents all the logic to represent control flow graph.
    + properties:
        - root_vertex: the source vertex from which the porgram will start
        - end_certex: the target vertex from which the program will end
        - vertices: all vertices stored in a list
        - edges: all edges stored in a list
    + methods:
        - renamed_edges: changes the old vertex by the new vertex in edges
        - get_path: returns the node list for the given starting environment
        - get_all_paths: returns the node list for the given starting environment list
        - get_all_k_paths: returns all the path with length if k
    """

    def __init__(self, root_vertex=None, end_vertex=None, vertices=[], edges=[]):
        self.root_vertex = root_vertex
        self.end_vertex = end_vertex
        self.vertices = vertices
        self.edges = edges

    def renamed_edges(self, old_vertex, new_vertex):
        """Return edges with old_vertex replaced by new_vertex. We do not affect self.edges"""
        new_edges = []
        for edge in self.edges:
            edge.root_vertex = (
                new_vertex
                if edge.root_vertex == old_vertex
                else edge.root_vertex
            )
            edge.child_vertex = (
                new_vertex
                if edge.child_vertex == old_vertex
                else edge.child_vertex
            )
            new_edges.append(edge)
        return new_edges

    def get_path(self, test_set):
        """
        Returns the vertex list we get from execution given test_set as input.
        Summary: We start from root_vertex and we take the succesor which respect the condition. We
        stops arrived at the end_vertex.
        """
        L = []
        values = test_set
        vertex = self.root_vertex
        L.append(self.root_vertex)
        while vertex.label != '_':
            out_edges = [edge for edge in self.edges if edge.root_vertex == vertex]
            # choose which edge to take
            for edge in out_edges:
                if edge.eval(values):  # ie eval was possible and gave a valid path
                    out_edge = edge
                    values = edge.eval(values)
                    break
            if not out_edge:
                raise ExecutionError
            vertex = out_edge.child_vertex
            L.append(vertex)
        return L  # list of vertices that we've been through

    def get_all_paths(self, test_sets):
        """
        Returns all_paths from test_sets.
        test_sets should like [{var1: val1, var2: val2, ...}, ...], each dict is a set of variables
        """
        paths = []
        for test_set in test_sets:
            paths.append(self.get_path(test_set))
        return paths  # paths is like [[vertex1, vertex2, ...], [vertex1, vertex4, ...], ...]

    def _get_all_k_paths_util(self, start_vertex, end_vertex, k, current_path, all_paths):
        """
        Util function that delegates logic from get_all_k_paths.
        inspired from https://www.geeksforgeeks.org/find-paths-given-source-destination/
        except we do not need to mark visited vertices as we only got down in the graph
        """
        current_path.append(start_vertex)
        if len(current_path) > k:
            pass
        elif start_vertex == end_vertex:
            all_paths.append(current_path)
        else:
            for edge in start_vertex.get_child_edges(self):
                self._get_all_k_paths_util(edge.child_vertex, end_vertex, k, current_path, all_paths)

        current_path.pop()

    def get_all_k_paths(self, k):
        """Returns all k paths of the cover path"""
        all_paths = []
        current_path = []
        self._get_all_k_paths_util(self.root_vertex, self.end_vertex, k, current_path, all_paths)
        return all_paths

    def get_labels(self, operations=['assignment', 'skip', 'if', 'while']):
        return [vertex.label for vertex in self.vertices if vertex.operation in operations]

    def get_variables(self):
        to_return = set()
        for edge in self.edges:
            to_return |= edge.get_variables()
        return to_return

    def get_def_variables(self, vertex):
        to_return = set()
        for edge in self.edges:
            if type(vertex) == int:
                if edge.root_vertex.operation == 'assignment' and edge.root_vertex.label == vertex:
                    to_return |= edge.operation.left_expression.get_variables()
            else:
                if edge.root_vertex.operation == 'assignment' and edge.root_vertex == vertex:
                    to_return |= edge.operation.left_expression.get_variables()
        return to_return

    def get_ref_variables(self, vertex):
        to_return = set()
        for edge in self.edges:
            if type(vertex) == int:
                if edge.root_vertex.label == vertex:
                    if edge.root_vertex.operation == 'assignment':
                        to_return |= edge.operation.right_expression.get_variables()
                    to_return |= edge.condition.get_variables()
            else:
                if edge.root_vertex == vertex:
                    if edge.root_vertex.operation == 'assignment':
                        to_return |= edge.operation.right_expression.get_variables()
                    to_return |= edge.condition.get_variables()
        return to_return

    def __str__(self):
        return '\n'.join([str(edge) for edge in self.edges])


class Vertex(object):
    """
    Vertex logic for control flow graph.
    + properties:
        - label: the label of the vertex (should be int or '_')
        - operation: should be in possible_operation
    + methods:
        - get_edges: return all edges that contain the vertex
        - get_child_edges: return a list of all child edges connected to this vertex
    """
    possible_operations = ['assignment', 'skip', 'if', 'while', 'end']

    def __init__(self, label, operation):
        self.label = label
        self.operation = operation

    def get_edges(self, cover_graph):
        """Returns a list of all the edges connected to this vertex"""
        L = []
        for edge in cover_graph.edges:
            if edge.root_vertex == self or edge.child_vertex == self:
                L.append(edge)
        return L

    def get_child_edges(self, cover_graph):
        """Returns a list of all the child edges connected to this vertex"""
        L = []
        for edge in cover_graph.edges:
            # self is root of the edge, so the edge is child of self
            if edge.root_vertex == self:
                L.append(edge)
        return L

    def __str__(self):
        return '{}'.format(self.label)


class Edge(object):
    """An edge should represent a step between two nodes, and might be paired
    with a condition (if there are possibly many children to the node, each
    edge represent a possibility for the condition)"""

    def __init__(self, root_vertex, child_vertex, condition, operation):
        self.root_vertex = root_vertex
        self.child_vertex = child_vertex
        self.condition = condition  # boolean node
        self.operation = operation  # assignement or skip node

    def eval(self, values):
        """Returns a value if the eval was possible, None otherwise"""
        if self.condition.eval(values):
            return self.operation.eval(values)
        else:
            return None

    def get_variables(self):
        return self.condition.get_variables() | self.operation.get_variables()

    def __str__(self):
        return '{} --({}/{})--> {}'.format(
            self.root_vertex,
            self.condition,
            self.operation,
            self.child_vertex,
        )
