from typing import Dict, Any

class ReportStore:
    _instance = None
    
    def __init__(self):
        self.reports: Dict[str, Any] = {}
        
    @classmethod
    def get_instance(cls) -> "ReportStore":
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
        
    def save(self, report_id: str, data: Any):
        self.reports[report_id] = data
        
    def get(self, report_id: str) -> Any:
        return self.reports.get(report_id)

def get_report_store() -> ReportStore:
    return ReportStore.get_instance()
