from typing import Dict, Optional, List
from sponsorcheck.data.loaders import load_soc_records
from sponsorcheck.domain.models import SocRecord

class SocStore:
    _instance = None

    def __init__(self):
        self.records_dict: Dict[str, SocRecord] = {}
        self.records_list: List[SocRecord] = []
        self._load_data()

    @classmethod
    def get_instance(cls) -> "SocStore":
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def _load_data(self):
        raw_data = load_soc_records()
        for item in raw_data:
            # Safely create a SocRecord
            record = SocRecord(**item)
            self.records_dict[record.occupation_code] = record
            self.records_list.append(record)

    def get_by_code(self, occupation_code: str) -> Optional[SocRecord]:
        return self.records_dict.get(occupation_code)
        
    def get_all(self) -> List[SocRecord]:
        return self.records_list

def get_soc_store() -> SocStore:
    return SocStore.get_instance()
