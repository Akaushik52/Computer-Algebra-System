from expressions import *
from evaluate import accurate

def fold(node, x):
    x = simplify(x)
    if isinstance(x, (Const, Pi, E)):
        return Const(accurate(node(x), {}))
    return node(x)


def simplify(expr: Expr) -> Expr:
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

        case Add(args):
            args = [simplify(a) for a in args]
            flat = []

            for a in args:
                if isinstance(a, Add):
                    flat.extend(a.args)
                else:
                    flat.append(a)

            flat = [a for a in flat if a != Const(0)]
            consts = [a for a in flat if isinstance(a, Const)]
            rest   = [a for a in flat if not isinstance(a, Const)]

            if consts:
                total = Const(sum(c.value for c in consts))
                if total != Const(0):
                    rest = [total] + rest        
            if not rest:
                return Const(0)
            if len(rest) == 1:
                return rest[0]
            return Add(tuple(rest))

        case Mul(args):
            args = [simplify(a) for a in args]

            flat = []
            for a in args:
                if isinstance(a, Mul):
                    flat.extend(a.args)
                else:
                    flat.append(a)

            if any(a == Const(0) for a in flat):
                return Const(0)

            flat = [a for a in flat if a != Const(1)]

            consts = [a for a in flat if isinstance(a, Const)]
            rest   = [a for a in flat if not isinstance(a, Const)]
            if consts:
                product = Const(1)
                for c in consts:
                    product = Const(product.value * c.value)
                if product == Const(0):
                    return Const(0)
                if product != Const(1):
                    rest = [product] + rest
            if not rest:
                return Const(1)
            if len(rest) == 1:
                return rest[0]

            neg_count = sum(1 for a in rest if isinstance(a, Neg))
            rest = [a.inp if isinstance(a, Neg) else a for a in rest]
            result = Mul(tuple(rest))
            return Neg(result) if neg_count % 2 == 1 else result

        case Pow(l, r):
            l = simplify(l)
            r = simplify(r)
            match (l, r):
                case (Const(a), Const(b)):
                    return Const(a ** b)
                case (_, Const(1)):
                    return l
                case (_, Const(0)):
                    return Const(1)
                case (Const(1), _):
                    return Const(1)
                case (Const(0), _):
                    return Const(0)
                case (_, Const(-1)):
                    return Pow(l, Const(-1)) 
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