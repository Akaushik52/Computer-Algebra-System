from tokeniser import tokenise
from parser import Parser
from simplify import simplify

tests = [
    "2 + 3 * 4",
    "(2+3)*4",
    "x + 0",
    "0 + x",
    "x * 1",
    "1 * x",
    "x * 0",
    "0 * x",
    "x - x",
    "x / x",
    "x ^ 0",
    "x ^ 1",
    "0 ^ x",
    "1 ^ x",
    "--x",
    "-(-x)",
    "0 - x",
    "(2+3)*x",
    "sin(0+x)",
]

for text in tests:
    ast = Parser(tokenise(text)).parse()
    simplified = simplify(ast)
    print(f"{text:15} -> raw: {ast}")
    print(f"{'':15}    simplified: {simplified}")
    print()