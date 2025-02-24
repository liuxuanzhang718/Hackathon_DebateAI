import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_start_conversation():
    response = client.post(
        "/agent-training/start",
        json={
            "topic_id": 1,
            "user_side": "supporting"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "conversation_id" in data
    assert "topic" in data
    assert data["topic"]["id"] == 1
    assert data["user_side"] == "supporting"

def test_start_conversation_invalid_topic():
    response = client.post(
        "/agent-training/start",
        json={
            "topic_id": 999,
            "user_side": "supporting"
        }
    )
    assert response.status_code == 400
    assert "Invalid topic ID" in response.json()["detail"]

def test_process_debate_round():
    # First create a conversation
    start_response = client.post(
        "/agent-training/start",
        json={
            "topic_id": 1,
            "user_side": "supporting"
        }
    )
    conversation_id = start_response.json()["conversation_id"]
    
    # Then submit a debate round
    response = client.post(
        f"/agent-training/round/{conversation_id}",
        json={
            "user_utterance": "Climate change is a serious issue because of rising global temperatures."
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "user_response" in data
    assert "ai_response" in data
    assert "round_id" in data

def test_process_debate_round_invalid_conversation():
    response = client.post(
        "/agent-training/round/invalid-id",
        json={
            "user_utterance": "Test argument"
        }
    )
    assert response.status_code == 404
    assert "Conversation not found" in response.json()["detail"]

def test_get_conversation_history():
    # Create a conversation and add a round
    start_response = client.post(
        "/agent-training/start",
        json={
            "topic_id": 1,
            "user_side": "supporting"
        }
    )
    conversation_id = start_response.json()["conversation_id"]
    
    client.post(
        f"/agent-training/round/{conversation_id}",
        json={
            "user_utterance": "Test argument"
        }
    )
    
    # Get history
    response = client.get(f"/agent-training/history/{conversation_id}")
    assert response.status_code == 200
    data = response.json()
    assert "conversation_id" in data
    assert "topic_id" in data
    assert "rounds" in data
    assert len(data["rounds"]) == 1

def test_get_logic_chain():
    # Create a conversation and add a round
    start_response = client.post(
        "/agent-training/start",
        json={
            "topic_id": 1,
            "user_side": "supporting"
        }
    )
    conversation_id = start_response.json()["conversation_id"]
    
    client.post(
        f"/agent-training/round/{conversation_id}",
        json={
            "user_utterance": "Test argument"
        }
    )
    
    # Get logic chain
    response = client.get(f"/agent-training/logic-chain/{conversation_id}")
    assert response.status_code == 200
    data = response.json()
    assert "topic" in data
    assert "logic_chains" in data
    assert len(data["logic_chains"]) == 1 