from dataclasses import dataclass, field

from bgstats.parser import parse_bgstats_export
from models.game import Game
from repositories.game_repository import GameRepository


@dataclass
class ImportRejection:
    bgg_id: int | None
    name: str | None
    reason: str


@dataclass
class ImportResult:
    records_received: int = 0
    inserted: int = 0
    updated: int = 0
    rejected: int = 0
    games: list[Game] = field(default_factory=list)
    rejections: list[ImportRejection] = field(default_factory=list)


class BGStatsImportService:
    def __init__(self, repository: GameRepository):
        self.repository = repository

    def import_owned_games(self, json_text: str) -> ImportResult:
        games = parse_bgstats_export(json_text)

        result = ImportResult(records_received=len(games))

        for game in games:
            if not game.owned:
                continue

            validation_error = self._validate_game(game)

            if validation_error:
                result.rejected += 1
                result.rejections.append(
                    ImportRejection(
                        bgg_id=game.bgg_id,
                        name=game.name,
                        reason=validation_error,
                    )
                )
                continue

            existing_game = self.repository.get_by_bgg_id(
                game.bgg_id
            )

            if existing_game is None:
                saved_game = self.repository.create(game)
                result.inserted += 1
            else:
                saved_game = self.repository.update(game)
                result.updated += 1

            result.games.append(saved_game)

        return result

    @staticmethod
    def _validate_game(game: Game) -> str | None:
        if not game.bgg_id or game.bgg_id <= 0:
            return "Missing or invalid BGG ID"

        if not game.name or not game.name.strip():
            return "Missing game name"

        if (
            game.min_players is not None
            and game.max_players is not None
            and game.min_players > game.max_players
        ):
            return "Minimum players exceeds maximum players"

        if (
            game.min_play_time is not None
            and game.max_play_time is not None
            and game.min_play_time > game.max_play_time
        ):
            return "Minimum play time exceeds maximum play time"

        if game.complexity is not None and not 0 <= game.complexity <= 5:
            return "Complexity must be between 0 and 5"

        return None