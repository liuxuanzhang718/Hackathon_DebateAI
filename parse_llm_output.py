import re

def parse_llm_output(raw_text: str, original_text: str) -> dict:
    """
    Parse the LLM output based on delimiters to construct a JSON structure that meets the requirements.
    It is assumed that the LLM output contains the following sections:
      - Original Text: ...
      - Premises: Each line is in the format "- pX: premise text"
      - Conclusions: Each conclusion starts with a line in the format "- cX: conclusion text", 
                     followed by additional lines that may include "Expression:", "From:" and "To:" information.
      - Relations: Each line is in the format "- pX to pY: relation type"
      - Fallacies: Each line is in the format "- fallacy_type: description"
    """
    result = {
        "text": original_text,
        "logic": {
            "premises": [],
            "conclusions": [],
            "relations": [],
            "fallacies": []
        }
    }
    
    # Split the raw text into lines
    lines = raw_text.splitlines()
    current_section = None
    current_conclusion = None

    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        # Determine the current section based on keywords
        if line.lower().startswith("original text:"):
            # Optionally skip or verify the original text
            continue
        elif line.lower().startswith("premises:"):
            current_section = "premises"
            continue
        elif line.lower().startswith("conclusions:"):
            current_section = "conclusions"
            continue
        elif line.lower().startswith("relations:"):
            current_section = "relations"
            continue
        elif line.lower().startswith("fallacies:"):
            current_section = "fallacies"
            continue

        if current_section == "premises":
            # Parse lines in the format: - pX: premise text
            if line.startswith("-"):
                parts = line[1:].strip().split(":", 1)
                if len(parts) == 2:
                    pid = parts[0].strip()
                    ptext = parts[1].strip()
                    result["logic"]["premises"].append({
                        "id": pid,
                        "text": ptext
                    })
        elif current_section == "conclusions":
            # If the line starts with "-", it denotes a new conclusion
            if line.startswith("-"):
                parts = line[1:].strip().split(":", 1)
                if len(parts) == 2:
                    cid = parts[0].strip()
                    ctext = parts[1].strip()
                    current_conclusion = {
                        "id": cid,
                        "text": ctext,
                        "expr": "",
                        "from": [],
                        "to": []
                    }
                    result["logic"]["conclusions"].append(current_conclusion)
            else:
                # Lines not starting with "-" may contain Expression, From, or To information
                lower_line = line.lower()
                if "expression:" in lower_line:
                    # Parse the Expression: ...
                    expr = line.split(":", 1)[1].strip()
                    if current_conclusion is not None:
                        current_conclusion["expr"] = expr
                elif lower_line.startswith("from:"):
                    from_ids = line.split(":", 1)[1].strip()
                    if current_conclusion is not None:
                        # Split multiple IDs separated by commas
                        current_conclusion["from"] = [fid.strip() for fid in from_ids.split(",") if fid.strip()]
                elif lower_line.startswith("to:"):
                    to_ids = line.split(":", 1)[1].strip()
                    if current_conclusion is not None:
                        current_conclusion["to"] = [tid.strip() for tid in to_ids.split(",") if tid.strip()]
        elif current_section == "relations":
            # Parse lines in the format: - pX to pY: relation type
            if line.startswith("-"):
                content = line[1:].strip()
                if ":" in content and "to" in content:
                    rel_part, rel_type = content.split(":", 1)
                    if "to" in rel_part:
                        from_part, to_part = rel_part.split("to", 1)
                        relation = {
                            "from": from_part.strip(),
                            "to": to_part.strip(),
                            "type": rel_type.strip()
                        }
                        result["logic"]["relations"].append(relation)
        elif current_section == "fallacies":
            # Parse lines in the format: - fallacy_type: description
            if line.startswith("-"):
                parts = line[1:].strip().split(":", 1)
                if len(parts) == 2:
                    ftype = parts[0].strip()
                    fdesc = parts[1].strip()
                    result["logic"]["fallacies"].append({
                        "type": ftype,
                        "description": fdesc
                    })
                    
    return result
