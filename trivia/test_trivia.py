# Test file for trivia kata

import random
import io
from pathlib import Path
from contextlib import redirect_stdout

from refactored import Game

def test_golden_master():
    random.seed(3)
    golden_master_file = Path('trivia/golden_master.txt')
    golden_master_nb_it = 100

    # with open(golden_master_file, 'w') as file, redirect_stdout(file):
    #     for _ in range(golden_master_nb_it):
    #         game = Game()
    #         not_a_winner = False

    #         game.add('Player1')
    #         game.add('Player2')
    #         game.add('Player3')

    #         while True:
    #             game.roll(random.randrange(5) + 1)

    #             if random.randrange(9) == 7:
    #                 not_a_winner = game.wrong_answer()
    #             else:
    #                 not_a_winner = game.was_correctly_answered()

    #             if not not_a_winner: break

    with io.StringIO() as buffer, redirect_stdout(buffer):
        for _ in range(golden_master_nb_it):
            game = Game()
            not_a_winner = False

            game.add('Player1')
            game.add('Player2')
            game.add('Player3')

            while True:
                game.roll(random.randrange(5) + 1)

                if random.randrange(9) == 7:
                    not_a_winner = game.wrong_answer()
                else:
                    not_a_winner = game.was_correctly_answered()

                if not not_a_winner: break

            output = buffer.getvalue()

    with open(golden_master_file, 'r') as file:
        reference = file.read()

    assert(output == reference)