"""
Autors: Yoann Gauthier and Thibaut Seys
Date: 21/02/2018

This file defines all the logic for the abstract syntax tree.
"""
from model.error import ParsingError
from model.parser import ProgramParser
from model.tokenizer import Token, Tokenizer


class ASTree(object):
    """This class defines an abstract syntax tree"""

    def __init__(self, file_path):
        """Create the abstract syntax tree from the given filepath"""
        # Loading raw content from file path
        self.program_file_path = file_path

        with open(file_path, 'r') as program_file:
            self.raw_program = program_file.read()

        # Clearing raw content from comments, ' ' and \t
        self.cleared_program = '\n'.join(Tokenizer.clear(self.raw_program.strip().split('\n')))

        # Tokenize program
        self.tokenized_program = Tokenizer.tokenize(self.cleared_program)
        if not self.is_well_formed():
            raise ParsingError

        # Parse program
        self.root_node = ProgramParser(self.tokenized_program).parse()
        if not (self.root_node.is_program() and self.root_node.is_well_labelled()):
            raise ParsingError

    def is_well_formed(self):
        """This function checks if the tokenized program opens and closes its brackets the correct
        way"""
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
        """Returns the tree represented as a dict object."""
        return self.root_node.to_dict()

    def __str__(self):
        """String representation"""
        return self.root_node.__str__()

    def to_control_flow_graph(self):
        """Returns the cover graph from this abstract syntax tree."""
        control_flow_graph = self.root_node.to_control_flow_graph()
        control_flow_graph.name = self.program_file_path
        return control_flow_graph

    def eval(self, env={}):
        """Evaluate the program from the given environment input."""
        return self.root_node.eval(env)
