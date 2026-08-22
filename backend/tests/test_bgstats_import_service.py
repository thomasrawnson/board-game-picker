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

    games = service.import_owned_games(json_text)

    assert len(games) == 1
    assert games[0].name == "Terraforming Mars"

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

    games = service.import_owned_games(json_text)

    assert len(games) == 1
    assert len(repository.updated) == 1
    assert repository.updated[0].bgg_id == 167791