from dataclasses import dataclass

class Expr:
    def __str__(self):
        return self.simple()
    
    def simple(self):
        raise NotImplementedError
    
    def latex(self):
        raise NotImplementedError

@dataclass(frozen=True)
class Var(Expr):
    name : str

    def simple(self):
        return self.name
    
    def latex(self):
        return self.name

@dataclass(frozen=True)
class Const(Expr):
    value : float

    def simple(self):
        return str(self.value)
    
    def latex(self):
        return str(self.value)
    
@dataclass(frozen=True)
class Neg(Expr):
    inp : Expr

    def simple(self):
        return f"-{self.inp}"
    
    def latex(self):
        return f"-{self.inp.latex()}"

@dataclass(frozen=True)
class Add(Expr):
    args: tuple

    def simple(self):
        return f"({'+'.join(str(a) for a in self.args)})"
    
    def latex(self):
        return f"\\left({'+'.join(a.latex() for a in self.args)}\\right)"

@dataclass(frozen=True)
class Mul(Expr):
    args: tuple

    def simple(self):
        return f"({"*".join(str(a) for a in self.args)})"
    
    def latex(self):
        return f"{"\\cdot ".join(a.latex() for a in self.args)}"

# @dataclass(frozen=True)
# class Sub(Expr):
#     first : Expr
#     second : Expr

#     def simple(self):
#         return f"({self.first}-{self.second})"
    
#     def latex(self):
#         return f"\\left({self.first.latex()}-{self.second.latex()}\\right)"
    
# @dataclass(frozen=True)
# class Div(Expr):
#     first : Expr
#     second : Expr

#     def simple(self):
#         return f"({self.first}/{self.second})"
    
#     def latex(self):
#         return f"\\frac{{{self.first.latex()}}}{{{self.second.latex()}}}"

@dataclass(frozen=True)
class Pow(Expr):
    first : Expr
    second : Expr
    
    def simple(self):
        return f"({self.first}^{self.second})"
    
    def latex(self):
        base = self.first.latex()
        if isinstance(self.first, (Var, Const, E, Pi)):
            return f"{base}^{{{self.second.latex()}}}"
        return f"\\left({base}\\right)^{{{self.second.latex()}}}"

@dataclass(frozen=True)
class Sin(Expr):
    inp : Expr

    def simple(self):
        return f"sin({self.inp})"

    def latex(self):
        return f"\\sin\\left({self.inp.latex()}\\right)"

@dataclass(frozen=True)
class Cos(Expr):
    inp : Expr

    def simple(self):
        return f"cos({self.inp})"

    def latex(self):
        return f"\\cos\\left({self.inp.latex()}\\right)"

@dataclass(frozen=True)
class Tan(Expr):
    inp : Expr

    def simple(self):
        return f"tan({self.inp})"

    def latex(self):
        return f"\\tan\\left({self.inp.latex()}\\right)"

@dataclass(frozen=True)
class Cot(Expr):
    inp : Expr

    def simple(self):
        return f"cot({self.inp})"

    def latex(self):
        return f"\\cot\\left({self.inp.latex()}\\right)"

@dataclass(frozen=True)
class Sec(Expr):
    inp : Expr

    def simple(self):
        return f"sec({self.inp})"

    def latex(self):
        return f"\\sec\\left({self.inp.latex()}\\right)"

@dataclass(frozen=True)
class Csc(Expr):
    inp : Expr

    def simple(self):
        return f"cosec({self.inp})"

    def latex(self):
        return f"\\csc\\left({self.inp.latex()}\\right)"

@dataclass(frozen=True)
class Exp(Expr):
    inp : Expr

    def simple(self):
        return f"exp({self.inp})"

    def latex(self):
        return f"e^{{{self.inp.latex()}}}"

@dataclass(frozen=True)
class Log(Expr):
    inp : Expr

    def simple(self):
        return f"log({self.inp})"

    def latex(self):
        return f"\\log\\left({self.inp.latex()}\\right)"
    
@dataclass(frozen=True)
class Pi(Expr):
    def simple(self):
        return "pi"
    
    def latex(self): 
        return "\\pi"

@dataclass(frozen=True)
class E(Expr):
    def simple(self):
        return "e"

    def latex(self): 
        return "e"