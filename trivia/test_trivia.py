# Test file for trivia kata

import io
import logging
import pytest
import random
from pathlib import Path

from refactored import (
    Game,
    Question,
    WINNING_CRITERION_THRESHOLD,
    BOARD_LENGTH,
)


@pytest.fixture
def logger():
    test_logger = logging.getLogger(__name__)
    test_logger.setLevel("ERROR")
    return test_logger


@pytest.mark.skip(reason="Used only for creating a reference before code refactoring")
def test_golden_master():
    random.seed(3)

    golden_master_file = Path('trivia/golden_master.txt')
    golden_master_nb_it = 100

    logger = logging.getLogger(__name__)
    logger.setLevel("DEBUG")

    if (WRITE_GOLDEN_MASTER := False):
        file_handler = logging.FileHandler(golden_master_file, mode="w")
        logger.addHandler(file_handler)

        for _ in range(golden_master_nb_it):
            game = Game(logger)

            game.add_new_player('Player1')
            game.add_new_player('Player2')
            game.add_new_player('Player3')

            game.play()

        assert(False)

    else:
        buffer = io.StringIO()
        buffer_handler = logging.StreamHandler(buffer)
        logger.addHandler(buffer_handler)

        for _ in range(golden_master_nb_it):
            game = Game(logger)

            game.add_new_player('Player1')
            game.add_new_player('Player2')
            game.add_new_player('Player3')

            game.play()

        with open(golden_master_file, 'r') as file:
            reference = file.read()

        assert(buffer.getvalue() == reference)


def test_add_player(logger):
    game = Game(logger)

    game.add_new_player('Player1')
    game._cycle_to_next_player()

    assert(game.nb_of_players == 1)
    assert(game.current_player == game.players[0])


def test_playability_2_players(logger):
    game = Game(logger)

    game.add_new_player('Player1')
    assert(not game.is_playable())

    game.add_new_player('Player2')
    assert(game.is_playable())


def test_playability_6_players(logger):
    game = Game(logger)

    game.add_new_player('Player1')
    game.add_new_player('Player2')
    game.add_new_player('Player3')
    game.add_new_player('Player4')
    game.add_new_player('Player5')
    game.add_new_player('Player6')
    assert(game.is_playable())

    game.add_new_player('Player7')
    assert(not game.is_playable())


def test_current_category_cycle(logger):
    game = Game(logger)

    game.add_new_player("Player1")
    game._cycle_to_next_player()
    player = game.current_player

    assert(game.current_category == Question.Type.POP)

    player.place += 1
    assert(game.current_category == Question.Type.SCIENCE)

    player.place += 1
    assert(game.current_category == Question.Type.SPORTS)

    player.place += 1
    assert(game.current_category == Question.Type.ROCK)

    player.place += 1
    assert(game.current_category == Question.Type.POP)


def test_wrong_answer(logger):
    game = Game(logger)
    game.add_new_player("Player1")
    game._cycle_to_next_player()

    assert(not game._is_player_in_penalty_box())
    game._punish_wrong_answer()
    assert(game._is_player_in_penalty_box())


def test_right_answer(logger):
    game = Game(logger)
    game.add_new_player("Player1")
    game._cycle_to_next_player()

    player1 = game.current_player

    assert(player1.purse == 0)
    game._reward_right_answer()
    assert(player1.purse == 1)


def test_update_player_position(logger):
    game = Game(logger)
    game.add_new_player("Player1")
    game._cycle_to_next_player()

    player = game.current_player

    assert(player.place == 0)
    game._update_player_position(2)
    assert(player.place == 2)


def test_player_position_wraps_around(logger):
    game = Game(logger)
    game.add_new_player("Player1")
    game._cycle_to_next_player()

    player = game.current_player
    player.place = BOARD_LENGTH - 1

    game._update_player_position(1)
    assert(player.place == 0)


def test_even_roll_outside_penalty_box(logger):
    game = Game(logger)
    game.add_new_player("Player1")
    game._cycle_to_next_player()

    player = game.current_player
    player.is_in_penalty_box = False

    assert(game._move_player(4))


def test_odd_roll_outside_penalty_box(logger):
    game = Game(logger)
    game.add_new_player("Player1")
    game._cycle_to_next_player()

    player = game.current_player
    player.is_in_penalty_box = False

    assert(game._move_player(3))


def test_even_roll_inside_penalty_box(logger):
    game = Game(logger)
    game.add_new_player("Player1")
    game._cycle_to_next_player()

    player = game.current_player
    player.is_in_penalty_box = True

    assert(not game._move_player(4))


def test_odd_roll_inside_penalty_box(logger):
    game = Game(logger)
    game.add_new_player("Player1")
    game._cycle_to_next_player()

    player = game.current_player
    player.is_in_penalty_box = True

    assert(game._move_player(3))


def test_player_has_won(logger):
    game = Game(logger)
    game.add_new_player("Player1")
    game._cycle_to_next_player()

    player = game.current_player
    player.purse = WINNING_CRITERION_THRESHOLD

    assert(game._did_player_win())


def test_player_has_not_won(logger):
    game = Game(logger)
    game.add_new_player("Player1")
    game._cycle_to_next_player()

    player = game.current_player
    player.purse = WINNING_CRITERION_THRESHOLD - 1

    assert(player.purse == 5)
    assert(not game._did_player_win())