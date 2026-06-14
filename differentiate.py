from expressions import *

def differentiate(expr : Expr, var) -> Expr:
    match expr:
        case Const(c):
            return  Const(0)
        
        case Var(x):
            if(x == var):
                return Const(1)
            return Const(0)
        
        case Neg(x):
            return Neg(differentiate(x, var))
        
        case Add(l,r):
            return Add(differentiate(l,var),differentiate(r,var))
        
        case Sub(l,r):
            return Sub(differentiate(l, var),differentiate(r,var))
        
        case Mul(l,r):
            return Add(Mul(l,differentiate(r,var)),Mul(differentiate(l,var),r))
        
        case Div(f, g):
            return Div(Sub(Mul(differentiate(f,var), g), Mul(f, differentiate(g,var))), Pow(g, Const(2)))
        
        case _:
            raise ValueError("dammmm")
        
        