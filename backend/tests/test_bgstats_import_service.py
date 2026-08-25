from pathlib import Path

from services.bgstats_import_service import BGStatsImportService


FIXTURE = (
    Path(__file__).parent
    / "fixtures"
    / "bgstats_collection.json"
)


def test_import_only_owned_games():
    class FakeRepository:
        def __init__(self):
            self.created = []

        def get_by_bgg_id(self, bgg_id):
            return None

        def create(self, game):
            self.created.append(game)
            return game

    repository = FakeRepository()
    service = BGStatsImportService(repository)

    json_text = FIXTURE.read_text(encoding="utf-8")

    result = service.import_owned_games(json_text)

    assert result.inserted == 1
    assert result.updated == 0
    assert result.rejected == 0

    assert len(result.games) == 1
    assert result.games[0].name == "Terraforming Mars"

    assert len(repository.created) == 1
    assert repository.created[0].bgg_id == 167791


def test_import_updates_existing_game():
    class FakeRepository:
        def __init__(self):
            self.updated = []

        def get_by_bgg_id(self, bgg_id):
            if bgg_id == 167791:
                return object()

            return None

        def create(self, game):
            return game

        def update(self, game):
            self.updated.append(game)
            return game

    repository = FakeRepository()
    service = BGStatsImportService(repository)

    json_text = FIXTURE.read_text(encoding="utf-8")

    result = service.import_owned_games(json_text)

    assert result.inserted == 0
    assert result.updated == 1
    assert result.rejected == 0

    assert len(result.games) == 1
    assert len(repository.updated) == 1
    assert repository.updated[0].bgg_id == 167791

def test_invalid_game_is_rejected(monkeypatch):
    from models.game import Game
    import services.bgstats_import_service as import_module

    invalid_game = Game(
        bgg_id=123,
        name="Invalid Game",
        min_players=5,
        max_players=2,
        owned=True,
    )

    monkeypatch.setattr(
        import_module,
        "parse_bgstats_export",
        lambda json_text: [invalid_game],
    )

    class FakeRepository:
        def get_by_bgg_id(self, bgg_id):
            raise AssertionError(
                "Repository should not be called for invalid data"
            )

    service = BGStatsImportService(FakeRepository())

    result = service.import_owned_games("{}")

    assert result.records_received == 1
    assert result.inserted == 0
    assert result.updated == 0
    assert result.rejected == 1
    assert result.games == []

    assert len(result.rejections) == 1
    assert (
        result.rejections[0].reason
        == "Minimum players exceeds maximum players"
    )