from pprint import pformat

from model.cover_graph import CoverGraph, Edge, Vertex
from model.tokenizer import Token


class ExecutionError(Exception):
    pass


class Node(object):
    seen_labels = []

    def is_arithmetic(self):
        if isinstance(self, VariableNode):
            return self.is_variable()
        elif isinstance(self, NumberNode):
            return self.is_number()
        elif isinstance(self, ArithmeticOperatorNode):
            return self.left_expression.is_arithmetic() and self.right_expression.is_arithmetic()
        else:
            return False

    def is_boolean(self):
        if isinstance(self, BooleanNode):
            return self.is_boolean_variable()
        elif isinstance(self, BooleanComparatorNode):
            return self.left_expression.is_arithmetic() and self.right_expression.is_arithmetic()
        elif isinstance(self, NotNode):
            return self.expression.is_boolean()
        elif isinstance(self, BooleanOperatorNode):
            return self.left_expression.is_boolean() and self.right_expression.is_boolean()
        else:
            return False

    def is_program(self):
        if isinstance(self, SkipNode):
            return True
        elif isinstance(self, AssignmentNode):
            return self.left_expression.is_variable() and self.right_expression.is_arithmetic()
        elif isinstance(self, SequenceNode):
            return self.left_expression.is_program() and self.right_expression.is_program()
        elif isinstance(self, IfNode):
            return (
                self.condition_expression.is_boolean() and
                self.then_expression.is_program() and
                self.else_expression.is_program()
            )
        elif isinstance(self, WhileNode):
            return self.left_expression.is_boolean() and self.right_expression.is_program()
        else:
            return False

    def is_well_labelled(self):
        return len(self.seen_labels) == len(set(self.seen_labels))

    def get_variables(self, variables=set()):
        raise NotImplementedError

    def eval(self, env):
        raise NotImplementedError

    def to_dict(self):
        raise NotImplementedError

    def __str__(self):
        return pformat(self.to_dict())


class UnaryNode(Node):
    def __init__(self, expression):
        self.expression = expression


class VariableNode(UnaryNode):
    def is_variable(self):
        return type(self.expression) == str and self.expression not in Token.key_words

    def eval(self, env):
        try:
            return env[self.expression]
        except KeyError:
            raise ExecutionError

    def to_dict(self):
        return {'variable': self.expression}

    def get_variables(self, variables=set()):
        return variables | set(self.expression)


class NumberNode(UnaryNode):
    def is_number(self):
        return type(self.expression) == int

    def eval(self, env):
        return self.expression

    def to_dict(self):
        return {'number': self.expression}

    def get_variables(self, variables=set()):
        return variables


class BinaryNode(Node):
    def __init__(self, left_expression, right_expression):
        self.left_expression = left_expression
        self.right_expression = right_expression

    def get_variables(self, variables=set()):
        return (
            variables |
            self.left_expression.get_variables(variables) |
            self.right_expression.get_variables(variables)
        )


class ArithmeticOperatorNode(BinaryNode):
    def to_dict(self):
        return {
            'arithmetic operator': self.operator,
            'left': self.left_expression.to_dict(),
            'right': self.right_expression.to_dict(),
        }


class AddNode(ArithmeticOperatorNode):
    operator = '+'

    def eval(self, env):
        return self.left_expression.eval(env) + self.right_expression.eval(env)


class MinusNode(ArithmeticOperatorNode):
    operator = '-'

    def eval(self, env):
        return self.left_expression.eval(env) - self.right_expression.eval(env)


class TimesNode(ArithmeticOperatorNode):
    operator = '*'

    def eval(self, env):
        return self.left_expression.eval(env) * self.right_expression.eval(env)


class DivideNode(ArithmeticOperatorNode):
    operator = '/'

    def eval(self, env):
        return self.left_expression.eval(env) / self.right_expression.eval(env)


class BooleanNode(UnaryNode):
    def is_boolean_variable(self):
        return type(self.expression) == str and self.expression in Token.boolean_key_words

    def eval(self, env):
        return True if self.expression == 'true' else False

    def to_dict(self):
        return {'boolean': self.expression}

    def get_variables(self, variables=set()):
        return variables


class BooleanComparatorNode(BinaryNode):
    def to_dict(self):
        return {
            'comparator': self.comparator,
            'left': self.left_expression.to_dict(),
            'right': self.right_expression.to_dict()
        }


class GteNode(BooleanComparatorNode):
    comparator = '>='

    def eval(self, env):
        return self.left_expression.eval(env) >= self.right_expression.eval(env)


class GtNode(BooleanComparatorNode):
    comparator = '>'

    def eval(self, env):
        return self.left_expression.eval(env) > self.right_expression.eval(env)


class LteNode(BooleanComparatorNode):
    comparator = '<='

    def eval(self, env):
        return self.left_expression.eval(env) <= self.right_expression.eval(env)


class LtNode(BooleanComparatorNode):
    comparator = '<'

    def eval(self, env):
        return self.left_expression.eval(env) < self.right_expression.eval(env)


class EqualNode(BooleanComparatorNode):
    comparator = '='

    def eval(self, env):
        return self.left_expression.eval(env) == self.right_expression.eval(env)


class BooleanOperatorNode(BinaryNode):
    def to_dict(self):
        return {
            'boolean operator': self.operator,
            'left': self.left_expression.to_dict(),
            'right': self.right_expression.to_dict()
        }


class AndNode(BooleanOperatorNode):
    operator = 'and'

    def eval(self, env):
        return self.left_expression.eval(env) and self.right_expression.eval(env)


class OrNode(BooleanOperatorNode):
    operator = 'or'

    def eval(self, env):
        return self.left_expression.eval(env) or self.right_expression.eval(env)


