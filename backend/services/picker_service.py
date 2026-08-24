from dataclasses import dataclass
from datetime import datetime, timezone

from models.game import Game


@dataclass
class PickerCriteria:
    players: int
    max_play_time: int | None = None
    max_complexity: float | None = None


@dataclass
class PickerMatch:
    game: Game
    score: int
    reasons: list[str]


class PickerService:
    def find_matches(
        self,
        games: list[Game],
        criteria: PickerCriteria,
    ) -> list[Game]:
        matches = []

        for game in games:
            if not game.owned:
                continue

            if not self._supports_player_count(game, criteria.players):
                continue

            if not self._fits_play_time(game, criteria.max_play_time):
                continue

            if not self._fits_complexity(game, criteria.max_complexity):
                continue

            matches.append(game)

        return matches

    def rank_matches(
        self,
        games,
        criteria,
        play_stats=None,
    ):
        play_stats = play_stats or {}

        eligible_games = self.find_matches(
            games,
            criteria,
        )

        ranked = [
            self._score_game(
                game,
                criteria,
                play_stats.get(game.bgg_id),
            )
            for game in eligible_games
        ]

        return sorted(
            ranked,
            key=lambda match: (
                -match.score,
                match.game.name,
            ),
        )

    def _score_game(
        self,
        game: Game,
        criteria: PickerCriteria,
        play_stats=None,
    ) -> PickerMatch:
        score = 50
        reasons = [
            f"Supports {criteria.players} player"
            + ("" if criteria.players == 1 else "s")
        ]

        # Play time contributes up to 30 points.
        if criteria.max_play_time is None:
            score += 30
        elif game.max_play_time is not None:
            utilisation = min(
                game.max_play_time / criteria.max_play_time,
                1.0,
            )

            time_score = round(15 + (15 * utilisation))
            score += time_score

            reasons.append(
                f"Fits within {criteria.max_play_time} minutes"
            )

        # Complexity contributes up to 20 points.
        if criteria.max_complexity is None:
            score += 20
        elif game.complexity is None:
            # Unknown complexity is allowed, but receives a neutral score.
            score += 10
            reasons.append("Complexity not yet available")
        else:
            utilisation = min(
                game.complexity / criteria.max_complexity,
                1.0,
            )

            complexity_score = round(10 + (10 * utilisation))
            score += complexity_score

            reasons.append(
                f"Complexity {game.complexity:.1f} fits preference"
            )

        if play_stats is None:
            score += 10

            reasons.append(
                "Hasn't been played yet"
            )

        elif play_stats.last_played_at is None:
            score += 10

            reasons.append(
                "Hasn't been played yet"
            )

        else:
            from datetime import (
                datetime,
                timezone,
            )

            now = datetime.now(timezone.utc)

            days_since_played = (
                now - play_stats.last_played_at
            ).days

            if days_since_played >= 180:
                score += 10

                reasons.append(
                    "Hasn't been played in a while"
                )

            elif days_since_played >= 60:
                score += 6

                reasons.append(
                    "Due another play"
                )

            elif days_since_played >= 14:
                score += 3

        return PickerMatch(
            game=game,
            score=min(score, 100),
            reasons=reasons,
        )

    @staticmethod
    def _supports_player_count(game: Game, players: int) -> bool:
        if game.min_players is None or game.max_players is None:
            return False

        return game.min_players <= players <= game.max_players

    @staticmethod
    def _fits_play_time(
        game: Game,
        max_play_time: int | None,
    ) -> bool:
        if max_play_time is None:
            return True

        if game.max_play_time is None:
            return False

        return game.max_play_time <= max_play_time

    @staticmethod
    def _fits_complexity(
        game: Game,
        max_complexity: float | None,
    ) -> bool:
        if max_complexity is None:
            return True

        if game.complexity is None:
            return True

        return game.complexity <= max_complexity
