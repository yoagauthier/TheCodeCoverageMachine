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

    def __str__(self):
        return '\n'.join([str(edge) for edge in self.edges])


class Vertex(object):
    possible_operations = ['assignment', 'skip', 'if', 'while', 'end']

    def __init__(self, label, operation):
        self.label = label
        self.operation = operation

    def __str__(self):
        return '{}'.format(self.label)


class Edge(object):
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
