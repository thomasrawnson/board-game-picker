from sqlalchemy.orm import Session

from database.models import Game as DatabaseGame
from database.models import Play as DatabasePlay
from models.play import Play as DomainPlay


class PlayRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(
        self,
        bgg_id: int,
        player_count: int,
    ) -> DomainPlay | None:
        database_game = (
            self.db.query(DatabaseGame)
            .filter(DatabaseGame.bgg_id == bgg_id)
            .first()
        )

        if database_game is None:
            return None

        database_play = DatabasePlay(
            game_id=database_game.id,
            player_count=player_count,
        )

        self.db.add(database_play)
        self.db.commit()
        self.db.refresh(database_play)

        return DomainPlay(
            id=database_play.id,
            bgg_id=database_game.bgg_id,
            player_count=database_play.player_count,
            played_at=database_play.played_at,
        )