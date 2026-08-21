from database.connection import SessionLocal
from database.models import Game as DatabaseGame
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
        assert game.thumbnail_url == "https://example.com/gloomhaven.jpg"

    finally:
        db.query(DatabaseGame).filter(
            DatabaseGame.bgg_id == 174430
        ).delete()
        db.commit()
        db.close()