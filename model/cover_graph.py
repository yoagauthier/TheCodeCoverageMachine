class CoverGraph(object):

    def __init__(self, nodes, verteces):
        self.nodes = nodes
        self.verteces = verteces

    def to_execution_path_tree(self):
        pass
        # return execution_path_tree


class Node(object):

    def __init__(self, label=''):
        self.label = label
        # Needed here ?
        # self.operation = operation (dans assign, skip, while, if)


class Vertex(object):

    def __init__(self, root_node, child_node, condition, operation):
        self.root_node = root_node
        self.child_node = child_node
        self.condition = condition  # boolean expression
        self.operation = operation  # assign, skip
