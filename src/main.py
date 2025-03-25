from fol_reasoning.reasoning import FOLReasoning
from fol_reasoning.questions import generate_question_answer, generate_multiple_choice_question, generate_yes_no_question

if __name__ == "__main__":
    fol_reasoning = FOLReasoning()
    premises = fol_reasoning.generate_premises(2)
    print("\n=== Premises ===")
    fol_reasoning.display_premises(premises)
    
    print("\n=== Question & Answer ===")
    question, answer = generate_question_answer(premises, option="hard")
    print(question)
    print(f"Answer: {answer}")
    
    print("\n=== Multiple-Choice Question ===")
    mc_question, mc_answer = generate_multiple_choice_question(premises, option="last")
    print(mc_question)
    print(f"Correct Answer: {mc_answer}")
    
    print("\n=== Yes/No Question ===")
    yn_question, yn_answer = generate_yes_no_question(premises, option="last")
    print(yn_question)
    print(f"Correct Answer: {yn_answer}")
