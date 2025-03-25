from z3 import *
import random
from .utils import expr_to_fol_string

def generate_question_answer(premises, option="last"):
    chosen_step = random.randint(0, len(premises) - 1) if option == "random" else len(premises) - 1
    rule_used, answer_expr = premises[chosen_step]
    answer = expr_to_fol_string(answer_expr)
    false_answers = [
        expr_to_fol_string(Not(answer_expr)),
        expr_to_fol_string(Implies(answer_expr, answer_expr)),
        expr_to_fol_string(And(answer_expr, Not(answer_expr)))
    ]
    options = [answer] + false_answers[:3]
    random.shuffle(options)
    question = f"Which statement can be inferred?\n"
    formatted_options = "\n".join([f"{chr(65+i)}. {opt}" for i, opt in enumerate(options)])
    return question + formatted_options, answer

def generate_multiple_choice_question(premises, option="last"):
    return generate_question_answer(premises, option)

def generate_yes_no_question(premises, option="last"):
    chosen_step = random.randint(0, len(premises) - 1) if option == "random" else len(premises) - 1
    rule_used, answer_expr = premises[chosen_step]
    question = f"Is the following statement true? {expr_to_fol_string(answer_expr)}"
    return question, "Yes"