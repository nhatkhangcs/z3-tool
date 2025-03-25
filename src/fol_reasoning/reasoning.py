from z3 import *
import random
from .utils import expr_to_fol_string

class FOLReasoning:
    """
    A class to encapsulate First-Order Logic (FOL) reasoning operations, including
    generating premises, displaying them, and creating questions and answers.
    """

    def __init__(self):
        # Declare variables (lowercase letters)
        self.variables = Ints('x y z a b c d e f g h t s')
        self.x, self.y, self.z, self.a, self.b, self.c, self.d, self.e, self.f, self.g, self.h, self.t, self.s = self.variables

        # Declare functions/predicates (uppercase letters)
        self.P = Function('P', IntSort(), BoolSort())
        self.Q = Function('Q', IntSort(), BoolSort())
        self.R = Function('R', IntSort(), BoolSort())
        self.S = Function('S', IntSort(), BoolSort())
        self.T = Function('T', IntSort(), BoolSort())
        self.U = Function('U', IntSort(), BoolSort())

        # Define inference rules
        self.rules = {
            "MP": lambda p, q: Implies(p, q),  # Modus Ponens
            "MT": lambda p, q: Implies(Not(q), Not(p)),  # Modus Tollens
            "HS": lambda p, q, r: Implies(And(Implies(p, q), Implies(q, r)), Implies(p, r)),  # Hypothetical Syllogism
            "DS": lambda p, q: Implies(And(Or(p, q), Not(p)), q),  # Disjunctive Syllogism
            "CD": lambda p, q, r, s: Implies(And(Implies(p, q), Implies(r, s), Or(p, r)), Or(q, s)),  # Constructive Dilemma
            "DD": lambda p, q, r, s: Implies(And(Implies(p, q), Implies(r, s), Not(Or(q, s))), Not(Or(p, r))),  # Destructive Dilemma
            "BD": lambda p, q, r, s: Implies(And(Implies(p, q), Implies(r, s), Or(p, Not(s))), Or(q, Not(r))),  # Bidirectional Dilemma
            "CT": lambda p, q: Implies(Or(p, q), Or(q, p)),  # Commutation
            "DMT": lambda p, q: Implies(Not(And(p, q)), Or(Not(p), Not(q))),  # De Morgan’s Theorem
            "CO": lambda p, q, r: Implies(And(Implies(p, q), Implies(p, r)), Implies(p, And(q, r))),  # Composition
            "IM": lambda p, q, r: Implies(Implies(p, Implies(q, r)), Implies(And(p, q), r)),  # Importation
            "MI": lambda p, q: Implies(Implies(p, q), Or(Not(p), q)),  # Material Implication
            "EG": lambda p: Exists([self.x], p(self.x)),  # Existential Generalization
            "UI": lambda p: ForAll([self.x], p(self.x)),  # Universal Instantiation
        }

    def generate_premises(self, steps):
        """
        Generate a random set of premises based on the defined inference rules.

        Args:
            steps (int): Number of reasoning steps to generate.

        Returns:
            list: A list of tuples containing rule names and generated premises.
        """
        premises = []
        used_variables = [self.P, self.Q, self.R, self.S, self.T, self.U]  # Use functions, not BoolRef

        for _ in range(steps):
            rule_name, rule_func = random.choice(list(self.rules.items()))
            vars_needed = rule_func.__code__.co_argcount

            # For rules requiring functions (e.g., EG, UI), pass functions; otherwise, pass BoolRef
            if rule_name in ["EG", "UI"]:
                chosen_vars = random.sample(used_variables, vars_needed)
            else:
                chosen_vars = random.sample([f(self.x) for f in used_variables], vars_needed)

            new_premise = rule_func(*chosen_vars)
            premises.append((rule_name, new_premise))

        return premises

    def display_premises(self, premises):
        """
        Display the generated premises in a readable format.

        Args:
            premises (list): List of premises to display.
        """
        for idx, (rule, expr) in enumerate(premises, start=1):
            print(f"Step {idx}: {rule} -> {expr} \n {expr_to_fol_string(expr)}")