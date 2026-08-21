from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from api.schemas.game import GameCreate
from database.connection import get_db
from models.game import Game
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


@app.post("/games", status_code=201)
def create_game(
    game_data: GameCreate,
    service: GameService = Depends(get_game_service),
):
    game = Game(
        bgg_id=game_data.bgg_id,
        name=game_data.name,
        year_published=game_data.year_published,
        min_players=game_data.min_players,
        max_players=game_data.max_players,
        min_play_time=game_data.min_play_time,
        max_play_time=game_data.max_play_time,
        complexity=game_data.complexity,
        rating=game_data.rating,
        owned=game_data.owned,
        image_url=game_data.image_url,
        thumbnail_url=game_data.thumbnail_url,
        categories=game_data.categories,
        mechanics=game_data.mechanics,
    )

    return service.create_game(game)