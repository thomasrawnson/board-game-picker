from bgg.collection import enrich_collection
from models.game import Game


def test_collection_is_enriched():

    collection = [
        Game(
            bgg_id=174430,
            name="Gloomhaven: Jaws of the Lion",
            owned=True,
        )
    ]

    metadata = {
        174430: Game(
            bgg_id=174430,
            name="Gloomhaven: Jaws of the Lion",
            year_published=2020,
            min_players=1,
            max_players=4,
            min_play_time=30,
            max_play_time=120,
            complexity=3.85,
            rating=8.4,
            image_url="https://example.com/gloomhaven.jpg",
            categories=["Adventure"],
            mechanics=["Cooperative Game"],
        )
    }

    result = enrich_collection(collection, metadata)

    game = result[0]

    assert game.bgg_id == 174430
    assert game.name == "Gloomhaven: Jaws of the Lion"

    assert game.min_players == 1
    assert game.max_players == 4

    assert game.min_play_time == 30
    assert game.max_play_time == 120

    assert game.complexity == 3.85
    assert game.rating == 8.4

    assert game.categories == ["Adventure"]
    assert game.mechanics == ["Cooperative Game"]


def test_missing_metadata_does_not_remove_game():

    collection = [
        Game(
            bgg_id=123,
            name="Unknown Game",
            owned=True,
        )
    ]

    metadata = {}

    result = enrich_collection(collection, metadata)

    assert len(result) == 1
    assert result[0].bgg_id == 123
    assert result[0].name == "Unknown Game"