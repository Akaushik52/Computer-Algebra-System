import streamlit as st
from tokeniser import tokenise
from parser import Parser
from simplify import simplify
from differentiate import differentiate
from evaluate import evaluate

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="CAS",
    page_icon="∂",
    layout="centered",
)

# ── Minimal custom CSS ─────────────────────────────────────────────────────────
st.markdown("""
<style>
    .block-container { padding-top: 2rem; max-width: 720px; }
    .result-box {
        background: #1e2130;
        border-left: 3px solid #4f8ef7;
        border-radius: 4px;
        padding: 1rem 1.25rem;
        margin: 0.5rem 0 1rem 0;
        color: #e8eaf0;
    }
    .label {
        font-size: 0.78rem;
        font-weight: 600;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        color: #888;
        margin-bottom: 0.25rem;
    }
    .error-msg { color: #c0392b; font-size: 0.9rem; }
</style>
""", unsafe_allow_html=True)

# ── Header ─────────────────────────────────────────────────────────────────────
st.markdown("## Computer Algebra System")
st.caption("Differentiate, simplify, and evaluate symbolic expressions.")
st.divider()

# ── Input panel ────────────────────────────────────────────────────────────────
col1, col2 = st.columns([4, 1])
with col1:
    expr_str = st.text_input(
        "Expression",
        value="sin(x^2)",
        placeholder="e.g. sin(x^2) * log(x)",
        label_visibility="visible",
    )
with col2:
    var = st.text_input("Variable", value="x")

mode = st.radio(
    "Operation",
    ["Simplify", "Evaluate", "Differentiate"],
    horizontal=True,
)

eval_value = None
if mode == "Evaluate":
    eval_value = st.number_input(
        f"Value of  {var}",
        value=1.0,
        step=0.1,
        format="%.4f",
    )

st.divider()

# ── Helper ─────────────────────────────────────────────────────────────────────
def parse(s):
    return Parser(tokenise(s)).parse()

def result_block(label, expr):
    st.markdown(f'<div class="label">{label}</div>', unsafe_allow_html=True)
    st.latex(expr.latex())

# ── Main logic ─────────────────────────────────────────────────────────────────
if expr_str and var:
    try:
        ast = parse(expr_str)

        # Always show parsed input
        result_block("Input", ast)
        simplified_input = simplify(ast)
        if str(simplified_input) != str(ast):
            result_block("Simplified input", simplified_input)

        st.divider()

        # ── Differentiate ──────────────────────────────────────────────────────
        if mode == "Differentiate":
            raw   = differentiate(ast, var)
            final = simplify(raw)

            result_block(f"d/d{var}", final)


            with st.expander(f"Show derivative at a point"):
                eval_at = st.number_input(f"Evaluate derivative at {var} =", value=1.0, step=0.1, format="%.4f")
                d_val = evaluate(final, {var: eval_at})
                st.markdown(
                    f'<div class="result-box"><span style="font-size:1.4rem;color:#e8eaf0;">'
                    f'{round(d_val, 10)}</span></div>',
                    unsafe_allow_html=True,
                )

        # ── Simplify ───────────────────────────────────────────────────────────
        elif mode == "Simplify":
            result = simplify(ast)
            result_block("Simplified", result)

        # ── Evaluate ───────────────────────────────────────────────────────────
        elif mode == "Evaluate":
            env = {var: eval_value}
            val = evaluate(ast, env)

            st.markdown(f'<div class="label">Result at {var} = {eval_value}</div>',
                        unsafe_allow_html=True)
            st.markdown(
                f'<div class="result-box"><span style="font-size:1.6rem;'
                f'font-weight:600;color:#e8eaf0;">{round(val, 10)}</span></div>',
                unsafe_allow_html=True,
            )

    except ZeroDivisionError:
        st.error("Division by zero — try a different value of the variable.")
    except ValueError as e:
        st.error(f"{e}")
    except Exception as e:
        st.error(f"Could not parse expression: {e}")

else:
    st.info("Enter an expression above to get started.")

# ── Reference ──────────────────────────────────────────────────────────────────
with st.expander("Supported syntax"):
    st.markdown("""
| Syntax | Meaning |
|---|---|
| `x^2`, `x^0.5` | Powers |
| `sin(x)`, `cos(x)`, `tan(x)` | Trig |
| `cot(x)`, `sec(x)`, `cosec(x)` | Reciprocal trig |
| `log(x)` | Natural log ln(x) |
| `exp(x)` | eˣ  (also written as `e^x`) |
| `*`, `/`, `+`, `-` | Arithmetic |
| `e` | Euler's number |
| `pi` | π |
""")