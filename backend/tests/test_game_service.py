from unittest.mock import Mock

from models.game import Game
from services.game_service import GameService


def test_get_game_delegates_to_repository():
    repository = Mock()

    expected_game = Game(
        bgg_id=174430,
        name="Gloomhaven",
    )

    repository.get_by_bgg_id.return_value = expected_game

    service = GameService(repository)

    result = service.get_game(174430)

    assert result == expected_game
    repository.get_by_bgg_id.assert_called_once_with(174430)


def test_create_game_delegates_to_repository():
    repository = Mock()

    game = Game(
        bgg_id=174430,
        name="Gloomhaven",
    )

    repository.create.return_value = game

    service = GameService(repository)

    result = service.create_game(game)

    assert result == game
    repository.create.assert_called_once_with(game)


def test_update_game_delegates_to_repository():
    repository = Mock()

    game = Game(
        bgg_id=174430,
        name="Gloomhaven",
        rating=8.5,
    )

    repository.update.return_value = game

    service = GameService(repository)

    result = service.update_game(game)

    assert result == game
    repository.update.assert_called_once_with(game)


def test_delete_game_delegates_to_repository():
    repository = Mock()

    repository.delete.return_value = True

    service = GameService(repository)

    result = service.delete_game(174430)

    assert result is True
    repository.delete.assert_called_once_with(174430)