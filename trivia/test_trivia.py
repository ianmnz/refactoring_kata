# Test file for trivia kata

import io
import logging
import pytest
import random
from pathlib import Path

from refactored import Game, Question


@pytest.fixture
def logger():
    test_logger = logging.getLogger(__name__)
    test_logger.setLevel("ERROR")
    return test_logger


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
    assert(not game.is_playable())

    game.add_new_player('Player2')
    assert(game.is_playable())

    game.add_new_player('Player3')
    game.add_new_player('Player4')
    game.add_new_player('Player5')
    game.add_new_player('Player6')
    assert(game.is_playable())

    game.add_new_player('Player7')
    assert(not game.is_playable())


def test_current_category(logger):
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
    game.add_new_player("Player2")
    game._cycle_to_next_player()

    player1 = game.current_player

    assert(player1.place == 0)
    game._update_player_position(2)
    assert(player1.place == 2)

    game._cycle_to_next_player()
    player2 = game.current_player
    player2.place = 11

    game._update_player_position(1)
    assert(player2.place == 0)


def test_move_player(logger):
    game = Game(logger)
    game.add_new_player("Player1")
    game.add_new_player("Player2")
    game.add_new_player("Player3")
    game._cycle_to_next_player()

    player1 = game.current_player
    player1.is_in_penalty_box = True

    assert(not game._move_player(4))    # Even integer roll

    game._cycle_to_next_player()
    player2 = game.current_player
    player2.is_in_penalty_box = True

    assert(game._move_player(3))    # Odd integer roll

    game._cycle_to_next_player()
    player3 = game.current_player
    player3.is_in_penalty_box = False

    assert(game._move_player(4))    # Even integer roll but not in penalty box


def test_game_winner(logger):
    game = Game(logger)
    game.add_new_player("Player1")
    game.add_new_player("Player2")
    game._cycle_to_next_player()

    player1 = game.current_player
    player1.purse = 4

    game._cycle_to_next_player()
    player2 = game.current_player
    player2.purse = 5

    game._cycle_to_next_player()
    game._reward_right_answer()

    assert(player1.purse == 5)
    assert(not game._did_player_win()) # player1.purse != 6

    game._cycle_to_next_player()
    game._reward_right_answer()

    assert(player2.purse == 6)
    assert(game._did_player_win()) # player2.purse == 6
