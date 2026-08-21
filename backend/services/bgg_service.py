from bgg.client import BGGClient
from bgg.game_parser import parse_game_metadata
from models.game import Game


class BGGService:
    def __init__(self, client: BGGClient):
        self.client = client

    def get_game(self, bgg_id: int) -> Game:
        xml = self.client.get_game(bgg_id)

        return parse_game_metadata(xml)