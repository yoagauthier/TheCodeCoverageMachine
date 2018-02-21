"""
Autors: Yoann Gautier and Thibaut Seys
Date: 21/02/2018

This file defines the Tokenizer class which is used to tokenized a given source code. The Token
class defines the Token class as well which contains some control functions for token.
"""


class Tokenizer(object):
    @staticmethod
    def clear(text_lines):
        """This method clear comments, spaces and tabulations from raw code"""
        if text_lines == []:
            return []
        elif text_lines[0] == '':
            return Tokenizer.clear(text_lines[1:])
        elif text_lines[0][0] == '#':
            return Tokenizer.clear(text_lines[1:])
        elif text_lines[0][0] in [' ', '\t']:
            return Tokenizer.clear([text_lines[0][1:]] + text_lines[1:])
        else:
            return [text_lines[0]] + Tokenizer.clear(text_lines[1:])

    @staticmethod
    def tokenize(text):
        """Tokenenize text from raw source code"""
        tokenized_text = []
        current_token = ''

        for char in text:
            if char == ' ' or char == '\n':
                if len(current_token) > 0:
                    tokenized_text.append(current_token)
                    current_token = ''
                continue

            if len(current_token) == 1 and current_token in ':<>':
                if char != '=':
                    tokenized_text.append(current_token)
                    current_token = char
                else:
                    current_token += char
                    tokenized_text.append(current_token)
                    current_token = ''
                continue

            if char in '!(){}-+*/&|;=':
                if len(current_token) > 0:
                    tokenized_text.append(current_token)
                    current_token = ''
                tokenized_text.append(char)
                continue

            if char in ':<>':
                if len(current_token) > 0:
                    tokenized_text.append(current_token)
                    current_token = ''
                current_token += char
                continue

            current_token += char

        tokenized_text.append(current_token) if current_token else None

        return [Token.number(token) for token in tokenized_text]


class Token(object):
    key_words = ['skip', 'if', 'else', 'then', 'while', 'do']
    symbols = [';', ':', ':=']

    arithmetic_operators = ['+', '-', '*', '/', '%']

    boolean_operators = ['!', '&', '|']
    comparators = ['<', '>', '>=', '<=', '=']
    boolean_key_words = ['true', 'false']

    brackets = ['(', ')', '{', '}']
    opening_brackets = ['(', '{']
    closing_brackets = [')', '}']

    @staticmethod
    def is_identifier(token):
        """Check if token is an identifier"""
        return token.isalpha() and token not in Token.key_words

    @staticmethod
    def is_number(token):
        """Check if token is a number"""
        return type(token) == int

    @staticmethod
    def opposite_bracket(token):
        """Return opposite bracket if current token is a bracket"""
        if token == '(':
            return ')'
        elif token == ')':
            return '('
        elif token == '{':
            return '}'
        elif token == '}':
            return '{'
        else:
            return None

    @staticmethod
    def is_opening_bracket(token):
        """Return True if token is an opening bracket"""
        return token in Token.opening_brackets

    @staticmethod
    def is_closing_bracket(token):
        """Return True if token is a closing bracket"""
        return token in Token.closing_brackets

    @staticmethod
    def number(token):
        """Return token as a number if it is one else we don't change anything"""
        try:
            return int(token)
        except ValueError:
            return token
