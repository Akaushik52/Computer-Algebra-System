# Computer Algebra System

A Computer Algebra System (CAS) built from scratch in Python, supporting symbolic differentiation, integration, and simplification.

## Project Structure

```
expressions.py   - AST node classes (Const, Var, Add, Mul, Pow, Neg, Sin, Cos, ...)
definitions.py   - Token constants and function/constant maps
tokeniser.py     - tokenise(expr: str) -> list[Token]
parser.py        - Recursive descent parser: parse() -> Expr
evaluate.py      - evaluate(expr, env) -> float
simplify.py      - simplify(expr) -> Expr
differentiate.py - differentiate(expr, var) -> Expr
integrate.py     - integrate(expr, var) -> Expr
algebra.py       - free_variables, is_constant, substitute
app.py           - Entry point / REPL
```

## Usage

```python
from tokeniser import tokenise
from parser import Parser
from evaluate import evaluate
from simplify import simplify
from differentiate import differentiate
from integrate import integrate

def parse(s):
    return Parser(tokenise(s)).parse()

expr = parse("x^2 + sin(x)")

print(evaluate(expr, {"x": 2}))       # numeric evaluation
print(simplify(expr))                  # simplified form
print(simplify(differentiate(expr, "x")))   # derivative
print(simplify(integrate(expr, "x")))       # integral
```

## Grammar

```
expression := term (('+' | '-') term)*
term       := unary (('*' | '/') unary)*
unary      := '-' unary | power
power      := primary ('^' unary)?
primary    := NUMBER | IDENTIFIER | IDENTIFIER '(' expression ')' | '(' expression ')'
```

- `+ -` bind loosest, `* /` next, unary `-` next, `^` tightest (right-associative)
- An identifier followed by `(` is a function call; otherwise a variable
- `pi` and `e` are parsed as symbolic constants `Pi()` and `E()`
- Subtraction `a-b` is parsed as `Add(a, Neg(b))`
- Division `a/b` is parsed as `Mul(a, Pow(b, -1))`

## Expression Tree

All expressions are immutable frozen dataclasses inheriting from `Expr`.

| Node | Fields | Notes |
|------|--------|-------|
| `Const(value)` | `float` | Numeric constant |
| `Var(name)` | `str` | Variable |
| `Neg(inp)` | `Expr` | Unary negation |
| `Add(args)` | `tuple[Expr, ...]` | N-ary addition |
| `Mul(args)` | `tuple[Expr, ...]` | N-ary multiplication |
| `Pow(first, second)` | `Expr, Expr` | Exponentiation |
| `Sin, Cos, Tan, Cot, Sec, Csc, Exp, Log` | `inp: Expr` | Unary functions |
| `Pi, E` | — | Symbolic constants |
| `Integral(inp, var)` | `Expr, str` | Unevaluated integral |

## Simplification Rules

- **Identity elements:** `x+0`, `x*1`, `x^1`, `x^0 -> 1`, `0*x -> 0`
- **Constant folding:** `Const(a) op Const(b)` for `+ * ^`
- **N-ary flattening:** nested `Add`/`Mul` trees are flattened
- **Collect like terms:** `2*x + 3*x -> 5*x`
- **Power rules:** `x*x -> x^2`, `x^a * x^b -> x^(a+b)`, `(x^a)^b -> x^(a*b)`, `x * x^-1 -> 1`
- **Neg rules:** `-(-x) -> x`, `(-a)*(-b) -> a*b`
- **Trig parity:** `sin(-x) -> -sin(x)`, `cos(-x) -> cos(x)`
- **Exp/log inverses:** `exp(log(x)) -> x`, `log(exp(x)) -> x`, `log(e) -> 1`

## Differentiation Rules

| Expression | Rule |
|------------|------|
| `Const` | `0` |
| `Var(x)` | `1` if `x == var`, else `0` |
| `Neg(f)` | `-f'` |
| `Add(f, g, ...)` | `f' + g' + ...` |
| `Mul(f, g, ...)` | Generalized product rule |
| `Pow(f, g)` | Power rule / exponential rule / logarithmic differentiation |
| `Sin, Cos, Tan, Cot, Sec, Csc, Exp, Log` | Chain rule |

## Integration

Integration returns a symbolic antiderivative where possible, or `∫f(x)dx` if the integral cannot be found.

| Pattern | Result |
|---------|--------|
| `Const` | `c*x` |
| `x^n` | `x^(n+1)/(n+1)` |
| `x^-1` | `log(x)` |
| `sin(x)`, `cos(x)`, `exp(x)` | Standard antiderivatives |
| `sin(ax+b)` | `-cos(ax+b)/a` (linear inner function) |
| `c*f(x)` | `c * ∫f(x)dx` (constant extraction) |
| `f'(x)*g(f(x))` | Reverse chain rule |
| `sin(x)*cos(x)` | `sin²(x)/2` |
| `x*sin(x)`, `x*exp(x)` | Integration by parts |
| `log(x)` | `x*log(x) - x` |
| Everything else | `∫f(x)dx` (unevaluated) |

## Algebra Utilities (`algebra.py`)

```python
free_variables(expr)        # set of variable names in expr
is_constant(expr, var)      # True if expr doesn't contain var
substitute(expr, old, new)  # replace old subexpression with new
```

## Known Limitations

- No `sin²(x)`, `cos²(x)` trig identity rewrites yet
- No inverse trig integration (`arctan`, `arcsin`)
- No partial fractions (needs polynomial engine)
- No repeated integration by parts (`x²*e^x`)
- `Const` stores `float`, so exact rational arithmetic is not supported
- No multi-argument functions (e.g. `log(x, 2)`)
- No equation solving yet