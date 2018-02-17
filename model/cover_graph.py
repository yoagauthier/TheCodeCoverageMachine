class CoverGraph(object):
    def __init__(self, root_vertex=None, end_vertex=None, vertices=[], edges=[]):
        self.root_vertex = root_vertex
        self.end_vertex = end_vertex
        self.vertices = vertices
        self.edges = edges

    def to_execution_path_tree(self):
        pass

    def renamed_edges(self, old_vertex, new_vertex):
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

    # def to_ep_tree(self):
    #     # need to do a BFS
    #     self.L = []  # list of verteces
    #     T = []
    #     self.visit_node(self.root_node)
    #     while self.L:
    #         root, child = self.L.pop(0)
    #         if not child.visited:
    #             T.append((root, child))
    #             self.visit_node(child)
    #
    #     return T  # execution_path_tree
    #
    # def get_next_node(self, current_node, variable):
    #     pass

    def get_path(self, initial_variable):
        # DRAFT
        # doing a BFS, need to return a list of node and edges
        L = []
        L.append(self.root_vertex)
        var = initial_variable
        while L:
            child = self.get_next_node(L.pop(), var)
            var = child.execute_step(var)
            L.append(child)

        # on part de la root node
        # on prend pour chaque node la successeur, en vérifiant la condition
        # on s'arrête à la node finale
        # return  path, qui est une liste d'edge et de nodes

    def get_all_nodes(self):
        """Returns all the nodes of the cover graph"""
        raise NotImplementedError

    # def visit_node(self, node):
    #     node.visited = True
    #     for vertex in (self.vertices.root_node, self.vertices.child_node):
    #         self.L.append(vertex)

    def __str__(self):
        return '\n'.join([str(edge) for edge in self.edges])


class Vertex(object):
    possible_operations = ['assignment', 'skip', 'if', 'while', 'end']

    def __init__(self, label, operation):
        self.label = label
        self.operation = operation

    def execute_step(self, var):
        # execute the operation
        pass
        # verify that the condition is fullfilled and return the value of the next variable

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

    def __str__(self):
        return '{} --({}/{})--> {}'.format(
            self.root_vertex,
            self.condition,
            self.operation,
            self.child_vertex,
        )
