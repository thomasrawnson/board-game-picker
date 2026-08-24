import sys
from pathlib import Path

from database.connection import SessionLocal
from repositories.play_repository import PlayRepository
from services.bgstats_play_import_service import (
    BGStatsPlayImportService,
)


def main():
    if len(sys.argv) != 2:
        print(
            "Usage: "
            "python -m scripts.import_bgstats_plays "
            "<path-to-bgstats-json>"
        )
        raise SystemExit(1)

    export_path = Path(sys.argv[1])

    if not export_path.exists():
        print(
            f"File not found: {export_path}"
        )
        raise SystemExit(1)

    json_text = export_path.read_text(
        encoding="utf-8"
    )

    db = SessionLocal()

    try:
        repository = PlayRepository(db)

        service = BGStatsPlayImportService(
            repository
        )

        result = service.import_plays(
            json_text
        )

        print(
            f"Imported: {result.imported}"
        )
        print(
            "Already imported: "
            f"{result.skipped_existing}"
        )
        print(
            "Skipped - game not in collection: "
            f"{result.skipped_missing_game}"
        )

    finally:
        db.close()


if __name__ == "__main__":
    main()