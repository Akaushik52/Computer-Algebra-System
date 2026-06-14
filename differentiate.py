from expressions import *

def differentiate(expr : Expr, var) -> Expr:
    match expr:
        case Const(_):
            return  Const(0)
        
        case Var(x):
            if(x == var):
                return Const(1)
            return Const(0)
        
        case Neg(x):
            return Neg(differentiate(x, var))
        
        case Add(f,g):
            return Add(differentiate(f,var),differentiate(g,var))
        
        case Sub(f,g):
            return Sub(differentiate(f, var),differentiate(g,var))
        
        case Mul(f,g):
            return Add(Mul(f,differentiate(g,var)),Mul(differentiate(f,var),g))
        
        case Div(f, g):
            return Div(Sub(Mul(differentiate(f,var), g), Mul(f, differentiate(g,var))), Pow(g, Const(2)))
        
        case Pow(f, g):
            df = differentiate(f, var)
            dg = differentiate(g, var)

            match (f, g):
                case(_, Const(_)):
                    return Mul(Mul(g,Pow(f,Sub(g,Const(1)))),df)
        
                case(Const(_), _):
                    return Mul(Mul(Pow(f, g), Log(f)), dg)
                
                case _:
                    return Mul(Pow(f, g), Add(Mul(dg, Log(f)), Mul(g, Div(df, f))))

        case Sin(x):
            return Mul(Cos(x),differentiate(x,var))
        
        case Cos(x):
            return Neg(Mul(Sin(x),differentiate(x,var)))
        
        case Tan(x):
            return Mul(Pow(Sec(x),Const(2)),differentiate(x,var))
        
        case Cot(x):
            return Neg(Mul(Pow(Csc(x),Const(2)),differentiate(x, var)))
        
        case Sec(x):
            return Mul(Mul(Sec(x),Tan(x)),differentiate(x,var))
        
        case Csc(x):
            return Neg(Mul(Mul(Csc(x),Cot(x)),differentiate(x,var)))
        
        case Exp(x):
            return Mul(Exp(x),differentiate(x, var))
        
        case Log(x):
            return Mul(Div(Const(1), x),differentiate(x, var))

        case _:
            raise ValueError(f"Can't differentiate: {expr}")
        
        