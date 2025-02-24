import re
from typing import Dict, Any, List
from ..models.schemas import LogicChain, LogicalPerformance
from ..config import settings
from openai import OpenAI


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
    
    Args:
        expr: The logical expression string to convert
        
    Returns:
        A list of tokens representing the converted logical expression
    """
    # Define mapping for logical operators to numeric tokens
    mapping = {
        "∧": "1",
        "∨": "2",
        "~": "3",
        "→": "4",
        "↔": "5",
        "(": "6",
        ")": "6",
        "～": "3"  # Handle full-width NOT symbol
    }
    # Pattern to match all logical operators
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
            # Convert non-operator text to lowercase
            converted_tokens.append(token.lower())
    return converted_tokens


def parse_llm_output(raw_output: str, sentence: str) -> dict:
    """
    Parses the raw output from the LLM and converts it into a structured format.
    
    Args:
        raw_output: The raw string output from the LLM
        sentence: The original sentence being analyzed
        
    Returns:
        A dictionary containing:
        - logic_expression: The logical expression string
        - converted_logical_expression: List of tokens
        - performance: Dictionary with validity and soundness analysis
    """
    # Define section markers
    logical_expr_marker = "Logical Expression:"
    performances_marker = "Performances:"
    
    # Return empty result if required markers are missing
    if logical_expr_marker not in raw_output or performances_marker not in raw_output:
        return {}
    
    # Extract logical expression section
    _, _, rest = raw_output.partition(logical_expr_marker)
    logical_expr_part, _, performance_part = rest.partition(performances_marker)
    logical_expr = logical_expr_part.strip()

    # Initialize performance analysis variables
    valid = None
    valid_explanation = ""
    sound = None
    sound_explanation = ""
    
    # Parse performance analysis section
    for line in performance_part.splitlines():
        line = line.strip()
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

    # Convert logical expression to token list
    converted_tokens = convert_logical_expression(logical_expr)
    
    # Construct and return the result
    return {
        "logic_expression": logical_expr,
        "converted_logical_expression": converted_tokens,
        "performance": {
            "valid": valid,
            "valid_explanation": valid_explanation,
            "sound": sound,
            "sound_explanation": sound_explanation
        }
    }

class LogicChainService:
    def __init__(self):
        """Initialize the Logic Chain Service with OpenAI client"""
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        self.conversation_contexts = {}  # Store context expressions for conversations

    async def get_response(self, prompt: str) -> str:
        """
        Get response from OpenAI API.
        
        Args:
            prompt: The input prompt for the language model
            
        Returns:
            The generated response text
            
        Raises:
            Exception: If there's an error in getting the LLM response
        """
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=500
            )
            return response.choices[0].message.content
        except Exception as e:
            raise Exception(f"Error in getting LLM response: {str(e)}")

    async def analyze_logic(self, sentence: str, previous_context_expressions: list = None) -> LogicChain:
        """
        Analyze the logical structure of a sentence.
        
        Args:
            sentence: The sentence to analyze
            previous_context_expressions: List of previous logical expressions for context
            
        Returns:
            A LogicChain object containing:
            - logic_expression: The logical expression string
            - converted_logical_expression: List of tokens
            - performance: LogicalPerformance object with validity and soundness analysis
        """
        # Prepare analysis instructions with context if available
        additional_instructions = ""
        if previous_context_expressions and len(previous_context_expressions) > 0:
            previous_context_str = "Previous Logical Expressions:\n"
            for expr in previous_context_expressions:
                previous_context_str += f"{expr}\n"
            additional_instructions = previous_context_str + "\n" + COMMON_INSTRUCTIONS + "\nNow, please integrate the previous analysis with the new sentence and analyze it."
        else:
            additional_instructions = COMMON_INSTRUCTIONS

        # Generate the analysis prompt
        prompt = PROMPT_TEMPLATE.format(additional_instructions=additional_instructions, sentence=sentence)

        # Get and parse the LLM response
        raw_response = await self.get_response(prompt)
        result = parse_llm_output(raw_response, sentence)
        
        # Convert to LogicChain model
        return LogicChain(
            logic_expression=result.get("logic_expression", ""),
            converted_logical_expression=result.get("converted_logical_expression", []),
            performance=LogicalPerformance(
                valid=result.get("performance", {}).get("valid", False),
                valid_explanation=result.get("performance", {}).get("valid_explanation", ""),
                sound=result.get("performance", {}).get("sound", False),
                sound_explanation=result.get("performance", {}).get("sound_explanation", "")
            )
        )

# Initialize the Logic Chain Service
logic_chain_service = LogicChainService() 