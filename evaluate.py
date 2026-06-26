from expressions import *
import math

def accurate(expr, env):
    return round(evaluate(expr,env),12)

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
        
        case Add(args):
            sum = 0
            for a in args:
                sum += evaluate(a, env)
            return sum            
        
        case Mul(args):
            prod = 1
            for a in args:
                prod *= evaluate(a, env)
            return prod
        
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
        
        case E():
            return math.e
        
        case Pi():
            return math.pi  
        
        case _:
            raise NotImplementedError(f"Don't know how to evaluate {expr}")