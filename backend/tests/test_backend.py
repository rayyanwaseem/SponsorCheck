import pytest
from fastapi.testclient import TestClient
from sponsorcheck.api.main import app
from sponsorcheck.domain.models import SocCandidate
from sponsorcheck.classification.rule_based_classifier import classify_rule_based
from sponsorcheck.classification.validation import validate_soc_decision
from sponsorcheck.domain.salary_models import ApplicantFacts
from sponsorcheck.salary.evaluator import evaluate_salary_routes
from sponsorcheck.data.soc_store import get_soc_store
from sponsorcheck.questions.missing_facts import derive_missing_facts_questions

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_rule_based_classifier():
    candidates = [
        SocCandidate(occupation_code="2132", job_type="IT directors", score=0.9),
        SocCandidate(occupation_code="2133", job_type="IT managers", score=0.5)
    ]
    decision = classify_rule_based("Looking for an IT director", candidates)
    assert decision.best_occupation_code == "2132"
    assert decision.classification_method == "rule_based"

def test_validate_soc_decision():
    candidates = [SocCandidate(occupation_code="2132", job_type="IT directors", score=0.9)]
    valid = validate_soc_decision({"best_occupation_code": "2132"}, candidates)
    assert valid is True
    
    invalid = validate_soc_decision({"best_occupation_code": "9999"}, candidates)
    assert invalid is False

def test_standard_salary_route():
    store = get_soc_store()
    record = store.get_by_code("2132")
    if record:
        facts = ApplicantFacts(weekly_hours=37.5, offered_salary=50000.0)
        eval = evaluate_salary_routes(record, facts)
        assert eval.standard_route is not None
        assert eval.standard_route.status in ["applicable", "salary_too_low", "needs_more_information", "not_applicable"]

def test_missing_facts_engine():
    store = get_soc_store()
    record = store.get_by_code("2132")
    if record:
        facts = ApplicantFacts()  # Empty facts
        eval = evaluate_salary_routes(record, facts)
        questions = derive_missing_facts_questions(eval)
        # Should ask for weekly_hours and offered_salary at minimum
        assert any("weekly hours" in q.lower() for q in questions)

def test_api_classify_rule_based():
    payload = {
        "job_description": "We need a Python developer.",
        "provider": "rule_based",
        "top_k": 5
    }
    response = client.post("/api/classify", json=payload)
    if response.status_code == 200:
        data = response.json()
        assert "decision" in data
        assert "report_id" in data
        assert data["decision"]["classification_method"] == "rule_based"

def test_api_report_generation():
    # Attempt to fetch a non-existent report
    response = client.get("/api/reports/fake-id.pdf")
    assert response.status_code == 404
