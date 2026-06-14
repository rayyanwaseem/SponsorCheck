class SponsorCheckError(Exception):
    pass

class DataLoadError(SponsorCheckError):
    pass

class ModelClassificationError(SponsorCheckError):
    pass

class SalaryEvaluationError(SponsorCheckError):
    pass
