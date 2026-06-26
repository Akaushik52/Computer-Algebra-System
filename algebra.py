from expressions import *

def free_variables(expr: Expr) -> set:
    match expr:
        case Var(v):
            return {v}
        
        case Const(_):
            return set()
        
        case Neg(x) | Sin(x) | Cos(x) | Tan(x) | Cot(x) | Sec(x) | Csc(x) | Exp(x) | Log(x):
            return free_variables(x)
        
        case Pow(l, r):
            return free_variables(l) | free_variables(r)
        
        case Add(args) | Mul(args):
            s = set()
            for a in args:
                s |= free_variables(a)
            return s
        
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
        
        case Pow(l, r):
            return type(expr)(substitute(l, old, new), substitute(r, old, new))
        
        case Add(args) | Mul(args):
            args = [substitute(a, old, new) for a in args]
            return type(expr)(tuple(args))
        
        case _:
            return expr        
        