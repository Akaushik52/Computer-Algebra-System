# Computer Algebra System (CAS) 🐍

This project is a personal endeavor to build a Computer Algebra System (CAS) from scratch in Python. It aims to provide functionalities for symbolic manipulation, including differentiation, integration, and simplification of mathematical expressions.

[![Python Version](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## Table of Contents 📄

* [Project Title & Badges](#computer-algebra-system-cas-🐍)
* [Description](#description)
* [Features](#features-✨)
* [Tech Stack](#tech-stack-🚀)
* [Installation](#installation--)
* [Usage](#usage--)
* [Project Structure](#project-structure-🌳)
* [Contributing](#contributing--)
* [License](#license-📜)
* [Footer](#footer-👋)

---

## Description 📝

The Computer Algebra System (CAS) is a Python-based project designed to perform symbolic mathematical operations. It parses mathematical expressions, allowing users to differentiate, integrate, simplify, and evaluate them. The system represents expressions using an Abstract Syntax Tree (AST) and implements various rules for algebraic manipulation.

---

## Features ✨

*   **Symbolic Differentiation:** Calculates the derivative of expressions with respect to a given variable.
*   **Symbolic Integration:** Computes the antiderivative of expressions, returning a symbolic result or an unevaluated integral.
*   **Expression Simplification:** Applies a set of rules to simplify expressions (e.g., constant folding, collecting like terms, power rules).
*   **Expression Evaluation:** Numerically evaluates symbolic expressions given values for variables.
*   **Abstract Syntax Tree (AST):** Represents mathematical expressions as immutable frozen dataclasses.
*   **Grammar Parsing:** Implements a recursive descent parser to interpret mathematical expressions.
*   **Streamlit-based GUI:** Provides an interactive web interface for using the CAS functionalities.
*   **Algebraic Utilities:** Includes functions for identifying free variables, checking if an expression is constant, and substituting subexpressions.

---

## Tech Stack 🚀

*   **Language:** Python
*   **Frameworks/Libraries:**
    *   Streamlit (for the interactive GUI)
*   **Core Components:** Custom-built parser, tokenizer, expression tree, and manipulation modules.

---

## Installation ⚙️

This project does not have explicit dependencies listed in a `requirements.txt` file or similar. However, it relies on standard Python libraries and Streamlit for its interactive interface.

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/Akaushik52/Computer-Algebra-System.git
    cd Computer-Algebra-System
    ```

2.  **Install Streamlit:**
    ```bash
    pip install streamlit
    ```

---

## Usage 💡

The primary entry point for the interactive user interface is `app.py`, which utilizes Streamlit.

**To run the application:**

```bash
streamlit run app.py
```

This will launch a web application in your browser where you can:

1.  **Enter an expression:** Type your mathematical expression in the 'Expression' field (e.g., `x^2 + sin(x)`).
2.  **Specify the variable:** Enter the variable you want to operate on (default is 'x').
3.  **Choose an operation:** Select from 'Simplify', 'Evaluate', 'Differentiate', or 'Integrate'.
4.  **Perform operations:** The system will display the parsed input, simplified input (if applicable), and the result of the chosen operation.

**Example Usage (from `app.py`):**

When the Streamlit app is running, you can input an expression like `sin(x^2) * log(x)` and choose an operation.

**Example Usage (programmatic):**

You can also use the core functionalities directly in your Python scripts:

```python
from tokeniser import tokenise
from parser import Parser
from evaluate import evaluate
from simplify import simplify
from differentiate import differentiate
from integrate import integrate

def parse(s):
    return Parser(tokenise(s)).parse()

# Example expression
expr = parse("x^2 + sin(x)")

# Numeric evaluation
print(evaluate(expr, {"x": 2}))

# Simplification
print(simplify(expr))

# Differentiation
print(simplify(differentiate(expr, "x")))

# Integration
print(simplify(integrate(expr, "x")))
```

---

## Project Structure 🌳

The project is organized into several Python modules, each responsible for a specific part of the CAS:

```
expressions.py   - Defines the AST node classes (Const, Var, Add, Mul, Pow, Neg, Sin, Cos, etc.).
definitions.py   - Contains token constants and mappings for functions/constants.
tokeniser.py     - Handles the tokenization of input strings into a list of tokens.
parser.py        - Implements a recursive descent parser to build the expression AST.
evaluate.py      - Evaluates symbolic expressions numerically.
simplify.py      - Applies simplification rules to expressions.
differentiate.py - Implements symbolic differentiation logic.
integrate.py     - Implements symbolic integration logic.
algebra.py       - Provides utility functions like free_variables, is_constant, and substitute.
app.py           - The main entry point for the Streamlit web application.
README.md        - Project documentation.
```

---

## How to Use 🤔

This CAS is designed for mathematical expression manipulation. It can be used for:

*   **Educational purposes:** Understanding how symbolic computation works, learning calculus concepts.
*   **Prototyping:** Quickly testing mathematical formulas and deriving expressions.
*   **Simple symbolic calculations:** Performing basic differentiation, integration, and simplification tasks.

**Key Capabilities:**

*   **Parsing:** Understands standard mathematical notation, including functions like `sin`, `cos`, `log`, `exp`, and constants like `pi` and `e`.
*   **Simplification:** Handles common algebraic and trigonometric identities, constant folding, and term collection.
*   **Differentiation:** Applies standard calculus rules (chain rule, product rule, etc.).
*   **Integration:** Implements basic integration techniques, returning symbolic antiderivatives where possible.

---

## Known Limitations ⚠️

The current version of the CAS has several limitations:

*   **Trigonometric Identities:** Lacks rewrites for identities like `sin²(x) + cos²(x) = 1`.
*   **Inverse Trig Integration:** No support for integrating inverse trigonometric functions (e.g., `arctan`, `arcsin`).
*   **Partial Fractions:** Requires a polynomial engine, which is not yet implemented.
*   **Advanced Integration:** Does not handle repeated integration by parts (e.g., `x²*e^x`).
*   **Arithmetic Precision:** Uses `float` for constants, limiting exact rational arithmetic.
*   **Function Arity:** Supports only single-argument functions (e.g., `log(x)` but not `log(x, 2)`).
*   **Equation Solving:** Lacks functionality for solving equations.

---

## Contributing 🤝

As this is a personal project, contributions are welcome but should align with the project's goal of building a CAS from scratch. Please feel free to:

1.  Fork the repository.
2.  Create a new branch for your feature (`git checkout -b feature/AmazingFeature`).
3.  Commit your changes (`git commit -m 'Add some AmazingFeature'`).
4.  Push to the branch (`git push origin feature/AmazingFeature`).
5.  Open a Pull Request.

*Please ensure your contributions are well-documented and include tests where applicable.*

---

## License 📜

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Footer 👋

Made with ❤️ by Akaushik52

**Repository:** [Computer-Algebra-System](https://github.com/Akaushik52/Computer-Algebra-System)

[![GitHub stars](https://img.shields.io/github/stars/Akaushik52/Computer-Algebra-System?style=social)](https://github.com/Akaushik52/Computer-Algebra-System)
[![GitHub forks](https://img.shields.io/github/forks/Akaushik52/Computer-Algebra-System?style=social)](https://github.com/Akaushik52/Computer-Algebra-System)

*If you find this project useful, please consider starring ⭐, forking 🍴, or opening an issue ❗.*


---
**<p align="center">Generated by [ReadmeCodeGen](https://www.readmecodegen.com/)</p>**