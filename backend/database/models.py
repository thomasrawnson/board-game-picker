from sqlalchemy import Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from database.connection import Base


class Game(Base):
    __tablename__ = "games"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    bgg_id: Mapped[int] = mapped_column(Integer, unique=True, nullable=False)

    name: Mapped[str] = mapped_column(String(255), nullable=False)

    year_published: Mapped[int | None] = mapped_column(Integer)

    min_players: Mapped[int | None] = mapped_column(Integer)

    max_players: Mapped[int | None] = mapped_column(Integer)

    playing_time: Mapped[int | None] = mapped_column(Integer)

    complexity: Mapped[float | None] = mapped_column(Float)

    rating: Mapped[float | None] = mapped_column(Float)

    thumbnail: Mapped[str | None] = mapped_column(String(500))