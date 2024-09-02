import sys
import os
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "This is the Tac Tac Toe API."}

def test_join_lobby():
    response = client.post("/lobby/join?player_name=Chaz")
    assert response.status_code == 200
    assert "player_id" in response.json()
    assert response.json()["message"] == "Chaz joined the lobby"

def test_get_players():
    response = client.get("/lobby/players")
    assert response.status_code == 200
    assert "players" in response.json()

def test_challenge_player():
    # First, join two players to the lobby
    response1 = client.post("/lobby/join?player_name=Player1")
    player1_id = response1.json()["player_id"]

    response2 = client.post("/lobby/join?player_name=Player2")
    player2_id = response2.json()["player_id"]

    # Now, Player1 challenges Player2
    response = client.post(f"/lobby/challenge?challenger_id={player1_id}&challenged_player_id={player2_id}")
    assert response.status_code == 200
    assert response.json()["message"] == f"Player {player1_id} challenged player {player2_id}"
