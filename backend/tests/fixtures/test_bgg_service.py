from bgg.client import BGGClient
from models.game import Game
from services.bgg_service import BGGService


def test_get_game():
    class FakeBGGClient:
        def get_game(self, bgg_id: int) -> str:
            return """
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

    service = BGGService(FakeBGGClient())

    game = service.get_game(174430)

    assert isinstance(game, Game)
    assert game.bgg_id == 174430
    assert game.name == "Gloomhaven"
    assert game.year_published == 2017
    assert game.min_players == 1
    assert game.max_players == 4
    assert game.min_play_time == 60
    assert game.max_play_time == 120
    assert game.rating == 8.5
    assert game.complexity == 3.8
    assert game.categories == ["Adventure", "Fantasy"]
    assert game.mechanics == ["Cooperative Game"]