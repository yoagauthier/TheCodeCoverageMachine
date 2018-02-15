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

    def __str__(self, index=0):
        return '{variable: {}}'.format(self.expression, index + 1)


class NumberNode(UnaryNode):
    def is_number(self):
        return type(self.expression) == int

    def __str__(self, index=0):
        return '(number: {})'.format(self.expression, index + 1)


class BooleanNode(UnaryNode):
    def is_boolean_variable(self):
        return type(self.expression) == str and self.expression in Token.boolean_key_words

    def __str__(self, index=0):
        return '{number: {}}'.format(self.expression, index + 1)


class NotNode(UnaryNode):
    def __str__(self, index=0):
        return '{not: {}}'.format(self.expression, index + 1)


class SkipNode(UnaryNode):
    def __str__(self, index=0):
        return '{skip: {}}'.format(self.expression, index + 1)


class BinaryNode(Node):
    def __init__(self, left_expression, right_expression):
        self.left_expression = left_expression
        self.right_expression = right_expression


class ArithmeticOperator(object):
    pass


class AddNode(ArithmeticOperator, BinaryNode):
    def __str__(self, index=0):
        return '{arithmetic operator: +, left: {}, right: {}}'.format(
            self.left_expression,
            self.right_expression
        )


class MinusNode(ArithmeticOperator, BinaryNode):
    def __str__(self, index=0):
        return '{arithmetic operator: -, left: {}, right: {}}'.format(
            self.left_expression,
            self.right_expression
        )


class TimesNode(ArithmeticOperator, BinaryNode):
    def __str__(self, index=0):
        return '{arithmetic operator: *, left: {}, right: {}}'.format(
            self.left_expression,
            self.right_expression
        )


class DivideNode(ArithmeticOperator, BinaryNode):
    def __str__(self, index=0):
        return '{arithmetic operator: /, left: {}, right: {}}'.format(
            self.left_expression,
            self.right_expression
        )


class BooleanComparator(object):
    pass


class GteNode(BooleanComparator, BinaryNode):
    def __str__(self, index=0):
        return '{comparator: >=, left: {}, right: {}}'.format(
            self.left_expression,
            self.right_expression
        )


class GtNode(BooleanComparator, BinaryNode):
    def __str__(self, index=0):
        return '{comparator: >, left: {}, right: {}}'.format(
            self.left_expression,
            self.right_expression
        )


class LteNode(BooleanComparator, BinaryNode):
    def __str__(self, index=0):
        return '{comparator: <=, left: {}, right: {}}'.format(
            self.left_expression,
            self.right_expression
        )


class LtNode(BooleanComparator, BinaryNode):
    def __str__(self, index=0):
        return '{comparator: <, left: {}, right: {}}'.format(
            self.left_expression,
            self.right_expression
        )


class BooleanOperator(object):
    pass


class AndNode(BooleanOperator, BinaryNode):
    def __str__(self, index=0):
        return '{boolean operator: and, left: {}, right: {}}'.format(
            self.left_expression,
            self.right_expression
        )


class OrNode(BooleanOperator, BinaryNode):
    def __str__(self, index=0):
        return '{boolean operator: or, left: {}, right: {}}'.format(
            self.left_expression,
            self.right_expression
        )


class AssignmentNode(BinaryNode):
    def __str__(self, index=0):
        return '{assignment: {}, {}}'.format(
            self.left_expression,
            self.right_expression
        )


class SequenceNode(BinaryNode):
    def __str__(self, index=0):
        return '{c1: {}, c2: {}}'.format(
            self.left_expression,
            self.right_expression
        )


class WhileNode(BinaryNode):
    def __str__(self, index=0):
        return '{while: {}, do: {}}'.format(
            self.left_expression,
            self.right_expression
        )


class IfNode(Node):
    def __init__(self, condition_expression, then_expression, else_expression):
        self.condition_expression = condition_expression
        self.then_expression = then_expression
        self.else_expression = else_expression

    def __str__(self, index=0):
        return '{if: {}, then: {}, else: {}}'.format(
            self.condition_expression,
            self.then_expression,
            self.else_expression
        )
