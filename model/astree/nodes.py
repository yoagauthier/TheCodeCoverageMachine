from model.astree.tokenizer import Token


class Node(object):
    def is_arithmetic(self):
        if isinstance(self, VariableNode):
            return self.is_variable()
        elif isinstance(self, NumberNode):
            return self.is_number()
        elif isinstance(self, ArithmeticOperator):
            return self.left_expression.is_arithmetic() and self.right_expression.is_arithmetic()
        else:
            return False

    def is_boolean(self):
        if isinstance(self, BooleanNode):
            return self.is_boolean_variable()
        elif isinstance(self, BooleanComparator):
            return self.left_expression.is_arithmetic() and self.right_expression.is_arithmetic()
        elif isinstance(self, NotNode):
            return self.expression.is_boolean()
        elif isinstance(self, BooleanOperator):
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
                self.then_condition.is_program() and
                self.else_condition.is_program()
            )
        elif isinstance(self, WhileNode):
            return self.left_epxression.is_boolean() and self.right_expression.is_program()
        else:
            return False


class UnaryNode(Node):
    def __init__(self, expression):
        self.expression = expression


class VariableNode(UnaryNode):
    def is_variable(self):
        return type(self.expression) == str and self.expression not in Token.key_words

    def to_dict(self):
        return {'variable': self.expression}


class NumberNode(UnaryNode):
    def is_number(self):
        return type(self.expression) == int

    def to_dict(self):
        return {'number': self.expression}


class BooleanNode(UnaryNode):
    def is_boolean_variable(self):
        return type(self.expression) == str and self.expression in Token.boolean_key_words

    def to_dict(self):
        return {'boolean': self.expression}


class NotNode(UnaryNode):
    def to_dict(self):
        return {'not': self.expression.to_dict()}


class SkipNode(UnaryNode):
    def to_dict(self):
        return {'skip': self.expression}


class BinaryNode(Node):
    def __init__(self, left_expression, right_expression):
        self.left_expression = left_expression
        self.right_expression = right_expression


class ArithmeticOperator(object):
    def to_dict(self):
        return {
            'arithmetic operator': self.operator,
            'left': self.left_expression.to_dict(),
            'right': self.right_expression.to_dict(),
        }


class AddNode(ArithmeticOperator, BinaryNode):
    operator = '+'


class MinusNode(ArithmeticOperator, BinaryNode):
    operator = '-'


class TimesNode(ArithmeticOperator, BinaryNode):
    operator = '*'


class DivideNode(ArithmeticOperator, BinaryNode):
    operator = '/'


class BooleanComparator(object):
    def to_dict(self):
        return {
            'comparator': self.comparator,
            'left': self.left_expression.to_dict(),
            'right': self.right_expression.to_dict()
        }


class GteNode(BooleanComparator, BinaryNode):
    comparator = '>='


class GtNode(BooleanComparator, BinaryNode):
    comparator = '>'


class LteNode(BooleanComparator, BinaryNode):
    comparator = '<='


class LtNode(BooleanComparator, BinaryNode):
    comparator = '<'


class EqualNode(BooleanComparator, BinaryNode):
    comparator = '='


class BooleanOperator(object):
    def to_dict(self):
        return {
            'boolean operator': self.operator,
            'left': self.left_expression.to_dict(),
            'right': self.right_expression.to_dict()
        }


class AndNode(BooleanOperator, BinaryNode):
    operator = 'and'


class OrNode(BooleanOperator, BinaryNode):
    operator = 'or'


class AssignmentNode(BinaryNode):
    def to_dict(self):
        return {
            'assignment': {
                'left': self.left_expression.to_dict(),
                'right': self.right_expression.to_dict()
            }
        }


class SequenceNode(BinaryNode):
    def to_dict(self):
        return {
            'c1': self.left_expression.to_dict(),
            'c2': self.right_expression.to_dict()
        }


class WhileNode(BinaryNode):
    def to_dict(self):
        return {
            'while': self.left_expression.to_dict(),
            'do': self.right_expression.to_dict()
        }


class IfNode(Node):
    def __init__(self, condition_expression, then_expression, else_expression):
        self.condition_expression = condition_expression
        self.then_expression = then_expression
        self.else_expression = else_expression

    def to_dict(self):
        return {
            'if': self.condition_expression.to_dict(),
            'then': self.then_expression.to_dict(),
            'else': self.else_expression.to_dict()
        }
