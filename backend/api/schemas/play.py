from pydantic import BaseModel, Field


class PlayCreate(BaseModel):
    bgg_id: int = Field(gt=0)
    player_count: int = Field(ge=1)