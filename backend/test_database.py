from sqlalchemy import inspect

from database.connection import engine


def test_games_table_exists():
    inspector = inspect(engine)

    tables = inspector.get_table_names()

    assert "games" in tables