from typing import Dict, Any
from sponsorcheck.data.loaders import load_salary_rules

class SalaryRuleStore:
    _instance = None

    def __init__(self):
        self.rules: Dict[str, Any] = load_salary_rules()

    @classmethod
    def get_instance(cls) -> "SalaryRuleStore":
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
        
    def get_rules(self) -> Dict[str, Any]:
        return self.rules

def get_salary_rule_store() -> SalaryRuleStore:
    return SalaryRuleStore.get_instance()
