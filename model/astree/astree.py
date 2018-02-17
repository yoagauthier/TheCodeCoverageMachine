from model.astree.parser import ParsingError, ProgramParser
from model.astree.tokenizer import Token, Tokenizer


class ASTree(object):

    def __init__(self, file_path):
        # Loading raw content from file path
        with open(file_path, 'r') as program_file:
            self.raw_program = program_file.read()

        # Clearing raw content from comments, ' ' and \t
        self.cleared_program = '\n'.join(Tokenizer.clear(self.raw_program.strip().split('\n')))

        # Tokenize program
        self.tokenized_program = Tokenizer.tokenize(self.cleared_program)
        if not self.is_well_formed:
            raise ParsingError

        # Parse program
        self.root_node = ProgramParser(self.tokenized_program).parse()
        if not self.root_node.is_program():
            raise ParsingError

    def is_well_formed(self):
        pile = []
        for token in self.tokenized_program:
            if Token.is_opening_bracket(token):
                pile = [token] + pile
            elif Token.is_closing_bracket(token):
                if pile == []:
                    return False
                elif token == Token.opposite_bracket(pile[0]):
                    pile = pile[1:]
                else:
                    return False
        return pile == []

    def to_dict(self):
        return self.root_node.to_dict()

    def __str__(self):
        return self.root_node.__str__()
