from typing import Dict, Any
from sponsorcheck.data.loaders import load_gap_analysis

class MetadataStore:
    _instance = None

    def __init__(self):
        self.gap_analysis: Dict[str, Any] = load_gap_analysis()

    @classmethod
    def get_instance(cls) -> "MetadataStore":
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

def get_metadata_store() -> MetadataStore:
    return MetadataStore.get_instance()
