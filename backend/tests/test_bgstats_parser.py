from pathlib import Path

from bgstats.parser import parse_bgstats_export


FIXTURE = (
    Path(__file__).parent
    / "fixtures"
    / "bgstats_collection.json"
)


def test_parse_bgstats_export():
    json_text = FIXTURE.read_text(encoding="utf-8")

    games = parse_bgstats_export(json_text)

    assert len(games) == 2

    terraforming_mars = games[0]

    assert terraforming_mars.bgg_id == 167791
    assert terraforming_mars.name == "Terraforming Mars"
    assert terraforming_mars.year_published == 2016

    assert terraforming_mars.min_players == 1
    assert terraforming_mars.max_players == 5

    assert terraforming_mars.min_play_time == 120
    assert terraforming_mars.max_play_time == 120

    assert terraforming_mars.owned is True


def test_parse_bgstats_export_detects_not_owned():
    json_text = FIXTURE.read_text(encoding="utf-8")

    games = parse_bgstats_export(json_text)

    dune = games[1]

    assert dune.bgg_id == 316554
    assert dune.name == "Dune: Imperium"
    assert dune.owned is False