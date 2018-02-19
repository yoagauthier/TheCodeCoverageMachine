class CoverGraph(object):
    def __init__(self, root_vertex=None, end_vertex=None, vertices=[], edges=[]):
        self.root_vertex = root_vertex
        self.end_vertex = end_vertex
        self.vertices = vertices
        self.edges = edges

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

    def get_path(self, test_set):
        # on part de la root node
        # on prend pour chaque node la successeur, en vérifiant la condition
        # on s'arrête à la node finale
        # return  path, qui est une liste d'edge et de nodes
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
                raise "Programm non executable"
            vertex = out_edge.child_vertex
            L.append(vertex)
        return L  # list of vertices that we've been through

    def get_all_paths(self, test_sets):
        # test set should like [{var1: val1, var2: val2, ...}, ...], each dict
        # is a set of variables
        paths = []
        for test_set in test_sets:
            paths += self.get_path(test_set)
        print("PATHS", paths)
        return paths

    def get_all_nodes(self):
        """Returns all the nodes of the cover graph"""
        raise NotImplementedError

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

    def eval(self, values):
        """Returns a value if the eval was possible, None otherwise"""
        if self.condition.eval(values):
            return self.operation.eval(values)
        else:
            return None

    def __str__(self):
        return '{} --({}/{})--> {}'.format(
            self.root_vertex,
            self.condition,
            self.operation,
            self.child_vertex,
        )