class NotNode(UnaryNode):
    def eval(self, env):
        return not self.expression.eval(env)

    def to_dict(self):
        return {'not': self.expression.to_dict()}

    def get_variables(self, variables=set()):
        return variables | self.expression.get_variables()


class ProgramNode(object):
    def to_cover_graph(self):
        raise NotImplementedError


class SkipNode(UnaryNode, ProgramNode):
    def __init__(self, expression, label):
        super().__init__(expression)
        self.label = label
        self.seen_labels.append(label)

    def to_cover_graph(self):
        root_vertex = Vertex(self.label, 'skip')
        end_vertex = Vertex('_', 'end')
        edge = Edge(root_vertex, end_vertex, BooleanNode('true'), self)
        return CoverGraph(root_vertex, end_vertex, [root_vertex, end_vertex], [edge])

    def eval(self, env):
        return env

    def to_dict(self):
        return {'{}: skip'.format(self.label): self.expression}

    def get_variables(self, variables=set()):
        return variables


class AssignmentNode(BinaryNode, ProgramNode):
    def __init__(self, left_expression, right_expression, label):
        super().__init__(left_expression, right_expression)
        self.label = label
        self.seen_labels.append(label)

    def to_cover_graph(self):
        root_vertex = Vertex(self.label, 'assignment')
        end_vertex = Vertex('_', 'end')
        edge = Edge(root_vertex, end_vertex, BooleanNode('true'), self)
        return CoverGraph(root_vertex, end_vertex, [root_vertex, end_vertex], [edge])

    def eval(self, env):
        env[self.left_expression.expression] = self.right_expression.eval(env)
        return env

    def to_dict(self):
        return {
            '{}: assignment'.format(self.label): {
                'left': self.left_expression.to_dict(),
                'right': self.right_expression.to_dict()
            }
        }


class SequenceNode(BinaryNode, ProgramNode):
    def to_cover_graph(self):
        cover_graph_1 = self.left_expression.to_cover_graph()
        cover_graph_2 = self.right_expression.to_cover_graph()
        root_vertex = cover_graph_1.root_vertex
        end_vertex = cover_graph_2.end_vertex
        vertices = cover_graph_1.vertices + cover_graph_2.vertices
        vertices.remove(cover_graph_1.end_vertex)
        edges = (
            cover_graph_1.renamed_edges(cover_graph_1.end_vertex, cover_graph_2.root_vertex) +
            cover_graph_2.edges
        )
        return CoverGraph(root_vertex, end_vertex, vertices, edges)

    def eval(self, env):
        env = self.left_expression.eval(env)
        return self.right_expression.eval(env)

    def to_dict(self):
        return {
            'c1': self.left_expression.to_dict(),
            'c2': self.right_expression.to_dict()
        }


class WhileNode(BinaryNode, ProgramNode):
    def __init__(self, left_expression, right_expression, label):
        super().__init__(left_expression, right_expression)
        self.label = label
        self.seen_labels.append(label)

    def to_cover_graph(self):
        cover_graph = self.right_expression.to_cover_graph()
        root_vertex = Vertex(self.label, 'while')
        end_vertex = cover_graph.end_vertex
        vertices = [root_vertex] + cover_graph.vertices
        edges = [
            Edge(
                root_vertex,
                cover_graph.root_vertex,
                self.left_expression, SkipNode('_', self.label)
            )
        ] + cover_graph.renamed_edges(cover_graph.end_vertex, root_vertex) + [
            Edge(
                root_vertex,
                end_vertex,
                NotNode(self.left_expression),
                SkipNode('_', self.label)
            )
        ]
        return CoverGraph(root_vertex, end_vertex, vertices, edges)

    def eval(self, env):
        if self.left_expression.eval(env):
            env = self.right_expression.eval(env)
            return self.eval(env)
        return env

    def to_dict(self):
        return {
            '{}: while'.format(self.label): self.left_expression.to_dict(),
            'do': self.right_expression.to_dict()
        }


class IfNode(Node, ProgramNode):
    def __init__(self, condition_expression, then_expression, else_expression, label):
        self.condition_expression = condition_expression
        self.then_expression = then_expression
        self.else_expression = else_expression
        self.label = label
        self.seen_labels.append(label)

    def to_cover_graph(self):
        cover_graph_1 = self.then_expression.to_cover_graph()
        cover_graph_2 = self.else_expression.to_cover_graph()
        root_vertex = Vertex(self.label, 'if')
        end_vertex = cover_graph_2.end_vertex
        vertices = [root_vertex] + cover_graph_1.vertices[:-1] + cover_graph_2.vertices
        edges = [
            Edge(
                root_vertex,
                cover_graph_1.root_vertex,
                self.condition_expression,
                SkipNode('_', cover_graph_1.root_vertex.label)
            )
        ] + cover_graph_1.renamed_edges(cover_graph_1.end_vertex, cover_graph_2.end_vertex) + [
            Edge(
                root_vertex,
                cover_graph_2.root_vertex,
                NotNode(self.condition_expression),
                SkipNode('_', cover_graph_2.root_vertex.label)
            )
        ] + cover_graph_2.edges
        return CoverGraph(root_vertex, end_vertex, vertices, edges)

    def eval(self, env):
        if self.condition_expression.eval(env):
            return self.then_expression.eval(env)
        return self.else_expression.eval(env)

    def to_dict(self):
        return {
            '{}: if'.format(self.label): self.condition_expression.to_dict(),
            'then': self.then_expression.to_dict(),
            'else': self.else_expression.to_dict()
        }

    def get_variables(self, variables=set()):
        return (
            variables |
            self.condition_expression.get_variables(variables) |
            self.else_expression.get_variables(variables) |
            self.then_expression.get_variables(variables)
        )
