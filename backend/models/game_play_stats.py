from dataclasses import dataclass
from datetime import datetime


@dataclass
class GamePlayStats:
    bgg_id: int
    play_count: int
    last_played_at: datetime | None