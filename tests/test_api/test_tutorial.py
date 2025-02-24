import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_get_next_question():
    response = client.get("/tutorial/next-question")
    assert response.status_code == 200
    data = response.json()
    assert "example" in data
    assert "question" in data
    assert isinstance(data["example"], list)
    assert isinstance(data["question"], list)

def test_submit_correct_answer():
    response = client.post(
        "/tutorial/answer",
        json={
            "question_id": 1,
            "user_answer": False
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "correct" in data
    assert data["correct"] is True

def test_submit_wrong_answer():
    response = client.post(
        "/tutorial/answer",
        json={
            "question_id": 1,
            "user_answer": True
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "correct" in data
    assert data["correct"] is False
    assert "explanation" in data

def test_submit_invalid_question_id():
    response = client.post(
        "/tutorial/answer",
        json={
            "question_id": 999,
            "user_answer": True
        }
    )
    assert response.status_code == 400
    assert "Invalid question ID" in response.json()["detail"]

def test_submit_invalid_request_format():
    response = client.post(
        "/tutorial/answer",
        json={
            "invalid_field": "value"
        }
    )
    assert response.status_code == 422  # Validation Error 