import json
import os
from typing import Dict, Any, List

def load_json_file(filename: str) -> Any:
    # navigate from backend/sponsorcheck/data/loaders.py to data/
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    data_dir = os.path.join(base_dir, "data")
    file_path = os.path.join(data_dir, filename)
    
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Data file not found: {file_path}")
        
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

def load_soc_records() -> List[Dict[str, Any]]:
    # The enriched file might be a list or a dict containing a list.
    data = load_json_file("soc_records_enriched_v3.json")
    if isinstance(data, dict) and "soc_records" in data:
        return data["soc_records"]
    return data

def load_special_datasets() -> Dict[str, Any]:
    return load_json_file("special_salary_datasets_v3.json")

def load_salary_rules() -> Dict[str, Any]:
    return load_json_file("skilled_worker_salary_rules_v3.json")

