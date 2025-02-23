import os
import json
from config import get_llm_client
from analyzer import LogicAnalyzer  # Import the DebateAnalyzer class

if __name__ == "__main__":
    model_name = input("Enter LLM model (openai/deepseek): ").strip().lower()
    llm = get_llm_client(model_name)
    
    # Create an instance of LogicAnalyzer with the provided LLM client
    logic_analyzer = LogicAnalyzer(llm)
    
    # Determine the absolute path of test.json relative to the script's directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, "test.json")

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        sentence = data.get("text", "").strip()
        if not sentence:
            raise ValueError("Missing 'text' field in JSON file")
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        exit(1)

    # Analyze the current sentence using the LogicAnalyzer instance
    logic_analysis = logic_analyzer.analyze(sentence)
    print(json.dumps(logic_analysis, indent=2, ensure_ascii=False))

    output_path = os.path.join(script_dir, "output.json")
    try:
        with open(output_path, "w", encoding="utf-8") as out_file:
            json.dump(logic_analysis, out_file, indent=2, ensure_ascii=False)
        print(f"Analysis result written to {output_path}")
    except Exception as e:
        print(f"Error writing to output file: {e}")
