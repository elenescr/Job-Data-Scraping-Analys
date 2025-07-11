import pytest
from src.data.processors import clean_and_validate_jobs

def test_clean_and_validate_jobs_removes_invalid():
    dirty_jobs = [
        {"title": "", "company": "Test", "location": "Remote"},
        {"title": "Engineer", "company": "", "location": "Remote"},
        {"title": "Valid", "company": "ValidCo", "location": "Remote"}
    ]
    clean_jobs = clean_and_validate_jobs(dirty_jobs)
    assert len(clean_jobs) == 1
    assert clean_jobs[0]['title'] == "Valid"
    assert clean_jobs[0]['company'] == "ValidCo"
