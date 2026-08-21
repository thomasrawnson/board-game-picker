from models.game import Game
from services.collection_service import CollectionService


GAME_XML = """
<items>
    <item type="boardgame" id="174430">
        <name type="primary" value="Gloomhaven"/>
        <yearpublished value="2017"/>

        <minplayers value="1"/>
        <maxplayers value="4"/>

        <minplaytime value="60"/>
        <maxplaytime value="120"/>

        <image>https://example.com/image.jpg</image>
        <thumbnail>https://example.com/thumb.jpg</thumbnail>

        <statistics>
            <ratings>
                <average value="8.5"/>
                <averageweight value="3.8"/>
            </ratings>
        </statistics>

        <link type="boardgamecategory" value="Adventure"/>
        <link type="boardgamecategory" value="Fantasy"/>
        <link type="boardgamemechanic" value="Cooperative Game"/>
    </item>
</items>
"""


def test_sync_game_creates_new_game():
    class FakeBGGClient:
        def get_game(self, bgg_id):
            return GAME_XML

    class FakeRepository:
        def get_by_bgg_id(self, bgg_id):
            return None

        def create(self, game):
            return game

    service = CollectionService(
        FakeBGGClient(),
        FakeRepository(),
    )

    game = service.sync_game(174430)

    assert game.bgg_id == 174430
    assert game.name == "Gloomhaven"


def test_sync_game_updates_existing_game():
    class FakeBGGClient:
        def get_game(self, bgg_id):
            return GAME_XML

    class FakeRepository:
        def get_by_bgg_id(self, bgg_id):
            return Game(
                bgg_id=174430,
                name="Old Name",
            )

        def update(self, game):
            return game

    service = CollectionService(
        FakeBGGClient(),
        FakeRepository(),
    )

    game = service.sync_game(174430)

    assert game.bgg_id == 174430
    assert game.name == "Gloomhaven"