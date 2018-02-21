"""
Autors: Yoann Gauthier and Thibaut Seys
Date: 21/02/2018

This file defines all custom exceptions needed in our project.
"""


class ParsingError(Exception):
    """Raised when the program does not respect the defined grammar."""
    pass


class ExecutionError(Exception):
    """Raised when the program gets an error while trying to eval."""
    pass
