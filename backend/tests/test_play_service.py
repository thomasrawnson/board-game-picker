from datetime import datetime, timezone

from models.play import Play
from services.play_service import PlayService


class FakePlayRepository:
    def __init__(self):
        self.created = None

    def create(
        self,
        bgg_id: int,
        player_count: int,
    ) -> Play:
        self.created = (bgg_id, player_count)

        return Play(
            id=1,
            bgg_id=bgg_id,
            player_count=player_count,
            played_at=datetime.now(timezone.utc),
        )


def test_record_play_uses_repository():
    repository = FakePlayRepository()
    service = PlayService(repository)

    play = service.record_play(
        bgg_id=167791,
        player_count=2,
    )

    assert repository.created == (167791, 2)
    assert play.bgg_id == 167791
    assert play.player_count == 2