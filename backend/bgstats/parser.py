import json

from models.game import Game


def parse_bgstats_export(json_text: str) -> list[Game]:
    data = json.loads(json_text)

    games = []

    for item in data.get("games", []):
        game = Game(
            bgg_id=item["bggId"],
            name=item.get("name") or item.get("bggName") or "",
            year_published=item.get("bggYear"),
            min_players=item.get("minPlayerCount"),
            max_players=item.get("maxPlayerCount"),
            min_play_time=item.get("minPlayTime"),
            max_play_time=item.get("maxPlayTime"),
            owned=_is_owned(item),
            image_url=item.get("urlImage"),
            thumbnail_url=item.get("urlThumb"),
        )

        games.append(game)

    return games


def _is_owned(item: dict) -> bool:
    copies = item.get("copies", [])

    return any(
        copy.get("statusOwned") == 1
        for copy in copies
    )