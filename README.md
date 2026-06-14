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
constants.py     - token type constants (NUMBER, IDENTIFIER, PLUS, ...) and FUNCTION_MAP
expressions.py   - Expr AST node classes (Const, Var, Add, Sub, Mul, Div, Pow, Neg,
                    Sin, Cos, Tan, Cot, Sec, Csc, Exp, Log)
tokeniser.py     - tokenise(expr: str) -> list[Token]
parser.py        - Parser class, recursive descent: parse() -> Expr
evaluate.py      - evaluate(expr: Expr, env: dict) -> float
simplify.py      - simplify(expr: Expr) -> Expr
depends_on.py    - depends_on(expr: Expr, var: str) -> bool
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
- The identifier `e` is treated as the constant `Const(math.e)`

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
| `Pow(f, g)`       | power rule, exponential rule, or log-differentiation, depending on which of `f`/`g` depend on `var` |
| `Sin`, `Cos`, `Tan`, `Cot`, `Sec`, `Csc`, `Exp`, `Log` | chain rule |

## Simplification rules implemented

- Identity elements: `f+0`, `0+f`, `f-0`, `f*1`, `1*f`, `f/1`, `f^1`
- Zero rules: `f*0`, `0*f`, `0/f`, `0^f` (convention), `f^0` (convention, including `0^0 -> 1`)
- Constant folding: `Const(a) op Const(b) -> Const(result)` for `+ - * / ^`
- `f - f -> 0`, `f / f -> 1` (structural equality)
- `Neg(Neg(f)) -> f`, `Neg(Const(c)) -> Const(-c)`
- Recursive simplification inside all function calls (`sin`, `cos`, `log`, ...)

## Known limitations / TODO

- No "combine like terms" rule yet (e.g. `2*x + 3*x` does not simplify to `5*x`).
  Planned after differentiation is working, using real derivative output as test cases.
- Uses Python's `math` module for `sin`, `cos`, `log`, `exp`, and the constant `e`.
  A from-scratch `mathfuncs.py` (Taylor series, Newton's method, hardcoded `pi`) is
  planned as a later upgrade.
- `Const` stores a `float`, so results can have floating-point imprecision
  (e.g. `0.1 + 0.2 != 0.3` exactly). No exact rational arithmetic (`Fraction`) yet.
- No support for multi-argument functions (e.g. `log(x, 2)`).