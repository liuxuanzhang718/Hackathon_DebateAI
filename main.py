from config import get_llm_client
from analyze_logic import analyze_logic

if __name__ == "__main__":
    model_name = input("Enter LLM model (openai/deepseek/claude/gemini): ").strip().lower()
    
    llm = get_llm_client(model_name)

    # Example sentence
    sentences = [
        "If fuel cost is reduced, then air pollution is reduced.",
        "More electric vehicles will reduce fuel cost, thus reduce air pollution and carbon emissions to reduce global warming."
    ]

    for sentence in sentences:
        structure, logic_analysis = analyze_logic(sentence, llm)

        print("\n🔹 Sentence:\n", sentence)
        print("🔍 Syntactic Structure:")
        for token in structure:
            print(f"  - {token['text']} ({token['pos']}, {token['dependency']}) → {token['head']}")
        print("\n💡 Logical Analysis:\n", logic_analysis)
