import os
import json
import pytest

def test_data_cleanliness():
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    data_dir = os.path.join(base_dir, "data")
    
    forbidden_terms = [
        "ChatGPT",
        "generated_from_uploaded_files",
        "datasets_from_uploaded_pages",
        "saved_file_name",
        "raw_saved_page_sections",
        "uploaded wording",
        "saved page wording",
        "uploaded page wording",
        "not uploaded",
        # "uploaded" by itself might be a generic term but based on prompt we check "uploaded" if it implies the provenance
    ]
    # Let's add "uploaded" as requested
    forbidden_terms.append("uploaded")
    
    json_files = [f for f in os.listdir(data_dir) if f.endswith(".json")]
    
    for filename in json_files:
        file_path = os.path.join(data_dir, filename)
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            # To avoid false positives on 'uploaded' if it happens to be a valid English word in a job description,
            # wait, the instruction says "fails if any JSON file contains ChatGPT, uploaded, generated_from_uploaded_files...".
            # So I must do a strict string matching check for these exact terms.
            content_lower = content.lower()
            
            for term in forbidden_terms:
                term_lower = term.lower()
                if term_lower in content_lower:
                    pytest.fail(f"File {filename} contains forbidden term: '{term}'")
