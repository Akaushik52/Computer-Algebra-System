from dataclasses import dataclass

class Expr:
    def __str__(self):
        return self.simple()
    
    def simple(self):
        raise NotImplementedError
    
    def __add__(self,other):
        return Add(self,other)
    
    def __sub__(self, other):
        return Sub(self,other)

    def __mul__(self, other):
        return Mul(self,other)
    
    def __truediv__(self, other):
        return Div(self,other)
    
    def __pow__(self, other):
        return Pow(self,other)

@dataclass(frozen=True)
class Var(Expr):
    name : str

    def simple(self):
        return self.name

@dataclass(frozen=True)
class Const(Expr):
    value : float

    def simple(self):
        return str(self.value)
    
@dataclass(frozen=True)
class Neg(Expr):
    inp : Expr

    def simple(self):
        return f"-{self.inp}" 

@dataclass(frozen=True)
class Add(Expr):
    first : Expr
    second : Expr

    def simple(self):
        return f"({self.first}+{self.second})"

@dataclass(frozen=True)
class Sub(Expr):
    first : Expr
    second : Expr

    def simple(self):
        return f"({self.first}-{self.second})"

@dataclass(frozen=True)
class Mul(Expr):
    first : Expr
    second : Expr
    
    def simple(self):
        return f"({self.first}*{self.second})"

@dataclass(frozen=True)
class Div(Expr):
    first : Expr
    second : Expr

    def simple(self):
        return f"({self.first}/{self.second})"

@dataclass(frozen=True)
class Pow(Expr):
    first : Expr
    second : Expr
    
    def simple(self):
        return f"({self.first}^{self.second})"

@dataclass(frozen=True)
class Sin(Expr):
    inp : Expr

    def simple(self):
        return f"sin({self.inp})"

@dataclass(frozen=True)
class Cos(Expr):
    inp : Expr

    def simple(self):
        return f"cos({self.inp})"

@dataclass(frozen=True)
class Tan(Expr):
    inp : Expr

    def simple(self):
        return f"tan({self.inp})"

@dataclass(frozen=True)
class Cot(Expr):
    inp : Expr

    def simple(self):
        return f"cot({self.inp})"

@dataclass(frozen=True)
class Sec(Expr):
    inp : Expr

    def simple(self):
        return f"sec({self.inp})"

@dataclass(frozen=True)
class Csc(Expr):
    inp : Expr

    def simple(self):
        return f"cosec({self.inp})"

@dataclass(frozen=True)
class Exp(Expr):
    inp : Expr

    def simple(self):
        return f"exp({self.inp})"

@dataclass(frozen=True)
class Log(Expr):
    inp : Expr

    def simple(self):
        return f"log({self.inp})"
