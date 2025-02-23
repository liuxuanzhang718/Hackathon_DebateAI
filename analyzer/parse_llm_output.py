import re
import json

def convert_logical_expression(expr: str) -> list:
    """
    Converts a logical expression string into a list of tokens according to the following rules:
      - AND (∧) → "1"
      - OR (∨) → "2"
      - NOT (~ or ～) → "3"
      - IMPLY (→) → "4"
      - IF AND ONLY IF (↔) → "5"
      - Parentheses (( or )) → "6"
    Any other text is converted to lowercase and kept as an operand.
    
    Parameters:
      expr: The logical expression string.
      
    Returns:
      A list of tokens representing the converted logical expression.
    """
    mapping = {
        "∧": "1",
        "∨": "2",
        "~": "3",
        "→": "4",
        "↔": "5",
        "(": "6",
        ")": "6",
        "～": "3"  # If a full-width NOT symbol is encountered, also convert it to "3"
    }
    # Define a regex pattern to capture all the operators (these unicode symbols can be matched directly)
    pattern = r"(\∧|\∨|~|→|↔|\(|\)|～)"
    tokens = re.split(pattern, expr)
    converted_tokens = []
    for token in tokens:
        token = token.strip()
        if not token:
            continue
        if token in mapping:
            converted_tokens.append(mapping[token])
        else:
            # Convert operands to lowercase and preserve the original text
            converted_tokens.append(token.lower())
    return converted_tokens

def parse_llm_output(raw_output: str, sentence: str) -> dict:
    """
    Parses the raw output from the LLM and converts it into JSON format.
    
    Example input:
    
        Logical Expression:
        Consumer spending falls ∨ unemploynent rises → (~ economy improve ∧ interest rates rise )
    
        Performances:
        Valid: True  
        Valid Explanation:  
        Sound: False 
        Sound Explanation: It's not necessarily true that consumer spending falling or unemployment rising will cause the economy to worsen.
    
    Example output:
    
    {
      "logical_expression": "Consumer spending falls ∨ unemploynent rises → (~ economy improve ∧ interest rates rise )",
      "converted_logical_expression": [
        "consumer spending falls",
        "2", 
        "unemploynent rises",
        "4",
        "6",
        "3",
        "economy improve",
        "1",
        "interest rates rise",
        "6"
      ],
      "performance": {
        "valid": true,
        "valid_explanation": "",
        "sound": false,
        "sound_explanation": "It's not necessarily true that consumer spending falling or unemployment rising will cause the economy to worsen."
      }
    }
    
    Parameters:
      raw_output: The raw string output from the LLM.
      sentence: The original sentence being analyzed (unused in current implementation, but kept for interface consistency).
    
    Returns:
      A dictionary containing the parsed JSON structure.
    """
    # Define markers to separate different sections
    logical_expr_marker = "Logical Expression:"
    performances_marker = "Performances:"
    
    # If the markers are not found, return an empty dictionary
    if logical_expr_marker not in raw_output or performances_marker not in raw_output:
        return {}
    
    # Partition the raw output into the Logical Expression part and the Performances part
    _, _, rest = raw_output.partition(logical_expr_marker)
    logical_expr_part, _, performance_part = rest.partition(performances_marker)
    logical_expr = logical_expr_part.strip()

    # Initialize variables for the Performances section
    valid = None
    valid_explanation = ""
    sound = None
    sound_explanation = ""
    
    # Process the Performances part line by line
    for line in performance_part.splitlines():
        line = line.strip()
        # Ensure "Valid Explanation:" is not confused with "Valid:"
        if line.startswith("Valid Explanation:"):
            valid_explanation = line[len("Valid Explanation:"):].strip()
        elif line.startswith("Valid:") and not line.startswith("Valid Explanation:"):
            valid_str = line[len("Valid:"):].strip()
            valid = True if valid_str.lower() == "true" else False
        elif line.startswith("Sound Explanation:"):
            sound_explanation = line[len("Sound Explanation:"):].strip()
        elif line.startswith("Sound:") and not line.startswith("Sound Explanation:"):
            sound_str = line[len("Sound:"):].strip()
            sound = True if sound_str.lower() == "true" else False

    # Convert the logical expression into a token list
    converted_tokens = convert_logical_expression(logical_expr)
    
    result = {
        "logical_expression": logical_expr,
        "converted_logical_expression": converted_tokens,
        "performance": {
            "valid": valid,
            "valid_explanation": valid_explanation,
            "sound": sound,
            "sound_explanation": sound_explanation
        }
    }
    
    return result
