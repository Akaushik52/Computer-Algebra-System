from expressions import *

def differentiate(expr: Expr, var) -> Expr:
    match expr:
        case Const(_) | E() | Pi():
            return Const(0)
        
        case Var(x):
            return Const(1) if x == var else Const(0)
        
        case Neg(x):
            return Neg(differentiate(x, var))
        
        case Add(args):
            return Add(tuple(differentiate(a, var) for a in args))
        
        case Mul(args):
            terms = []
            for i, f in enumerate(args):
                rest = args[:i] + args[i+1:]
                rest_mul = rest[0] if len(rest) == 1 else Mul(tuple(rest))
                terms.append(Mul((differentiate(f, var), rest_mul)))
            return Add(tuple(terms))
        
        case Pow(f, g):
            df = differentiate(f, var)
            dg = differentiate(g, var)
            match (f, g):
                case (_, Const(_)):
                    return Mul((g, Pow(f, Add((g, Neg(Const(1))))), df))
                case (Const(_), _):
                    return Mul((Pow(f, g), Log(f), dg))
                case _:
                    return Mul((Pow(f, g), Add((Mul((dg, Log(f))), Mul((g, Mul((df, Pow(f, Const(-1))))))))  ))

        case Sin(x):
            return Mul((Cos(x), differentiate(x, var)))
        
        case Cos(x):
            return Neg(Mul((Sin(x), differentiate(x, var))))
        
        case Tan(x):
            return Mul((Pow(Sec(x), Const(2)), differentiate(x, var)))
        
        case Cot(x):
            return Neg(Mul((Pow(Csc(x), Const(2)), differentiate(x, var))))
        
        case Sec(x):
            return Mul((Sec(x), Tan(x), differentiate(x, var)))
        
        case Csc(x):
            return Neg(Mul((Csc(x), Cot(x), differentiate(x, var))))
        
        case Exp(x):
            return Mul((Exp(x), differentiate(x, var)))
        
        case Log(x):
            return Mul((Pow(x, Const(-1)), differentiate(x, var)))

        case _:
            raise ValueError(f"Can't differentiate: {expr}")