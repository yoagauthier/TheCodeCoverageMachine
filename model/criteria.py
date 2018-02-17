from model.cover_graph import Node


class Criteria(object):

    def check(self, cover_graph, initial_value):
        execution_path = cover_graph.get_path(initial_value)
        return self.check_criteria_against_path(cover_graph, execution_path)

    def check_criteria_against_path(self, cover_graph, execution_path):
        """
        Should return True or False depending on the criteria
        """
        raise NotImplementedError


class TA(Criteria):
    """
    Get all the labels of the cover graph, and checks if they are all defined
    in the nodes of the programm
    """

    def check_criteria_against_path(self, cover_graph, execution_path):
        assigned = []
        for element in execution_path:
            if isinstance(element, Node):
                if element.label:
                    assigned.append(element)
        nodes = cover_graph.get_all_nodes()
        for node in nodes:
            if node not in assigned:
                return False
        return True
