class Tokenizer(object):
    @staticmethod
    def clear(text_lines):
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
        tokenized_text = []
        current_token = ''

        for char in text:
            if len(current_token) == 1 and current_token in ':<>':
                if char != '=':
                    tokenized_text.append(current_token)
                    current_token = char
                else:
                    current_token += char
                    tokenized_text.append(current_token)
                    current_token = ''
                continue

            if char == ' ' or char == '\n':
                if len(current_token) > 0:
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
    def is_identifier(char):
        return char.isalpha() and char not in Token.key_words

    @staticmethod
    def opposite_bracket(char):
        if char == '(':
            return ')'
        elif char == ')':
            return '('
        elif char == '{':
            return '}'
        elif char == '}':
            return '{'
        else:
            return 'Not a bracket'

    @staticmethod
    def is_opening_bracket(char):
        return char in Token.opening_brackets

    @staticmethod
    def is_closing_bracket(char):
        return char in Token.closing_brackets

    @staticmethod
    def number(char):
        try:
            return int(char)
        except ValueError:
            return char
