# Test file for trivia kata

import random
import io
from pathlib import Path
from contextlib import redirect_stdout

from refactored import Game, Question

def test_golden_master():
    random.seed(3)
    golden_master_file = Path('trivia/golden_master.txt')
    golden_master_nb_it = 100

    # with open(golden_master_file, 'w') as file, redirect_stdout(file):
    #     for _ in range(golden_master_nb_it):
    #         game = Game()

    #         game.add_player('Player1')
    #         game.add_player('Player2')
    #         game.add_player('Player3')

    #         game.play()

    with io.StringIO() as buffer, redirect_stdout(buffer):
        for _ in range(golden_master_nb_it):
            game = Game()

            game.add_player('Player1')
            game.add_player('Player2')
            game.add_player('Player3')

            game.play()

            output = buffer.getvalue()

    with open(golden_master_file, 'r') as file:
        reference = file.read()

    assert(output == reference)


def test_add_player():
    game = Game()

    game.add_player('Player1')

    assert(game.nb_of_players == 1)
    assert(game.get_current_player() == game.players[0])
    assert(not game.is_playable())

    game.add_player('Player2')
    assert(game.is_playable())

    game.add_player('Player3')
    game.add_player('Player4')
    game.add_player('Player5')
    game.add_player('Player6')
    assert(game.is_playable())

    game.add_player('Player7')
    assert(not game.is_playable())


def test_current_category():
    game = Game()

    game.add_player("Player1")
    player = game.get_current_player()

    assert(game._current_category == Question.Type.POP)

    player.place += 1
    assert(game._current_category == Question.Type.SCIENCE)

    player.place += 1
    assert(game._current_category == Question.Type.SPORTS)

    player.place += 1
    assert(game._current_category == Question.Type.ROCK)

    player.place += 1
    assert(game._current_category == Question.Type.POP)


def test_wrong_answer_cycling():
    game = Game()
    game.add_player("Player1")
    game.add_player("Player2")

    game.wrong_answer()
    assert(game.current_player == 1)

    game.wrong_answer()
    assert(game.current_player == 0)


def test_right_answer():
    game = Game()
    game.add_player("Player1")
    game.add_player("Player2")
    game.add_player("Player3")

    player1 = game.get_current_player()

    assert(player1.purse == 0)
    assert(game.was_correctly_answered())
    assert(player1.purse == 1)

    player2 = game.get_current_player()
    player2.is_in_penalty_box = True

    assert(player2.purse == 0)
    assert(game.was_correctly_answered())
    assert(player2.purse == 0)

    player3 = game.get_current_player()
    player3.is_in_penalty_box = True
    game.is_getting_out_of_penalty_box = True

    assert(player3.purse == 0)
    assert(game.was_correctly_answered())
    assert(player3.purse == 1)

    player1.purse = 5
    assert(not game.was_correctly_answered())


def test_roll():
    game = Game()
    game.add_player("Player1")
    game.add_player("Player2")
    game.add_player("Player3")
    game.add_player("Player4")

    player1 = game.get_current_player()

    assert(player1.place == 0)
    game.roll(2)
    assert(player1.place == 2)

    game.cycle_to_next_player()
    player2 = game.get_current_player()
    player2.place = 11

    game.roll(1)
    assert(player2.place == 0)

    game.cycle_to_next_player()
    player3 = game.get_current_player()
    player3.is_in_penalty_box = True
    player3.place = 3

    game.roll(4)    # Even integer roll
    assert(player3.place == 3)
    assert(not game.is_getting_out_of_penalty_box)

    game.cycle_to_next_player()
    player4 = game.get_current_player()
    player4.is_in_penalty_box = True
    player4.place = 7

    game.roll(5)    # Odd integer roll
    assert(player4.place == 0)
    assert(game.is_getting_out_of_penalty_box)
