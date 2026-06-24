from expressions import *

def integrate(expr : Expr , var) -> Expr: 
    match expr:
        case Const(_):
            return Mul(expr,Var(var))
        
        case Var(v):
            if(v == var):
                return Div(Pow(expr,Const(2)),Const(2))
            return expr
        
        case Neg(x): 
            return Neg(integrate(x, var))
            
        case Pow(Var(v),Const(c)):
            if(v == var):
                if(c == -1):
                    return Log(Var(v))
                return Div(Pow(Var(v),Const(c+1)),Const(c+1))
            return expr
            
        case Add(l, r):
            return Add(integrate(l, var),integrate(r, var))
        
        case Sub(l, r):
            return Sub(integrate(l, var),integrate(r, var))
        
        case Mul(Const(c),x) | Mul(x,Const(c)):
            return Mul(Const(c),integrate(x, var))
        
        case Sin(x): 
            return Neg(Cos(x))
        
        case Cos(x): 
            return Sin(x)

        case Exp(x): 
            return Exp(x)

        
        case _:
            raise ValueError("nothing here")
        