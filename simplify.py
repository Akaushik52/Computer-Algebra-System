from expressions import *
from evaluate import accurate

def fold(node, x):
    x = simplify(x)
    if isinstance(x, (Const, Pi)):
        return Const(accurate(node(x), {}))
    return node(x)


def simplify(expr : Expr) -> Expr:
    match expr:
        case Var(_) | Const(_) | E() | Pi():
            return expr
        
        case Neg(x):
            x = simplify(x)
            match x:
                case Neg(a):
                    return a
                case Const(a):
                    return Const(-a)
                case _:
                    return Neg(x)
                
        case Add(l, r):
            l = simplify(l)
            r = simplify(r)
            match (l, r):
                case (Const(0), _):
                    return r
                case (_, Const(0)):
                    return l
                case (Const(a), Const(b)):
                    return Const(a + b)
                case _:
                    return Add(l, r)

        case Sub(l, r):
            l = simplify(l)
            r = simplify(r)
            
            if(l == r):
                return Const(0)
            
            match (l, r):
                case (Const(a), Const(b)):
                    return Const(a - b)
                case (Const(0), _):
                    return Neg(r)
                case (_, Const(0)):
                    return l
                case _:
                    return Sub(l, r)
                    
        case Mul(l, r):
            l = simplify(l)
            r = simplify(r)
            match (l, r):
                case (Const(a), Const(b)):
                    return Const(a*b)
                case (Const(1), _):
                    return r
                case (_, Const(1)):
                    return l
                case (Const(0), _):
                    return Const(0)
                case (_, Const(0)):
                    return Const(0)
                case (_, Div(Const(1), b)) if l == b:
                    return Const(1)
                case (Div(Const(1), b), _) if r == b:
                    return Const(1)
                case (Neg(a), Neg(b)):
                    return simplify(Mul(a, b))
                case (_, Neg(b)):
                    return simplify(Neg(Mul(l, b)))
                case (Neg(a), _):
                    return simplify(Neg(Mul(a, r)))
                case _:
                    return Mul(l, r)
                
        case Div(l, r):
            l = simplify(l)
            r = simplify(r)
            
            if(l == r):
                return Const(1)
            
            match (l, r):
                case (Const(a), Const(b)):
                    return Const(a / b)
                case (_, Const(1)):
                    return l
                case (Const(0), _):
                    return Const(0)
                case _:
                    return Div(l, r)
                
        case Pow(l,r):
            l = simplify(l)
            r = simplify(r)

            match (l, r):
                case (Const(a), Const(b)):
                    return Const(a ** b)
                case (_ , Const(1)):
                    return l
                case (_ , Const(0)):
                    return Const(1)
                case (Const(1), _):
                    return Const(1)
                case(Const(0), _):
                    return Const(0)
                case _:
                    return Pow(l, r)
                
        case Sin(x):
            x = simplify(x)
            if isinstance(x, Neg):
                return Neg(Sin(x.inp))
            return fold(Sin, x)
                
        case Cos(x):
            x = simplify(x)
            if isinstance(x, Neg):
                return Cos(x.inp)
            return fold(Cos, x)
                
        case Tan(x):
            x = simplify(x)
            if isinstance(x, Neg):
                return Neg(Tan(x.inp))
            return fold(Tan, x)
                
        case Cot(x):
            x = simplify(x)
            if isinstance(x, Neg):
                return Cot(x.inp)
            return fold(Cot, x)
                
        case Sec(x):
            x = simplify(x)
            if isinstance(x, Neg):
                return Sec(x.inp)
            return fold(Sec, x)
                
        case Csc(x):
            x = simplify(x)
            if isinstance(x, Neg):
                return Neg(Csc(x.inp))
            return fold(Csc, x)
                
        case Exp(x):
            x = simplify(x)
            if isinstance(x, Log):
                return x.inp
            return fold(Exp, x)
                
        case Log(x):
            x = simplify(x)
            if isinstance(x, E):
                return Const(1)
            if isinstance(x, Exp):
                return x.inp
            return fold(Log, x)

        case _:
            raise NotImplementedError(f"Can't simplify {expr}")