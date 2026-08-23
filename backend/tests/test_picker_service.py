from models.game import Game
from services.picker_service import PickerCriteria, PickerService


def test_filters_games_by_player_count_and_play_time():
    games = [
        Game(
            bgg_id=1,
            name="Quick Two Player Game",
            min_players=2,
            max_players=4,
            min_play_time=30,
            max_play_time=45,
            owned=True,
        ),
        Game(
            bgg_id=2,
            name="Long Game",
            min_players=2,
            max_players=4,
            min_play_time=90,
            max_play_time=120,
            owned=True,
        ),
        Game(
            bgg_id=3,
            name="Three Player Only",
            min_players=3,
            max_players=3,
            min_play_time=30,
            max_play_time=45,
            owned=True,
        ),
    ]

    service = PickerService()

    matches = service.find_matches(
        games,
        PickerCriteria(
            players=2,
            max_play_time=60,
        ),
    )

    assert [game.bgg_id for game in matches] == [1]


def test_excludes_games_that_are_not_owned():
    games = [
        Game(
            bgg_id=1,
            name="Owned Game",
            min_players=2,
            max_players=4,
            max_play_time=60,
            owned=True,
        ),
        Game(
            bgg_id=2,
            name="Wishlist Game",
            min_players=2,
            max_players=4,
            max_play_time=60,
            owned=False,
        ),
    ]

    service = PickerService()

    matches = service.find_matches(
        games,
        PickerCriteria(
            players=2,
            max_play_time=60,
        ),
    )

    assert [game.bgg_id for game in matches] == [1]


def test_filters_by_complexity_when_available():
    games = [
        Game(
            bgg_id=1,
            name="Medium Game",
            min_players=2,
            max_players=4,
            max_play_time=60,
            complexity=2.5,
            owned=True,
        ),
        Game(
            bgg_id=2,
            name="Heavy Game",
            min_players=2,
            max_players=4,
            max_play_time=60,
            complexity=4.2,
            owned=True,
        ),
    ]

    service = PickerService()

    matches = service.find_matches(
        games,
        PickerCriteria(
            players=2,
            max_play_time=60,
            max_complexity=3.0,
        ),
    )

    assert [game.bgg_id for game in matches] == [1]


def test_missing_complexity_does_not_exclude_game():
    games = [
        Game(
            bgg_id=1,
            name="Unknown Weight Game",
            min_players=2,
            max_players=4,
            max_play_time=60,
            complexity=None,
            owned=True,
        )
    ]

    service = PickerService()

    matches = service.find_matches(
        games,
        PickerCriteria(
            players=2,
            max_play_time=60,
            max_complexity=3.0,
        ),
    )

    assert [game.bgg_id for game in matches] == [1]

def test_rank_matches_returns_highest_score_first():
    games = [
        Game(
            bgg_id=1,
            name="Short Game",
            min_players=2,
            max_players=4,
            max_play_time=30,
            complexity=2.0,
            owned=True,
        ),
        Game(
            bgg_id=2,
            name="Closer Match",
            min_players=2,
            max_players=4,
            max_play_time=55,
            complexity=2.8,
            owned=True,
        ),
    ]

    service = PickerService()

    matches = service.rank_matches(
        games,
        PickerCriteria(
            players=2,
            max_play_time=60,
            max_complexity=3.0,
        ),
    )

    assert matches[0].game.bgg_id == 2
    assert matches[0].score > matches[1].score


def test_rank_match_contains_explanation():
    game = Game(
        bgg_id=1,
        name="Example Game",
        min_players=2,
        max_players=4,
        max_play_time=60,
        complexity=2.5,
        owned=True,
    )

    service = PickerService()

    matches = service.rank_matches(
        [game],
        PickerCriteria(
            players=2,
            max_play_time=90,
            max_complexity=3.0,
        ),
    )

    match = matches[0]

    assert "Supports 2 players" in match.reasons
    assert "Fits within 90 minutes" in match.reasons
    assert "Complexity 2.5 fits preference" in match.reasons


def test_score_never_exceeds_100():
    game = Game(
        bgg_id=1,
        name="Perfect Match",
        min_players=2,
        max_players=4,
        max_play_time=60,
        complexity=3.0,
        owned=True,
    )

    service = PickerService()

    matches = service.rank_matches(
        [game],
        PickerCriteria(
            players=2,
            max_play_time=60,
            max_complexity=3.0,
        ),
    )

    assert matches[0].score == 100