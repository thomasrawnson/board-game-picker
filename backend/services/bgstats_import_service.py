import logging
from dataclasses import dataclass, field
from bgstats.parser import parse_bgstats_export
from models.game import Game
from repositories.game_repository import GameRepository

logger = logging.getLogger(__name__)
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
        
        logger.info(
                "BG Stats import started records=%d",
                len(games),
            )

        result = ImportResult(records_received=len(games))

        for game in games:
            if not game.owned:
                continue

            validation_error = self._validate_game(game)

            if validation_error:
                logger.warning(
                    "BG Stats record rejected bgg_id=%s reason=%s",
                    game.bgg_id,
                    validation_error,
                )
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

            logger.info(
            (
                "BG Stats import completed "
                "received=%d inserted=%d updated=%d rejected=%d"
            ),
            result.records_received,
            result.inserted,
            result.updated,
            result.rejected,
        )
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

def test_import_logs_quality_summary(caplog):
    import logging
    from pathlib import Path

    fixture = (
        Path(__file__).parent
        / "fixtures"
        / "bgstats_collection.json"
    )

    class FakeRepository:
        def get_by_bgg_id(self, bgg_id):
            return None

        def create(self, game):
            return game

    repository = FakeRepository()
    service = BGStatsImportService(repository)

    json_text = fixture.read_text(encoding="utf-8")

    with caplog.at_level(logging.INFO):
        result = service.import_owned_games(json_text)

    assert result.inserted == 1
    assert "BG Stats import started" in caplog.text
    assert "BG Stats import completed" in caplog.text
    assert "inserted=1" in caplog.text