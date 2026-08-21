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

    try:
        client = TestClient(app)

        response = client.get("/games/999999")

        assert response.status_code == 404
        assert response.json() == {
            "detail": "Game not found"
        }

    finally:
        app.dependency_overrides.clear()


def test_create_game():
    class FakeGameService:
        def create_game(self, game):
            return game

    app.dependency_overrides[get_game_service] = (
        lambda: FakeGameService()
    )

    try:
        client = TestClient(app)

        response = client.post(
            "/games",
            json={
                "bgg_id": 999999,
                "name": "Test Game",
                "year_published": 2026,
                "min_players": 2,
                "max_players": 4,
                "rating": 8.0,
                "complexity": 2.5,
            },
        )

        assert response.status_code == 201

        data = response.json()

        assert data["bgg_id"] == 999999
        assert data["name"] == "Test Game"
        assert data["min_players"] == 2
        assert data["max_players"] == 4

    finally:
        app.dependency_overrides.clear()


def test_create_game_rejects_invalid_rating():
    class FakeGameService:
        def create_game(self, game):
            return game

    app.dependency_overrides[get_game_service] = (
        lambda: FakeGameService()
    )

    try:
        client = TestClient(app)

        response = client.post(
            "/games",
            json={
                "bgg_id": 999999,
                "name": "Test Game",
                "rating": 15,
            },
        )

        assert response.status_code == 422

    finally:
        app.dependency_overrides.clear()

def test_get_games():
    class FakeGameService:
        def get_games(self):
            return [
                Game(bgg_id=174430, name="Gloomhaven"),
                Game(bgg_id=167791, name="Terraforming Mars"),
            ]

    app.dependency_overrides[get_game_service] = (
        lambda: FakeGameService()
    )

    try:
        client = TestClient(app)

        response = client.get("/games")

        assert response.status_code == 200

        data = response.json()

        assert len(data) == 2
        assert data[0]["name"] == "Gloomhaven"
        assert data[1]["name"] == "Terraforming Mars"

    finally:
        app.dependency_overrides.clear()

def test_update_game():
    class FakeGameService:
        def update_game(self, game):
            return game

    app.dependency_overrides[get_game_service] = (
        lambda: FakeGameService()
    )

    try:
        client = TestClient(app)

        response = client.put(
            "/games/174430",
            json={
                "bgg_id": 174430,
                "name": "Gloomhaven Updated",
                "rating": 9.0,
            },
        )

        assert response.status_code == 200

        data = response.json()

        assert data["bgg_id"] == 174430
        assert data["name"] == "Gloomhaven Updated"
        assert data["rating"] == 9.0

    finally:
        app.dependency_overrides.clear()

def test_delete_game():
    class FakeGameService:
        def delete_game(self, bgg_id):
            return True

    app.dependency_overrides[get_game_service] = (
        lambda: FakeGameService()
    )

    try:
        client = TestClient(app)

        response = client.delete("/games/174430")

        assert response.status_code == 200
        assert response.json() == {
            "message": "Game deleted"
        }

    finally:
        app.dependency_overrides.clear()

def test_update_missing_game_returns_404():
    class FakeGameService:
        def update_game(self, game):
            return None

    app.dependency_overrides[get_game_service] = (
        lambda: FakeGameService()
    )

    try:
        client = TestClient(app)

        response = client.put(
            "/games/999999",
            json={
                "bgg_id": 999999,
                "name": "Missing Game",
            },
        )

        assert response.status_code == 404

    finally:
        app.dependency_overrides.clear()

def test_delete_missing_game_returns_404():
    class FakeGameService:
        def delete_game(self, bgg_id):
            return False

    app.dependency_overrides[get_game_service] = (
        lambda: FakeGameService()
    )

    try:
        client = TestClient(app)

        response = client.delete("/games/999999")

        assert response.status_code == 404

    finally:
        app.dependency_overrides.clear()