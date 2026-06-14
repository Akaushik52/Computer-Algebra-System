from expressions import *

def simplify(expr : Expr):
    match expr:
        case Var(_) | Const(_):
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
            return Sin(simplify(x))
                
        case Cos(x):
            return Cos(simplify(x))
                
        case Tan(x):
            return Tan(simplify(x))
                
        case Cot(x):
            return Cot(simplify(x))
                
        case Sec(x):
            return Sec(simplify(x))
                
        case Csc(x):
            return Csc(simplify(x))
                
        case Exp(x):
            return Exp(simplify(x))
                
        case Log(x):
            return Log(simplify(x))

        case _:
            raise NotImplementedError(f"Can't simplify {expr}")