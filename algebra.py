from expressions import *

def free_variables(expr: Expr) -> set:
    match expr:
        case Var(v):
            return {v}
        
        case Const(_):
            return set()
        
        case Neg(x) | Sin(x) | Cos(x) | Tan(x) | Cot(x) | Sec(x) | Csc(x) | Exp(x) | Log(x):
            return free_variables(x)
        
        case Add(l, r) | Sub(l, r) | Mul(l, r) | Div(l, r) | Pow(l, r):
            return free_variables(l) | free_variables(r)
        
        case _:
            return set()

def is_constant(expr: Expr, var):
    return var not in free_variables(expr)

def substitute(expr, old, new) -> Expr:
    match expr:
        case _ if expr == old:
            return new
        
        case Const(_) | Var(_):
            return expr
        
        case Neg(x) | Sin(x) | Cos(x) | Tan(x) | Cot(x) | Sec(x) | Csc(x) | Exp(x) | Log(x):
            return type(expr)(substitute(x, old, new))
        
        case Add(l, r) | Sub(l, r) | Mul(l, r) | Div(l, r) | Pow(l, r):
            return type(expr)(substitute(l, old, new), substitute(r, old, new))
        
        case _:
            return expr        


from tokeniser import tokenise
from parser import Parser

ast = Parser(tokenise("sin(x) + x^2")).parse()
x   = Var("x")
u   = Var("u")
print(substitute(ast, x, u))   # should give sin(u)+u^2
        