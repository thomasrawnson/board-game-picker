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
    
    def get_all(self) -> list[DomainGame]:
        database_games = (
            self.db.query(DatabaseGame)
            .order_by(DatabaseGame.name)
            .all()
        )

        return [
            self._to_domain(game)
            for game in database_games
        ]

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

    def update(self, game: DomainGame) -> DomainGame | None:
        database_game = (
            self.db.query(DatabaseGame)
            .filter(DatabaseGame.bgg_id == game.bgg_id)
            .first()
        )

        if database_game is None:
            return None

        database_game.name = game.name
        database_game.year_published = game.year_published
        database_game.min_players = game.min_players
        database_game.max_players = game.max_players
        database_game.rating = game.rating
        database_game.complexity = game.complexity
        database_game.thumbnail = game.thumbnail_url

        self.db.commit()
        self.db.refresh(database_game)

        return self._to_domain(database_game)

    def delete(self, bgg_id: int) -> bool:
        database_game = (
            self.db.query(DatabaseGame)
            .filter(DatabaseGame.bgg_id == bgg_id)
            .first()
        )

        if database_game is None:
            return False

        self.db.delete(database_game)
        self.db.commit()

        return True

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