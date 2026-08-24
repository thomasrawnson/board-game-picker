import json

from bgstats.play_parser import (
    parse_bgstats_plays,
)


def test_parse_bgstats_plays():
    export = {
        "games": [
            {
                "id": 1,
                "bggId": 36218,
                "name": "Dominion",
            },
        ],
        "plays": [
            {
                "uuid": "play-123",
                "ignored": False,
                "playDate": (
                    "2025-05-10 19:30:00"
                ),
                "durationMin": 53,
                "gameRefId": 1,
                "playerScores": [
                    {"playerRefId": 1},
                    {"playerRefId": 2},
                    {"playerRefId": 3},
                ],
            },
        ],
    }

    plays = parse_bgstats_plays(
        json.dumps(export)
    )

    assert len(plays) == 1

    play = plays[0]

    assert play.source_play_id == "play-123"
    assert play.bgg_id == 36218
    assert play.player_count == 3
    assert play.duration_minutes == 53
    assert play.played_at.year == 2025