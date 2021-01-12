import requests
import logging
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

logger = logging.getLogger(__name__)
PLAYER = "synapz"
URL = f"https://lichess.org/api/games/user/{PLAYER}"


def get_game_from_lichess() -> str:
    response = requests.get(URL, params={"max": 1, "analysed": False})
    return response.text


def test_post_game():
    data: str = get_game_from_lichess()
    logger.debug(data)
    r = client.post("/game", json={"pgn": "{" + data + "}"})
    assert r.status_code == 201


test_post_game()
