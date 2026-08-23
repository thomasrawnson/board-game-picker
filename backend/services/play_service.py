from models.play import Play
from repositories.play_repository import PlayRepository


class PlayService:
    def __init__(self, repository: PlayRepository):
        self.repository = repository

    def record_play(
        self,
        bgg_id: int,
        player_count: int,
    ) -> Play | None:
        return self.repository.create(
            bgg_id=bgg_id,
            player_count=player_count,
        )