import json

from dataclasses import dataclass
from datetime import datetime, timezone


@dataclass(frozen=True)
class BGStatsPlay:
    source_play_id: str
    bgg_id: int
    player_count: int
    played_at: datetime
    duration_minutes: int | None


def parse_bgstats_plays(
    json_text: str,
) -> list[BGStatsPlay]:
    data = json.loads(json_text)

    games_by_ref_id = {
        game["id"]: game["bggId"]
        for game in data.get("games", [])
        if game.get("id") is not None
        and game.get("bggId")
    }

    plays: list[BGStatsPlay] = []

    for item in data.get("plays", []):
        if item.get("ignored"):
            continue

        source_play_id = item.get("uuid")

        if not source_play_id:
            continue

        game_ref_id = item.get("gameRefId")
        bgg_id = games_by_ref_id.get(game_ref_id)

        if not bgg_id:
            continue

        play_date = item.get("playDate")

        if not play_date:
            continue

        player_scores = item.get("playerScores") or []
        player_count = len(player_scores)

        if player_count == 0:
            continue

        played_at = _parse_datetime(play_date)

        plays.append(
            BGStatsPlay(
                source_play_id=source_play_id,
                bgg_id=bgg_id,
                player_count=player_count,
                played_at=played_at,
                duration_minutes=item.get(
                    "durationMin"
                ),
            )
        )

    return plays


def _parse_datetime(value: str) -> datetime:
    parsed = datetime.fromisoformat(
        value.replace("Z", "+00:00")
    )

    if parsed.tzinfo is None:
        parsed = parsed.replace(
            tzinfo=timezone.utc
        )

    return parsed