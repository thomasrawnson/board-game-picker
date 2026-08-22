from models.game import Game
from repositories.game_repository import GameRepository


class GameService:
    def __init__(self, repository: GameRepository):
        self.repository = repository

    def get_game(self, bgg_id: int) -> Game | None:
        return self.repository.get_by_bgg_id(bgg_id)

    def get_games(self) -> list[Game]:
        return self.repository.get_all()

    def create_game(self, game: Game) -> Game:
        return self.repository.create(game)

    def update_game(self, game: Game) -> Game | None:
        return self.repository.update(game)

    def delete_game(self, bgg_id: int) -> bool:
        return self.repository.delete(bgg_id)