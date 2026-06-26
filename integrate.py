from expressions import *

def integrate(expr : Expr , var) -> Expr: 
    match expr:
        case Const(_):
            return Mul((expr,Var(var)))
        
        case Var(v):
            if(v == var):
                return Mul((Pow(expr,Const(2)),Pow(Const(2),Const(-1))))
            return expr
        
        case Neg(x): 
            return Neg(integrate(x, var))
            
        case Pow(Var(v),Const(c)):
            if(v == var):
                if(c == -1):
                    return Log(Var(v))
                return Mul((Pow(Var(v),Const(c+1)),Pow(Const(c+1),Const(-1))))
            return expr
            
        case Add(args):
            return Add(tuple(integrate(a, var) for a in args))
        
        case Sin(x): 
            return Neg(Cos(x))
        
        case Cos(x): 
            return Sin(x)

        case Exp(x): 
            return Exp(x)

        
        case _:
            raise ValueError("nothing here")
        