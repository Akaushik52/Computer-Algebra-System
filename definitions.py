from expressions import *

END = "END"

NUMBER = "NUMBER"
IDENTIFIER = "IDENTIFIER"

PLUS = "PLUS"
MINUS = "MINUS"
MUL = "MUL"
DIV = "DIV"
POW = "POW"

LPAREN = "LPAREN"
RPAREN = "RPAREN"

OPERATORS = {
    "+": PLUS,
    "-": MINUS,
    "*": MUL,
    "/": DIV,
    "^": POW,
    "(": LPAREN,
    ")": RPAREN,
}

FUNCTION_MAP ={
    "sin": Sin,
    "cos": Cos,
    "tan": Tan,
    "cot": Cot,
    "sec": Sec,
    "cosec": Csc,
    "exp": Exp,
    "log": Log
}

E = 2.718281828459045
PI = 3.141592653589793