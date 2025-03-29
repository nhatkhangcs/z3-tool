from z3 import *
import random
from .utils import expr_to_fol_string

def trace_chained_premises_with_indices(premises, target_expr):
    """
    Trace the premises that are logically chained to infer the target expression.

    Args:
        premises (list): List of premises (rule name, expression).
        target_expr (z3.ExprRef): The target expression to trace.

    Returns:
        list: A list of indices of premises used to infer the target expression.
    """
    used_indices = []
    current_expr = target_expr

    for idx, (rule, expr) in enumerate(reversed(premises)):
        if current_expr.eq(expr):  # Check if the current expression matches
            used_indices.append(len(premises) - 1 - idx)  # Store the index
            # Update the current expression to trace further
            if is_app(expr) and expr.num_args() > 0:
                current_expr = expr.arg(0)  # Assume the first argument is part of the chain
            else:
                break

    return list(reversed(used_indices))  # Reverse to maintain logical order

def generate_chained_multiple_choice_question(premises, option="last"):
    """
    Generate a multiple-choice question using chained premises.

    Args:
        premises (dict): Dictionary containing original, derived, and unrelated premises.
        option (str): The type of question to generate ("last", "random").

    Returns:
        tuple: A tuple containing the question, the correct answer letter (A, B, C, or D), and the indices of premises used.
    """
    all_premises = premises["original"] + premises["derived"]
    chosen_step = random.randint(0, len(all_premises) - 1) if option == "random" else len(all_premises) - 1
    _, answer_expr = all_premises[chosen_step]

    # Trace the indices of premises used to infer the answer
    used_indices = trace_chained_premises_with_indices(all_premises, answer_expr)

    # Generate the correct answer and distractors
    answer = expr_to_fol_string(answer_expr)
    false_answers = [
        expr_to_fol_string(Not(answer_expr)),
        expr_to_fol_string(Implies(answer_expr, answer_expr)),
        expr_to_fol_string(And(answer_expr, Not(answer_expr))),
        "Uncertain"  # Add "Uncertain" as a distractor
    ]
    options = [answer] + false_answers[:3]
    random.shuffle(options)

    # Determine the correct answer letter
    correct_answer_letter = chr(65 + options.index(answer))  # Convert index to letter (A, B, C, D)

    # Format the question
    question = f"Based on the above premises, which statement can be inferred?\n"
    # for idx, (rule, expr) in enumerate(all_premises):
    #     question += f"Premise {idx}: {rule} -> {expr_to_fol_string(expr)}\n"
    formatted_options = "\n".join([f"{chr(65+i)}. {opt}" for i, opt in enumerate(options)])
    question += formatted_options

    return question, correct_answer_letter, used_indices


def generate_chained_yes_no_question(premises, option="last"):
    """
    Generate a yes/no/uncertain question using chained premises.

    Args:
        premises (dict): Dictionary containing original, derived, and unrelated premises.
        option (str): The type of question to generate ("last", "random").

    Returns:
        tuple: A tuple containing the question, the correct answer, and the indices of premises used.
    """
    all_premises = premises["original"] + premises["derived"]
    chosen_step = random.randint(0, len(all_premises) - 1) if option == "random" else len(all_premises) - 1
    _, target_expr = all_premises[chosen_step]

    # Randomly decide the type of question: "Yes", "No", or "Uncertain"
    question_type = random.choice(["Yes", "No", "Uncertain"])

    if question_type == "Yes":
        # Trace the indices of premises used to infer the answer
        used_indices = trace_chained_premises_with_indices(all_premises, target_expr)
        answer = "Yes" if used_indices else "Uncertain"
    elif question_type == "No":
        # Negate the target expression to create a contradiction
        target_expr = Not(target_expr)
        used_indices = trace_chained_premises_with_indices(all_premises, target_expr)
        answer = "No" if used_indices else "Uncertain"
    else:  # "Uncertain"
        # Create an expression that cannot be inferred
        target_expr = random.choice([expr for _, expr in premises["unrelated"]])
        used_indices = []
        answer = "Uncertain"

    # Format the question
    question = f"Based on the above premises, is the statement true?\n"
    question += f"Statement: {expr_to_fol_string(target_expr)}"

    return question, answer, used_indices