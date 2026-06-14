from sponsorcheck.domain.models import SocRecord
from sponsorcheck.domain.salary_models import ApplicantFacts, RouteResult

class RouteEvaluator:
    route_id: str = "base"
    route_label: str = "Base Route"

    def evaluate(self, record: SocRecord, facts: ApplicantFacts) -> RouteResult:
        raise NotImplementedError
