from enum import Enum

class RouteStatus(str, Enum):
    APPLICABLE = "applicable"
    NOT_APPLICABLE = "not_applicable"
    NEEDS_MORE_INFORMATION = "needs_more_information"
    SALARY_TOO_LOW = "salary_too_low"
    SOURCE_CHECK_REQUIRED = "source_check_required"
