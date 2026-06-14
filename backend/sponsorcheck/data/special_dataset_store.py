from typing import Dict, Any
from sponsorcheck.data.loaders import load_special_datasets

class SpecialDatasetStore:
    _instance = None

    def __init__(self):
        self.datasets: Dict[str, Any] = load_special_datasets()

    @classmethod
    def get_instance(cls) -> "SpecialDatasetStore":
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
        
    def get_dataset(self, dataset_name: str) -> Any:
        return self.datasets.get(dataset_name)

def get_special_dataset_store() -> SpecialDatasetStore:
    return SpecialDatasetStore.get_instance()
