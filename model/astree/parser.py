from model.astree.nodes import (
    AddNode,
    BooleanNode,
    MinusNode,
    TimesNode,
    DivideNode,
    NumberNode,
    VariableNode,
    GtNode,
    GteNode,
    LteNode,
    LtNode,
    EqualNode,
    NotNode,
    AndNode,
    OrNode,
    SkipNode,
    AssignmentNode,
    SequenceNode,
    WhileNode,
    IfNode
)
from model.astree.tokenizer import Token


class ParsingError(Exception):
    pass


class ProgramParser(object):
    arithmetic_operator_mapping = {
        '+': AddNode,
        '-': MinusNode,
        '*': TimesNode,
        '/': DivideNode,
    }
    comparator_mapping = {
        '<': LtNode,
        '<=': LteNode,
        '>': GtNode,
        '>=': GteNode,
        '=': EqualNode,
    }
    boolean_operator_mapping = {
        '&': AndNode,
        '|': OrNode,
    }

    def __init__(self, tokens):
        self.tokens = tokens
        self.index = 0
        self.end = len(tokens)

    def parse(self):
        self.index = 0
        self.tokens = ['{'] + self.tokens + ['}']
        self.end = len(self.tokens)
        to_return = self.parse_program()
        self.tokens = self.tokens[1:-1]
        return to_return

    def parse_program(self, previous_nodes=[], expected=[]):
        self._check_end()
        label = self._parse_label()
        current_token = self.tokens[self.index]
        self.index += 1

        if current_token == 'skip':
            current_node = SkipNode('_', label)
            return self._parse_if_expected_not_empty(
                expected, current_node, previous_nodes, self.parse_program
            )
        elif current_token == ';':
            self._check_not_empty(previous_nodes)
            left_node = previous_nodes[0]
            right_node = self.parse_program()
            current_node = SequenceNode(left_node, right_node)
            return self._parse_if_expected_not_empty(
                expected, current_node, previous_nodes, self.parse_program
            )
        elif current_token == '{':
            return self.parse_program(previous_nodes, ['}'] + expected)
        elif current_token == '}':
            return self._parse_closing_bracket(
                '}', previous_nodes, expected, self.parse_program
            )
        elif Token.is_identifier(current_token):
            if self.tokens[self.index] == ':=':
                self.index += 1
                left_node = VariableNode(current_token)
                right_node = self.parse_arithmetic()
                current_node = AssignmentNode(left_node, right_node, label)
                return self._parse_if_expected_not_empty(
                    expected, current_node, previous_nodes, self.parse_program
                )
            raise ParsingError
        elif current_token == 'while':
            label = self._parse_label()
            left_node = self.parse_boolean()
            if self.tokens[self.index] == 'do':
                self.index += 1
                right_node = self.parse_program()
                current_node = WhileNode(left_node, right_node, label)
                return self._parse_if_expected_not_empty(
                    expected, current_node, previous_nodes, self.parse_program
                )
            raise ParsingError
        elif current_token == 'if':
            label = self._parse_label()
            condition_node = self.parse_boolean()

            if self.tokens[self.index] == 'then':
                self.index += 1
                then_node = self.parse_program()
            else:
                raise ParsingError

            if self.tokens[self.index] == 'else':
                self.index += 1
                else_node = self.parse_program()
            else:
                raise ParsingError

            current_node = IfNode(condition_node, then_node, else_node, label)
            return self._parse_if_expected_not_empty(
                expected, current_node, previous_nodes, self.parse_program
            )
        raise ParsingError

    def parse_arithmetic(self, previous_nodes=[], expected=[]):
        self._check_end()
        current_token = self.tokens[self.index]
        self.index += 1

        if type(current_token) == int:
            current_node = NumberNode(current_token)
            return self._parse_if_expected_not_empty(
                expected, current_node, previous_nodes, self.parse_arithmetic
            )
        elif Token.is_identifier(current_token):
            current_node = VariableNode(current_token)
            return self._parse_if_expected_not_empty(
                expected, current_node, previous_nodes, self.parse_arithmetic
            )
        elif current_token == '(':
            return self.parse_arithmetic(previous_nodes, [')'] + expected)
        elif current_token == ')':
            return self._parse_closing_bracket(
                ')', previous_nodes, expected, self.parse_arithmetic
            )
        elif current_token in Token.arithmetic_operators:
            self._check_not_empty(previous_nodes)
            current_node = self.arithmetic_operator_mapping[current_token](
                previous_nodes[0], self.parse_arithmetic()
            )
            return self._parse_if_expected_not_empty(
                expected, current_node, previous_nodes, self.parse_arithmetic
            )
        raise ParsingError

    def parse_boolean(self, previous_nodes=[], expected=[]):
        try:
            current_index = self.index
            current_node = self.parse_arithmetic()

            return self.parse_boolean([current_node] + previous_nodes, expected)
        except ParsingError:
            self.index = current_index
            self._check_end()
            current_token = self.tokens[self.index]
            self.index += 1

            if current_token in Token.boolean_key_words:
                current_node = BooleanNode(current_token)
                return self._parse_if_expected_not_empty(
                    expected, current_node, previous_nodes, self.parse_boolean
                )
            elif current_token == '!':
                current_node = NotNode(self.parse_boolean(previous_nodes, expected))
                return self._parse_if_expected_not_empty(
                    expected, current_node, previous_nodes, self.parse_boolean
                )
            elif current_token == '(':
                return self.parse_boolean(previous_nodes, [')'] + expected)
            elif current_token == ')':
                return self._parse_closing_bracket(
                    ')', previous_nodes, expected, self.parse_boolean
                )
            elif current_token in Token.comparators:
                self._check_not_empty(previous_nodes)
                left_node = previous_nodes[0]
                if left_node.is_arithmetic():
                    right_node = self.parse_arithmetic(previous_nodes[1:])
                    current_node = self.comparator_mapping[current_token](
                        left_node, right_node
                    )
                    return self._parse_if_expected_not_empty(
                        expected, current_node, previous_nodes, self.parse_boolean
                    )
                raise ParsingError
            elif current_token in Token.boolean_operators:
                self._check_not_empty(previous_nodes)
                left_node = previous_nodes[0]
                if left_node.is_boolean():
                    right_node = self.parse_boolean(previous_nodes[1:])
                    current_node = self.boolean_operator_mapping[current_token](
                        left_node, right_node
                    )
                    return self._parse_if_expected_not_empty(
                        expected, current_node, previous_nodes, self.parse_boolean
                    )
                raise ParsingError
            raise ParsingError

    def _check_end(self):
        if self.index == self.end:
            raise ParsingError

    def _check_not_empty(self, to_check):
        if to_check == []:
            raise ParsingError

    def _parse_if_expected_not_empty(self, expected, current_node, previous_nodes, parsing_func):
        if expected == []:
            return current_node
        return parsing_func([current_node] + previous_nodes, expected)

    def _parse_closing_bracket(self, bracket, previous_nodes, expected, parsing_func):
        if expected == [] or previous_nodes == []:
            raise ParsingError
        elif expected[0] == bracket:
            if len(expected) == 1:
                return previous_nodes[0]
            else:
                return parsing_func(previous_nodes, expected[1:])
        raise ParsingError

    def _parse_label(self):
        label = self.tokens[self.index]
        if not Token.is_number(label):
            return None
        self.index += 1
        if not self.tokens[self.index] == ':':
            raise ParsingError
        self.index += 1
        return label
