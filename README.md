# Differentiate

A small Computer Algebra System (CAS) in Python, built from scratch, focused on symbolic differentiation.

Given a math expression as a string (e.g. `"3*x^2 + sin(x)"`), this project:
1. **Tokenizes** it into a flat stream of tokens
2. **Parses** the tokens into an Abstract Syntax Tree (AST) using recursive descent
3. **Evaluates** the AST numerically given variable values
4. **Simplifies** the AST by applying algebraic identity rules
5. **Differentiates** the AST symbolically with respect to a variable, producing a new AST

## Project structure

```
Constants.py     - token type constants (NUMBER, IDENTIFIER, PLUS, ...) and FUNCTION_MAP
expressions.py   - Expr AST node classes (Const, Var, Add, Sub, Mul, Div, Pow, Neg,
                    Sin, Cos, Tan, Cot, Sec, Csc, Exp, Log)
tokeniser.py     - tokenise(expr: str) -> list[Token]
parser.py        - Parser class, recursive descent: parse() -> Expr
evaluate.py      - evaluate(expr: Expr, env: dict) -> float
                    accurate(expr: Expr, env: dict) -> float (evaluate, rounded to 12 d.p.)
simplify.py      - simplify(expr: Expr) -> Expr
differentiate.py - differentiate(expr: Expr, var: str) -> Expr
```

## Usage

```python
from tokeniser import tokenise
from parser import Parser
from evaluate import evaluate
from simplify import simplify
from differentiate import differentiate

text = "3*x^2 + sin(x)"
ast = Parser(tokenise(text)).parse()

print(ast)                          # the parsed expression
print(evaluate(ast, {"x": 2}))      # numeric evaluation at x = 2
print(simplify(ast))                # simplified form

derivative = differentiate(ast, "x")
print(simplify(derivative))         # derivative, cleaned up
```

## Grammar

```
expression := term (('+' | '-') term)*
term       := unary (('*' | '/') unary)*
unary      := '-' unary | power
power      := primary ('^' unary)?
primary    := NUMBER | IDENTIFIER | IDENTIFIER '(' expression ')' | '(' expression ')'
```

- `+ -` (binary) bind loosest, `* /` next, unary `-` next, `^` tightest (right-associative)
- An `IDENTIFIER` followed by `(` is parsed as a function call (`sin`, `cos`, `tan`, `cot`,
  `sec`, `cosec`, `exp`, `log`); otherwise it's a variable
- The identifier `e` is treated as the constant `Const(E)`, where `E` is a hardcoded
  float literal in `Constants.py` (numerically equal to `math.e`, but not derived from it)

## Differentiation rules implemented

| Expression       | Rule                                                  |
|-------------------|------------------------------------------------------|
| `Const(c)`        | `0`                                                    |
| `Var(x)`          | `1` if `x == var`, else `0`                           |
| `Add(f, g)`       | `f' + g'`                                             |
| `Sub(f, g)`       | `f' - g'`                                             |
| `Neg(f)`          | `-f'`                                                 |
| `Mul(f, g)`       | product rule: `f'g + fg'`                             |
| `Div(f, g)`       | quotient rule: `(f'g - fg') / g^2`                    |
| `Pow(f, g)`       | `g` constant → power rule (`g*f^(g-1)*f'`); `f` constant → exponential rule (`f^g*ln(f)*g'`); otherwise → logarithmic differentiation (`f^g*(g'*ln(f) + g*f'/f)`) |
| `Sin`, `Cos`, `Tan`, `Cot`, `Sec`, `Csc`, `Exp`, `Log` | chain rule |

## Simplification rules implemented

- Identity elements: `f+0`, `0+f`, `f-0`, `f*1`, `1*f`, `f/1`, `f^1`
- Zero rules: `f*0`, `0*f`, `0/f`, `0^f` (convention), `f^0` (convention, including `0^0 -> 1`)
- Constant folding: `Const(a) op Const(b) -> Const(result)` for `+ - * / ^`
- `f - f -> 0`, `f / f -> 1` (structural equality)
- `f * (1/f) -> 1` and `(1/f) * f -> 1` (reciprocal cancellation, structural equality)
- `Neg(Neg(f)) -> f`, `Neg(Const(c)) -> Const(-c)`
- Sign normalization in products: `(-a)*(-b) -> a*b`, `a*(-b) -> -(a*b)`, `(-a)*b -> -(a*b)`,
  with the result recursively re-simplified (so e.g. `(-x)*(1/x)` folds all the way to `-1`)
- Constant folding for `sin`, `cos`, `tan`, `cot`, `sec`, `csc`, `exp`, `log` when the argument
  is a `Const`: evaluates numerically via `accurate()` (rounded to 12 decimal places to absorb
  floating-point noise, e.g. `sin(0) -> 0.0` instead of `1.2e-16`)
- Recursive simplification inside all function calls (`sin`, `cos`, `log`, ...)

## Known limitations / TODO

- No "combine like terms" rule yet (e.g. `2*x + 3*x` does not simplify to `5*x`), and no
  trig-identity collapsing (e.g. `cos(x)^2 - sin(x)^2` does not become `cos(2*x)`).
  Differentiation is now complete across all `Expr` types, so real derivative output
  (e.g. `sin(x)*cos(x) -> -(sin(x)*sin(x))+(cos(x)*cos(x))`) is available as test cases for this.
- Constant folding (`accurate()`) uses Python's `math` module under the hood, and the
  constant `e` is a hardcoded float literal rather than derived from `math.e`. A from-scratch
  `mathfuncs.py` (Taylor series, Newton's method, hardcoded `pi`) is planned as a later upgrade.
- `Const` stores a `float`, so results can have floating-point imprecision
  (e.g. `0.1 + 0.2 != 0.3` exactly). No exact rational arithmetic (`Fraction`) yet.
- No support for multi-argument functions (e.g. `log(x, 2)`).
- Yet to add Latex writing