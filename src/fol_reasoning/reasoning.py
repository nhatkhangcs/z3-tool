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
            "EG": lambda p: Exists([self.x], p(self.x) if callable(p) else p),  # Existential Generalization
            "UI": lambda p: ForAll([self.x], p(self.x) if callable(p) else p),  # Universal Instantiation
        }

    def generate_premises(self, steps, chain_count, derive_count):
        """
        Generate a random set of premises, including derived premises created by chaining existing ones.

        Args:
            steps (int): Total number of premises to generate.
            chain_count (int): Number of premises that should be logically chained. chain_count <= steps.
            derive_count (int): Number of derived premises to create by chaining existing premises.

        Returns:
            dict: A dictionary containing lists of original, derived, and unrelated premises.
        """
        if chain_count > steps:
            raise ValueError("chain_count should be less than or equal to steps.")

        # Initialize lists for different types of premises
        original_premises = []
        derived_premises = []
        unrelated_premises = []
        unique_premises = set()  # Track unique premises

        used_variables = [self.P, self.Q, self.R, self.S, self.T, self.U]  # Use functions, not BoolRef

        # Generate original premises
        for _ in range(steps):
            while True:
                rule_name, rule_func = random.choice(list(self.rules.items()))
                vars_needed = rule_func.__code__.co_argcount
                chosen_vars = random.sample([f(self.x) for f in used_variables], vars_needed)
                premise = rule_func(*chosen_vars)

                # Avoid tautologies and duplicates
                if not self.is_tautology(premise) and str(premise) not in unique_premises:
                    original_premises.append((rule_name, premise))
                    unique_premises.add(str(premise))
                    break

        # Generate derived premises using Z3
        for _ in range(derive_count):
            while True:
                # Randomly select two premises to chain
                premise1 = random.choice(original_premises + derived_premises)
                premise2 = random.choice(original_premises + derived_premises)

                # Use Z3 to derive a new premise
                solver = Solver()
                solver.add(premise1[1])  # Add the first premise
                solver.add(premise2[1])  # Add the second premise

                # Attempt to derive a new logical conclusion
                derived_expr = Implies(premise1[1], premise2[1])  # Example: Derive an implication
                solver.push()
                solver.add(Not(derived_expr))  # Check if the derived expression is valid
                if solver.check() == unsat and not self.is_tautology(derived_expr) and str(derived_expr) not in unique_premises:
                    # If unsatisfiable, the derived expression is valid
                    derived_rule = f"Derived({premise1[0]} → {premise2[0]})"
                    derived_premises.append((derived_rule, derived_expr))
                    unique_premises.add(str(derived_expr))
                    solver.pop()
                    break
                solver.pop()

        # Generate unrelated premises for confusion
        for _ in range(steps - chain_count):
            while True:
                rule_name, rule_func = random.choice(list(self.rules.items()))
                vars_needed = rule_func.__code__.co_argcount
                chosen_vars = random.sample([f(self.x) for f in used_variables], vars_needed)
                unrelated_premise = rule_func(*chosen_vars)

                # Avoid tautologies and duplicates
                if not self.is_tautology(unrelated_premise) and str(unrelated_premise) not in unique_premises:
                    unrelated_premises.append((rule_name, unrelated_premise))
                    unique_premises.add(str(unrelated_premise))
                    break

        # Shuffle all premises to mix them
        all_premises = original_premises + derived_premises + unrelated_premises
        random.shuffle(all_premises)

        return {
            "original": original_premises,
            "derived": derived_premises,
            "unrelated": unrelated_premises,
        }

    def is_tautology(self, expr):
        """
        Check if a given expression is a tautology.

        Args:
            expr (z3.ExprRef): The expression to check.

        Returns:
            bool: True if the expression is a tautology, False otherwise.
        """
        solver = Solver()
        solver.add(Not(expr))  # Check if the negation of the expression is satisfiable
        return solver.check() == unsat

    def display_premises(self, premises):
        """
        Display the generated premises in a readable format.

        Args:
            premises (list): List of premises to display.
        """
        for idx, (rule, expr) in enumerate(premises, start=1):
            print(f"Step {idx}: {rule} -> {expr} \n {expr_to_fol_string(expr)}")