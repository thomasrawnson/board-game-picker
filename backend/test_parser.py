from pathlib import Path

from bgg.parser import parse_collection


FIXTURE = Path(__file__).parent / "tests" / "fixtures" / "bgg_collection.xml"


def test_parse_collection():
    xml = FIXTURE.read_text(encoding="utf-8")

    games = parse_collection(xml)

    assert len(games) == 2

    assert games[0].bgg_id == 174430
    assert games[0].name == "Gloomhaven: Jaws of the Lion"
    assert games[0].min_players == 1
    assert games[0].max_players == 4
    assert games[0].min_play_time == 30
    assert games[0].max_play_time == 120
    assert games[0].rating == 8.4
    assert games[0].owned is True


def test_parse_collection_handles_multiple_games():
    xml = FIXTURE.read_text(encoding="utf-8")

    games = parse_collection(xml)

    assert games[1].name == "Catan"
    assert games[1].bgg_id == 13