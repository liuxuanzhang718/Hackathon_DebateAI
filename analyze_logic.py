import spacy

nlp = spacy.load("en_core_web_sm")

def analyze_logic(sentence, llm_client):
    
    doc = nlp(sentence)
    structure = [
        {
            "text": token.text,
            "lemma": token.lemma_,
            "pos": token.pos_,
            "dependency": token.dep_,
            "head": token.head.text
        }
        for token in doc
    ]
    
    prompt = f"Convert this sentence into symbolic logic and identify logical errors: {sentence}"
    logic_analysis = llm_client.get_response(prompt)
    
    return structure, logic_analysis

