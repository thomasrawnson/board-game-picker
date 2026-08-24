from sqlalchemy import func
from sqlalchemy.orm import Session

from database.models import Game, Play
from models.collection_insights import (
    GamePlaySummary,
    LastPlayedGame,
)


class InsightsRepository:
    def __init__(self, db: Session):
        self.db = db

    def total_owned_games(self) -> int:
        return (
            self.db.query(func.count(Game.id))
            .filter(Game.owned.is_(True))
            .scalar()
            or 0
        )

    def total_plays(self) -> int:
        return (
            self.db.query(func.count(Play.id))
            .scalar()
            or 0
        )

    def get_most_played(self) -> GamePlaySummary | None:
        result = (
            self.db.query(
                Game.bgg_id,
                Game.name,
                func.count(Play.id).label("play_count"),
            )
            .join(Play, Play.game_id == Game.id)
            .group_by(
                Game.id,
                Game.bgg_id,
                Game.name,
            )
            .order_by(
                func.count(Play.id).desc(),
                Game.name,
            )
            .first()
        )

        if result is None:
            return None

        return GamePlaySummary(
            bgg_id=result.bgg_id,
            name=result.name,
            play_count=result.play_count,
        )

    def get_last_played(self) -> LastPlayedGame | None:
        result = (
            self.db.query(
                Game.bgg_id,
                Game.name,
                Play.played_at,
            )
            .join(Play, Play.game_id == Game.id)
            .order_by(Play.played_at.desc())
            .first()
        )

        if result is None:
            return None

        return LastPlayedGame(
            bgg_id=result.bgg_id,
            name=result.name,
            played_at=result.played_at,
        )

    def never_played_count(self) -> int:
        return (
            self.db.query(func.count(Game.id))
            .outerjoin(
                Play,
                Play.game_id == Game.id,
            )
            .filter(
                Game.owned.is_(True),
                Play.id.is_(None),
            )
            .scalar()
            or 0
        )