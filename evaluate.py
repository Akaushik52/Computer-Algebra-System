from expressions import *
import math

def accurate(expr, env):
    return round(evaluate(expr,env))

def evaluate(expr, env) -> float:
    match expr:
        case Var(x):
            if x in env:
                return env[x]
            else:
                raise ValueError(f"No value provided for {x}")
            
        case Const(c):
            return c
        
        case Neg(x):
            return -1 * evaluate(x, env)
        
        case Add(l, r):
            return evaluate(l, env) + evaluate(r, env)

        case Sub(l, r):
            return evaluate(l, env) - evaluate(r, env)
        
        case Mul(l,r):
            return evaluate(l, env) * evaluate(r, env)

        case Div(l, r):
            return evaluate(l,env) / evaluate(r,env)
        
        case Pow(l,r):
            return evaluate(l, env) ** evaluate(r, env)
        
        case Sin(i):
            return math.sin(evaluate(i,env))
        
        case Cos(i):
            return math.cos(evaluate(i,env))
        
        case Tan(i):
            return math.tan(evaluate(i,env))
        
        case Cot(i):
            return 1 / math.tan(evaluate(i,env))
        
        case Sec(i):
            return 1 / math.cos(evaluate(i,env))
        
        case Csc(i):
            return 1 / math.sin(evaluate(i,env))
        
        case Exp(i):
            return math.exp(evaluate(i,env))
        
        case Log(i):
            return math.log(evaluate(i,env))

        case _:
            raise NotImplementedError(f"Don't know how to evaluate {expr}")