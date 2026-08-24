from dataclasses import dataclass
from datetime import datetime


@dataclass
class GamePlaySummary:
    bgg_id: int
    name: str
    play_count: int


@dataclass
class LastPlayedGame:
    bgg_id: int
    name: str
    played_at: datetime


@dataclass
class CollectionInsights:
    total_games: int
    total_plays: int
    most_played: GamePlaySummary | None
    last_played: LastPlayedGame | None
    never_played_count: int