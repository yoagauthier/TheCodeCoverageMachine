from model.astree.nodes import (
    AddNode,
    MinusNode,
    TimesNode,
    DivideNode,
    NumberNode,
    VariableNode,
)
from model.astree.tokenizer import Token


class ParsingError(Exception):
    pass


class ProgramParser(object):
    index = 0
    end = 0

    arithmetic_operator_mapping = {
        '+': AddNode,
        '-': MinusNode,
        '*': TimesNode,
        '/': DivideNode,
    }

    @staticmethod
    def parse(tokens):
        ProgramParser.index = 0
        ProgramParser.end = len(tokens) + 2
        ProgramParser.parse_program(['{'] + tokens + ['}'])

    @staticmethod
    def parse_program(tokens, previous_nodes=[], expected=[]):
        pass

    @staticmethod
    def parse_arithmetic(tokens, previous_nodes=[], expected=[]):
        if ProgramParser.index == ProgramParser.end:
            raise ParsingError

        current_token = tokens[ProgramParser.index]

        if type(current_token) == int:
            ProgramParser.index += 1
            current_node = NumberNode(current_token)
            if expected == []:
                return current_node
            else:
                return ProgramParser.parse_arithmetic(
                    tokens,
                    previous_nodes=[current_node] + previous_nodes,
                    expected=expected
                )
        elif Token.is_identifier(current_token):
            ProgramParser.index += 1
            current_node = VariableNode(current_token)
            if expected == []:
                return current_node
            else:
                return ProgramParser.parse_arithmetic(
                    tokens,
                    previous_nodes=[current_node] + previous_nodes,
                    expected=expected
                )
        elif current_token == '(':
            ProgramParser.index += 1
            return ProgramParser.parse_arithmetic(tokens, previous_nodes, [')'] + expected)
        elif current_token == ')':
            if expected == []:
                raise ParsingError
            elif expected[0] == ')':
                ProgramParser.index += 1
                if len(expected) == 1:
                    return previous_nodes[0]
                else:
                    return ProgramParser.parse_arithmetic(tokens, expected=expected[1:])
            else:
                raise ParsingError
        elif current_token in Token.arithmetic_operators:
            if previous_nodes == []:
                raise ParsingError
            else:
                ProgramParser.index += 1
                left_node = previous_nodes[0]
                right_node = ProgramParser.parse_arithmetic(tokens)
                current_node = ProgramParser.arithmetic_operator_mapping[current_token](
                    left_node,
                    right_node
                )
                if expected == []:
                    return current_node
                else:
                    return ProgramParser.parse_arithmetic(
                        tokens,
                        previous_nodes=[current_node] + previous_nodes[1:],
                        expected=expected
                    )
        else:
            raise ParsingError

    @staticmethod
    def parse_boolean(tokens, previous_nodes=[], expected=[]):
        pass
