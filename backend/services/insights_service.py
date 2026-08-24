from models.collection_insights import CollectionInsights
from repositories.insights_repository import InsightsRepository


class InsightsService:
    def __init__(
        self,
        repository: InsightsRepository,
    ):
        self.repository = repository

    def get_collection_insights(
        self,
    ) -> CollectionInsights:
        return CollectionInsights(
            total_games=self.repository.total_owned_games(),
            total_plays=self.repository.total_plays(),
            most_played=self.repository.get_most_played(),
            last_played=self.repository.get_last_played(),
            never_played_count=self.repository.never_played_count(),
        )