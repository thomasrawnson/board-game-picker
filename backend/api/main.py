from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from database.connection import get_db
from repositories.game_repository import GameRepository
from services.game_service import GameService


app = FastAPI(
    title="BoardGamePicker API",
    version="0.1.0",
)


def get_game_service(
    db: Session = Depends(get_db),
) -> GameService:
    repository = GameRepository(db)
    return GameService(repository)


@app.get("/games/{bgg_id}")
def get_game(
    bgg_id: int,
    service: GameService = Depends(get_game_service),
):
    game = service.get_game(bgg_id)

    if game is None:
        raise HTTPException(
            status_code=404,
            detail="Game not found",
        )

    return game