from datetime import datetime, timezone

from models.collection_insights import (
    GamePlaySummary,
    LastPlayedGame,
)
from services.insights_service import InsightsService


class FakeInsightsRepository:
    def total_owned_games(self):
        return 194

    def total_plays(self):
        return 12

    def get_most_played(self):
        return GamePlaySummary(
            bgg_id=167791,
            name="Terraforming Mars",
            play_count=4,
        )

    def get_last_played(self):
        return LastPlayedGame(
            bgg_id=167791,
            name="Terraforming Mars",
            played_at=datetime.now(timezone.utc),
        )

    def never_played_count(self):
        return 150


def test_get_collection_insights():
    service = InsightsService(
        FakeInsightsRepository()
    )

    insights = service.get_collection_insights()

    assert insights.total_games == 194
    assert insights.total_plays == 12

    assert insights.most_played is not None
    assert insights.most_played.name == "Terraforming Mars"
    assert insights.most_played.play_count == 4

    assert insights.last_played is not None
    assert insights.last_played.name == "Terraforming Mars"

    assert insights.never_played_count == 150