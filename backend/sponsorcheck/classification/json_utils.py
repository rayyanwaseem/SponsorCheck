import json
import re
from typing import Dict, Any

def extract_json_from_text(text: str) -> Dict[str, Any]:
    # Try to find a JSON block
    match = re.search(r'```(?:json)?(.*?)```', text, re.DOTALL)
    if match:
        json_str = match.group(1).strip()
    else:
        # Fallback to finding the first { and last }
        start = text.find('{')
        end = text.rfind('}')
        if start != -1 and end != -1:
            json_str = text[start:end+1]
        else:
            json_str = text
            
    try:
        return json.loads(json_str)
    except json.JSONDecodeError as e:
        raise ValueError(f"Failed to parse JSON: {e}. Raw text: {text}")
