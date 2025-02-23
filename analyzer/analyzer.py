# analyzer.py
import json
from analyze_logic import analyze_logic

class LogicAnalyzer:
    """
    LogicAnalyzer encapsulates the NLP analysis logic for debate arguments.
    It uses a provided LLM client to analyze a sentence and maintains a history of previous logical expressions.
    """
    def __init__(self, llm):
        """
        Initialize the LogicAnalyzer with the given LLM client.
        
        Parameters:
            llm: An object with a method get_response(prompt) that interfaces with the language model.
        """
        self.llm = llm
        self.previous_context_expressions = []  # List to store previous logical expression strings

    def analyze(self, sentence: str) -> dict:
        """
        Analyzes the logical structure of the provided sentence, integrating previous analyses if available.
        
        Parameters:
            sentence: The current input sentence to analyze.
        
        Returns:
            A dictionary containing the analysis result in JSON format.
        """
        analysis = analyze_logic(sentence, self.llm, self.previous_context_expressions)
        # Update the previous context with the new logical expression (if available)
        logical_expr = analysis.get("logical_expression", "")
        if logical_expr:
            self.previous_context_expressions.append(logical_expr)
        return analysis
