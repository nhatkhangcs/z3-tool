from z3 import *
import json

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

def save_to_json(filepath, premises, questions, answers, indices):
    """
    Save premises, questions, answers, and indices to a JSON file.

    Args:
        filepath (str): Path to the JSON file.
        premises (list): List of premises in string format.
        questions (list): List of questions in string format.
        answers (list): List of answers (e.g., "A", "B", "Yes", "Uncertain").
        indices (list): List of lists, where each sublist contains indices of premises used for each answer.
    """
    data = {
        "premises": premises,
        "questions": questions,
        "answers": answers,
        "idx": indices
    }

    with open(filepath, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, indent=4, ensure_ascii=False)

    print(f"Data successfully saved to {filepath}")