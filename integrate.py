from expressions import *
from algebra import is_constant
from simplify import simplify
from evaluate import evaluate


def _get_ratio(rest_expr, d, var):
    ratio = simplify(Mul((rest_expr, Pow(d, Const(-1)))))
    if is_constant(ratio, var):
        return ratio
    try:
        env1 = {var: 2.0}
        env2 = {var: 3.0}
        r1 = evaluate(rest_expr, env1) / evaluate(d, env1)
        r2 = evaluate(rest_expr, env2) / evaluate(d, env2)
        if abs(r1 - r2) < 1e-10:
            return Const(r1)
    except:
        pass
    return None


def integrate(expr: Expr, var: str) -> Expr:
    match expr:
        case Const(_):
            return Mul((expr, Var(var)))

        case Var(v):
            if v == var:
                return Mul((Pow(Var(var), Const(2)), Pow(Const(2), Const(-1))))
            return Mul((expr, Var(var)))

        case Neg(x):
            return Neg(integrate(x, var))

        case Add(args=args):
            return Add(tuple(integrate(a, var) for a in args))

        case Mul(args=args):
            consts = [a for a in args if is_constant(a, var)]
            rest   = [a for a in args if not is_constant(a, var)]
            if consts:
                c = Mul(tuple(consts)) if len(consts) > 1 else consts[0]
                if not rest:
                    return Mul((c, Var(var)))
                integrand = rest[0] if len(rest) == 1 else Mul(tuple(rest))
                return simplify(Mul((c, integrate(integrand, var))))
            return _integrate_mul(args, var)

        case Pow(Var(v), Neg(Const(c))):
            if v == var:
                nc = -c
                if nc == -1 or nc == -1.0:
                    return Log(Var(v))
                return Mul((Pow(Var(v), Const(nc + 1)), Pow(Const(nc + 1), Const(-1))))
            return Mul((expr, Var(var)))

        case Pow(Var(v), Const(c)):
            if v == var:
                if c == -1 or c == -1.0:
                    return Log(Var(v))
                return Mul((Pow(Var(v), Const(c + 1)), Pow(Const(c + 1), Const(-1))))
            return Mul((expr, Var(var)))

        case Sin(x):
            return _integrate_trig(Sin, Neg(Cos(x)), x, var)

        case Cos(x):
            return _integrate_trig(Cos, Sin(x), x, var)

        case Exp(x):
            return _integrate_trig(Exp, Exp(x), x, var)
        
        case Log(x):
            if x == Var(var):
                return simplify(Add((Mul((Var(var), Log(Var(var)))), Neg(Var(var)))))
            raise ValueError(f"Can't integrate log({x})")

        case _:
            return Integral(expr, var)


def _integrate_trig(node, result, inner, var):
    from differentiate import differentiate
    d = simplify(differentiate(inner, var))
    if is_constant(d, var):
        if d == Const(1):
            return result
        return simplify(Mul((result, Pow(d, Const(-1)))))
    return Integral(node(inner), var)

def _integrate_mul(args, var):
    from differentiate import differentiate
    args = list(args)

    for i, f in enumerate(args):
        rest = [args[j] for j in range(len(args)) if j != i]
        rest_expr = rest[0] if len(rest) == 1 else Mul(tuple(rest))
        match f:
            case Sin(inner):
                d_sin = simplify(differentiate(Sin(inner), var))
                ratio = _get_ratio(rest_expr, d_sin, var)
                if ratio is not None:
                    return simplify(Mul((ratio, Mul((Pow(Sin(inner), Const(2)), Pow(Const(2), Const(-1)))))))
                d = simplify(differentiate(inner, var))
                ratio = _get_ratio(rest_expr, d, var)
                if ratio is not None:
                    return simplify(Mul((ratio, Neg(Cos(inner)))))
    
            case Cos(inner):
                d_cos = simplify(differentiate(Cos(inner), var))
                ratio = _get_ratio(rest_expr, d_cos, var)
                if ratio is not None:
                    return simplify(Mul((ratio, Mul((Pow(Cos(inner), Const(2)), Pow(Const(2), Const(-1)))))))
                d = simplify(differentiate(inner, var))
                ratio = _get_ratio(rest_expr, d, var)
                if ratio is not None:
                    return simplify(Mul((ratio, Sin(inner))))
                
            case Exp(inner):
                d = simplify(differentiate(inner, var))
                ratio = _get_ratio(rest_expr, d, var)
                if ratio is not None:
                    return simplify(Mul((ratio, Exp(inner))))
                
            case Pow(inner, Const(n)):
                d = simplify(differentiate(inner, var))
                ratio = _get_ratio(rest_expr, d, var)
                if ratio is not None:
                    if n == -1:
                        return simplify(Mul((ratio, Log(inner))))
                    return simplify(Mul((ratio, Mul((Pow(inner, Const(n + 1)), Pow(Const(n + 1), Const(-1)))))))
            case _:
                pass

    original = Mul(tuple(args))
    _PARTS_ORDER = (Pow, Var, Log, Sin, Cos, Exp)
    args_sorted = sorted(args, key=lambda a: next(
        (i for i, t in enumerate(_PARTS_ORDER) if isinstance(a, t)), len(_PARTS_ORDER)
    ))
    u = args_sorted[0]
    dv_args = args_sorted[1:]
    dv = dv_args[0] if len(dv_args) == 1 else Mul(tuple(dv_args))
    du = simplify(differentiate(u, var))
    try:
        v = integrate(dv, var)
        v_du = simplify(Mul((v, du)))
        if v_du == original:
            return Integral(original, var)
        result = integrate(v_du, var)
        if isinstance(result, Integral):
            return Integral(original, var)
        return simplify(Add((Mul((u, v)), Neg(result))))
    except:
        return Integral(original, var)