from sqlalchemy.orm import Session

from database.models import Game as DatabaseGame
from models.game import Game as DomainGame


class GameRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_bgg_id(self, bgg_id: int) -> DomainGame | None:
        database_game = (
            self.db.query(DatabaseGame)
            .filter(DatabaseGame.bgg_id == bgg_id)
            .first()
        )

        if database_game is None:
            return None

        return self._to_domain(database_game)

    def create(self, game: DomainGame) -> DomainGame:
        database_game = DatabaseGame(
            bgg_id=game.bgg_id,
            name=game.name,
            year_published=game.year_published,
            min_players=game.min_players,
            max_players=game.max_players,
            rating=game.rating,
            complexity=game.complexity,
            thumbnail=game.thumbnail_url,
        )

        self.db.add(database_game)
        self.db.commit()
        self.db.refresh(database_game)

        return self._to_domain(database_game)

    @staticmethod
    def _to_domain(database_game: DatabaseGame) -> DomainGame:
        return DomainGame(
            bgg_id=database_game.bgg_id,
            name=database_game.name,
            year_published=database_game.year_published,
            min_players=database_game.min_players,
            max_players=database_game.max_players,
            rating=database_game.rating,
            complexity=database_game.complexity,
            thumbnail_url=database_game.thumbnail,
        )