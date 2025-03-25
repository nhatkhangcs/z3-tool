from z3 import *
import random


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
            print(f"Step {idx}: {rule} -> {expr} \n {self.expr_to_fol_string(expr)}")

    def expr_to_fol_string(self, expr):
        """
        Convert a Z3 expression into a human-readable FOL string.

        Args:
            expr (z3.ExprRef): The Z3 expression to convert.

        Returns:
            str: The human-readable FOL string.
        """
        # Check if the expression is an application (e.g., a function or operator)
        if is_app(expr):
            if expr.decl().name() == '=>':
                return f"({self.expr_to_fol_string(expr.arg(0))} → {self.expr_to_fol_string(expr.arg(1))})"
            elif expr.decl().name() == 'and':
                return f"({self.expr_to_fol_string(expr.arg(0))} ∧ {self.expr_to_fol_string(expr.arg(1))})"
            elif expr.decl().name() == 'or':
                return f"({self.expr_to_fol_string(expr.arg(0))} ∨ {self.expr_to_fol_string(expr.arg(1))})"
            elif expr.decl().name() == 'not':
                return f"¬{self.expr_to_fol_string(expr.arg(0))}"
            elif expr.decl().name() == 'forall':
                return f"∀{expr.var_name(0)}: {self.expr_to_fol_string(expr.body())}"
            elif expr.decl().name() == 'exists':
                return f"∃{expr.var_name(0)}: {self.expr_to_fol_string(expr.body())}"
        # If not an application, return the string representation
        return str(expr)

    def generate_question_answer(self, premises, option="last"):
        """
        Generate a question and answer based on the premises.

        Args:
            premises (list): List of premises to use.
            option (str): The type of question to generate ("last", "random", "hard", "natural").

        Returns:
            tuple: A tuple containing the question and the correct answer.
        """
        if option == "random":
            chosen_step = random.randint(0, len(premises) - 1)
        else:
            chosen_step = len(premises) - 1

        rule_used, answer_expr = premises[chosen_step]
        answer = self.expr_to_fol_string(answer_expr)

        false_answers = [
            self.expr_to_fol_string(Not(answer_expr)),
            self.expr_to_fol_string(Implies(answer_expr, self.P(self.x))),
            self.expr_to_fol_string(And(answer_expr, Not(self.Q(self.x))))
        ]
        options = [answer] + false_answers[:3]
        random.shuffle(options)

        if option == "natural":
            question = f"Dựa vào chuỗi suy luận, điều nào có thể suy ra?\n"
        else:
            question = f"Dựa vào các premises, điều nào sau đây là đúng?\n"

        formatted_options = "\n".join([f"{chr(65+i)}. {opt}" for i, opt in enumerate(options)])
        question += formatted_options

        return question, answer


if __name__ == "__main__":
    # Instantiate the reasoning class
    fol_reasoning = FOLReasoning()

    # Generate premises
    reasoning_steps = 2
    premises = fol_reasoning.generate_premises(reasoning_steps)

    # Display premises
    print("\n=== Premises ===")
    fol_reasoning.display_premises(premises)

    # Generate and display question and answer
    print("\n=== Câu Hỏi & Câu Trả Lời ===")
    option = "hard"  # Choose question type: "last", "random", "hard", "natural"
    question, answer = fol_reasoning.generate_question_answer(premises, option)
    print(question)
    print(f"Đáp án: {answer}")