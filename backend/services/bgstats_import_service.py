from bgstats.parser import parse_bgstats_export
from models.game import Game
from repositories.game_repository import GameRepository


class BGStatsImportService:
    def __init__(self, repository: GameRepository):
        self.repository = repository

    def import_owned_games(self, json_text: str) -> list[Game]:
        games = parse_bgstats_export(json_text)

        imported_games = []

        for game in games:
            if not game.owned:
                continue

            existing_game = self.repository.get_by_bgg_id(
                game.bgg_id
            )

            if existing_game is None:
                saved_game = self.repository.create(game)
            else:
                saved_game = self.repository.update(game)

            imported_games.append(saved_game)

        return imported_games