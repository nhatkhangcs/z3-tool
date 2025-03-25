from z3 import *

def expr_to_fol_string(expr):
    if is_app(expr):
        if expr.decl().name() == '=>':
            return f"({expr_to_fol_string(expr.arg(0))} → {expr_to_fol_string(expr.arg(1))})"
        elif expr.decl().name() == 'and':
            return f"({expr_to_fol_string(expr.arg(0))} ∧ {expr_to_fol_string(expr.arg(1))})"
        elif expr.decl().name() == 'or':
            return f"({expr_to_fol_string(expr.arg(0))} ∨ {expr_to_fol_string(expr.arg(1))})"
        elif expr.decl().name() == 'not':
            return f"¬{expr_to_fol_string(expr.arg(0))}"
    return str(expr)

