from fol_reasoning.reasoning import FOLReasoning
from fol_reasoning.questions import generate_chained_multiple_choice_question, generate_chained_yes_no_question
from fol_reasoning.utils import expr_to_fol_string

if __name__ == "__main__":
    # Initialize the FOLReasoning class
    fol_reasoning = FOLReasoning()

    # Generate premises with 5 steps, 3 chained premises, and 2 derived premises
    premises = fol_reasoning.generate_premises(steps=3, chain_count=1, derive_count=2)

    # Display the premises
    print("\n=== All Premises ===")
    all_premises = premises["original"] + premises["derived"] + premises["unrelated"]
    for idx, (rule, expr) in enumerate(all_premises):
        print(f"Premise {idx}: {rule} -> {expr_to_fol_string(expr)}")

    # Generate a chained multiple-choice question
    print("\n=== Multiple-Choice Question ===")
    mc_question, mc_answer, mc_used_indices = generate_chained_multiple_choice_question(premises, option="last")
    print(mc_question)
    print(f"Correct Answer: {mc_answer}")
    print("\nPremises Used for Inference:")
    for idx in mc_used_indices:
        rule, expr = all_premises[idx]
        print(f"Premise {idx}")

    # Generate a chained yes/no/uncertain question
    print("\n=== Yes/No/Uncertain Question ===")
    yn_question, yn_answer, yn_used_indices = generate_chained_yes_no_question(premises, option="last")
    print(yn_question)
    print(f"Correct Answer: {yn_answer}")
    print("\nPremises Used for Inference:")
    for idx in yn_used_indices:
        rule, expr = all_premises[idx]
        print(f"Premise {idx}")