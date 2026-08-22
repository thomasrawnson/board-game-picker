import sys
from pathlib import Path

from database.connection import SessionLocal
from repositories.game_repository import GameRepository
from services.bgstats_import_service import BGStatsImportService


def main():
    if len(sys.argv) != 2:
        print(
            "Usage: python -m scripts.import_bgstats "
            "<path-to-bgstats-json>"
        )
        raise SystemExit(1)

    export_path = Path(sys.argv[1])

    if not export_path.exists():
        print(f"File not found: {export_path}")
        raise SystemExit(1)

    json_text = export_path.read_text(
        encoding="utf-8"
    )

    db = SessionLocal()

    try:
        repository = GameRepository(db)
        service = BGStatsImportService(repository)

        games = service.import_owned_games(json_text)

        print(
            f"Imported {len(games)} currently-owned games."
        )

    finally:
        db.close()


if __name__ == "__main__":
    main()