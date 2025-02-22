
# import spacy

# nlp = spacy.load("en_core_web_sm")

# def analyze_logic(sentence, llm_client):
#     # spaCy analysis for sentence structure
#     doc = nlp(sentence)

#     # Create a structure for key components and custom symbols
#     premise = []
#     conclusion = []

#     # Iterate over tokens to identify key components and map them to symbols
#     for token in doc:
#         if token.dep_ == 'nsubj':  # Example: Find the subject
#             premise.append(token.text)
#         elif token.dep_ == 'dobj':  # Example: Find the object
#             conclusion.append(token.text)
#         elif token.dep_ == 'mark' and token.text.lower() == "if":
#             # Identify "if" to represent an implication (→)
#             premise.append("→")

#     # Example: Simple implication structure (if...then...)
#     logic_expression = f"{' '.join(premise)} → {' '.join(conclusion)}"

#     # Now create the prompt for the LLM with the simplified logic
#     prompt = f"""
#     Given the sentence: "{sentence}",
#     Convert the following logic structure to a symbolic representation using custom symbols (Keep the phrases; don't convert them to letters, only represent their relationship with the following symbol):
#     - Use "→" for implication.
#     - Use "∧" for "and" (to represent logical conjunction).
#     - Use "¬" for "not" (to represent logical negation).
#     - For each clause in the sentence, break it down clearly into symbolic expressions.

#     Logic structure: {logic_expression}

#     Example:
#     - "More electric vehicles will reduce fuel cost" becomes "more electric vehicles → less fuel cost"
#     - "Reduced fuel cost will reduce air pollution and carbon emissions" becomes "less fuel cost → (less air pollution ∧ less carbon emissions)" (if air pollution and carbon emissions are two distinct facts, use "∧")
#     """

#     # Get logic analysis from the LLM
#     logic_analysis = llm_client.get_response(prompt)
    
#     return logic_analysis

import json
from parse_llm_output import parse_llm_output

def analyze_logic(sentence: str, llm) -> dict:
    # Construct the prompt asking the LLM to analyze the logical structure of the sentence
    prompt = f"""
    You are an AI assistant that analyzes the logical structure of a sentence and identifies logical errors.
    Please analyze the logical structure of the following sentence and present your analysis in plain text with the following sections:
    - Original Text
    - Premises (each line starting with "- pX: premise text")
    - Conclusions (each line starting with "- cX: conclusion text", followed by additional lines for "Expression:", "From:" and "To:")
    - Relations (each line starting with "- pX to pY: relation type")
    - Fallacies (each line starting with "- fallacy_type: description")

    For example, your output might look like:

    Original Text: Electric Vehicle will reduce fuel cost; therefore, reduce air pollution and carbon emission to reduce global warming.

    Premises:
    - p1: Electric Vehicle
    - p2: reduce fuel cost
    - p3: reduce air pollution
    - p4: reduce carbon emission
    - p5: reduce global warming

    Conclusions:
    - c1: Electric Vehicle → reduce fuel cost → (reduce air pollution ∧ reduce carbon emission) → reduce global warming
    Expression: p1 → p2 → (p3 ∧ p4) → p5
    From: p1
    To: p5

    Relations:
    - p1 to p2: if then
    - p2 to p3: if then
    - p2 to p4: if then
    - p3 to p4: or
    - p3 to p5: if then
    - p4 to p5: if then

    Fallacies:
    - causal_fallacy: Causal fallacy: assuming correlation implies causation (in English)
    - false_dichotomy: False dichotomy: oversimplifying complex issues into either/or choices (in English)

    Now, analyze this sentence:
    "{sentence}"
    """

    # Call the LLM to get the raw output
    raw_response = llm.get_response(prompt)

    # Try to directly parse the LLM output as JSON
    try:
        result = json.loads(raw_response)
        return result
    except Exception as e:
        # If direct parsing fails, use the custom parsing function to convert the LLM output into the required JSON format
        return parse_llm_output(raw_response, sentence)
