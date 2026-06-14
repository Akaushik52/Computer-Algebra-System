from tokeniser import tokenise
from parser import Parser
from simplify import simplify
from differentiate import differentiate

diff_tests = [
    ("x^2", "x"),
    ("sin(x^2)", "x"),
    ("e^(2*x)", "x"),
    ("log(sin(x))", "x"),
    ("x^x", "x"),
    ("tan(x)/x", "x"),
    ("sin(x)*cos(x)", "x"),
]


for test in diff_tests:
    print(simplify(differentiate((Parser(tokenise(test[0]))).parse(), "x")))
    