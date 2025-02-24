import json
from parse_llm_output import parse_llm_output

# Common instructions for the "Logical Expression" and "Performances" sections
COMMON_INSTRUCTIONS = """
- Logical Expression
  Provide the logical expression of the sentence, using logical symbols to represent their relationships.
- Performances
  Provide the performance analysis with the following sub-sections:
    - Valid: True/False  
    - Valid Explanation: Provide explanation if invalid; leave empty if valid 
    - Sound: True/False  
    - Sound Explanation: Provide explanation if unsound; leave empty if sound 

For example, given the sentence: "If either consumer spending falls or unemployment rises, then the economy will not improve and interest rates will not rise.", your output might look like:

Logical Expression:
Consumer spending falls ∨ unemployment rises → (~ economy improve ∧ interest rates rise)

Performances:
Valid: True  
Valid Explanation:  
Sound: False  
Sound Explanation: It's not necessarily true that consumer spending falling or unemployment rising will cause the economy to worsen.

Given the sentence: "If it rained last night, then my lawn is wet this morning. It did not rain last night, so, my lawn is not wet this morning.", your output might look like:

Logical Expression:
(It rained last night → my lawn is wet this morning ∧ ~ it rained last night) → ~ my lawn is wet this morning

Performances:
Valid: False
Valid Explanation: The argument commits the fallacy of denying the antecedent by incorrectly assuming if the antecedent of a conditional statement is false, then the consequent must also be false, which is not logically valid.
Sound: False
Sound Explanation: An argument is sound if and only if it is valid and all premises are true. Since it's invalid, it's unsound.

Given the sentence: "If the mind and brain are identical, then the brain is a physical entity if and only if the mind is a physical entity. If the mind is a physical entity, then thoughts are material entities. Thoughts are not material, but the brain is a physical entity. Therefore, the mind and the brain are not identical.", your output might look like:

Logical Expression:
((Mind and brain are identical → (brain is a physical entity ↔ mind is a physical entity)) ∧ (mind is a physical entity → thoughts are material) ∧ (~ thoughts are material ∧ brain is a physical entity) → ~ mind and brain are identical

Performances:
Valid: True
Valid Explanation:
Sound: True
Sound Explanation:
"""

# Overall prompt template
PROMPT_TEMPLATE = """You are an AI assistant that analyzes the logical structure of a sentence and identifies logical errors.
{additional_instructions}

Now, analyze this sentence:
"{sentence}"
"""

def analyze_logic(sentence: str, llm, previous_context_expressions: list = None) -> dict:
    """
    Analyzes the logical structure of the current sentence and integrates it with previous logical expression outputs (if any),
    returning a JSON object that meets the front-end requirements.

    Parameters:
      - sentence: The current user input as a string.
      - llm: The interface object for the language model.
      - previous_context_expressions: If provided, a list of logical expressions from previous analyses,
        with each element being a string (e.g., "Consumer spending falls ∨ unemployment rises → (~ economy improve ∧ interest rates rise)").
    """
    additional_instructions = ""
    if previous_context_expressions and len(previous_context_expressions) > 0:
        previous_context_str = "Previous Logical Expressions:\n"
        # Concatenate each logical expression from the previous context into a single text block
        for expr in previous_context_expressions:
            previous_context_str += f"{expr}\n"
        additional_instructions = previous_context_str + "\n" + COMMON_INSTRUCTIONS + "\nNow, please integrate the previous analysis with the new sentence and analyze it."
    else:
        additional_instructions = COMMON_INSTRUCTIONS

    # Generate the final prompt using the template
    prompt = PROMPT_TEMPLATE.format(additional_instructions=additional_instructions, sentence=sentence)

    # Call the language model to get the raw output
    raw_response = llm.get_response(prompt)
    
    # Parse and return the LLM output as a JSON object
    return parse_llm_output(raw_response, sentence)
