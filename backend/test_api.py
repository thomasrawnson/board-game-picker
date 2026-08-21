from fastapi.testclient import TestClient

from api.main import app, get_game_service
from models.game import Game


def test_get_game_returns_game():
    class FakeGameService:
        def get_game(self, bgg_id: int):
            return Game(
                bgg_id=bgg_id,
                name="Gloomhaven",
                year_published=2017,
                min_players=1,
                max_players=4,
                complexity=3.86,
                rating=8.5,
            )

    app.dependency_overrides[get_game_service] = (
        lambda: FakeGameService()
    )

    try:
        client = TestClient(app)

        response = client.get("/games/174430")

        assert response.status_code == 200

        data = response.json()

        assert data["bgg_id"] == 174430
        assert data["name"] == "Gloomhaven"
        assert data["min_players"] == 1
        assert data["max_players"] == 4

    finally:
        app.dependency_overrides.clear()

def test_get_missing_game_returns_404():
    class FakeGameService:
        def get_game(self, bgg_id: int):
            return None

    app.dependency_overrides[get_game_service] = (
        lambda: FakeGameService()
    )

    client = TestClient(app)

    response = client.get("/games/999999")

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Game not found"
    }

    app.dependency_overrides.clear()