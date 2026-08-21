from database.connection import SessionLocal
from database.models import Game as DatabaseGame
from models.game import Game as DomainGame
from repositories.game_repository import GameRepository


def test_get_game_by_bgg_id():
    db = SessionLocal()

    try:
        test_game = DatabaseGame(
            bgg_id=174430,
            name="Gloomhaven",
            year_published=2017,
            min_players=1,
            max_players=4,
            rating=8.4,
            complexity=3.9,
            thumbnail="https://example.com/gloomhaven.jpg",
        )

        db.add(test_game)
        db.commit()

        repository = GameRepository(db)

        game = repository.get_by_bgg_id(174430)

        assert game is not None
        assert game.bgg_id == 174430
        assert game.name == "Gloomhaven"
        assert game.rating == 8.4

    finally:
        db.query(DatabaseGame).filter(
            DatabaseGame.bgg_id == 174430
        ).delete()
        db.commit()
        db.close()


def test_create_game():
    db = SessionLocal()

    try:
        repository = GameRepository(db)

        game = DomainGame(
            bgg_id=999001,
            name="Test Board Game",
            year_published=2026,
            min_players=2,
            max_players=4,
            rating=7.5,
            complexity=2.5,
            thumbnail_url="https://example.com/test.jpg",
        )

        created_game = repository.create(game)

        assert created_game.bgg_id == 999001
        assert created_game.name == "Test Board Game"
        assert created_game.rating == 7.5

        stored_game = (
            db.query(DatabaseGame)
            .filter(DatabaseGame.bgg_id == 999001)
            .first()
        )

        assert stored_game is not None
        assert stored_game.name == "Test Board Game"

    finally:
        db.query(DatabaseGame).filter(
            DatabaseGame.bgg_id == 999001
        ).delete()
        db.commit()
        db.close()