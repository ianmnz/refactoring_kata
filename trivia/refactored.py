# Trivia Refactor-kata from
# https://github.com/emilybache/trivia


from collections import defaultdict, deque
from dataclasses import dataclass, field
from enum import IntEnum, auto
from typing import Dict, List

@dataclass
class Player:
    id: int
    name: str
    place: int = field(default=0)
    purse: int = field(default=0)
    is_in_penalty_box: bool = field(default=False)

@dataclass
class Question:
    class Type(IntEnum):
        POP = 0
        SCIENCE = 1
        SPORTS = 2
        ROCK = 3
        COUNT = auto()

        def __str__(self) -> str:
            return self.name.title()

    type: Type
    index: int

    def __str__(self) -> str:
        return f"{self.type} Question {self.index}"


class Game:
    def __init__(self):
        self.players: Dict[int, Player] = dict()
        self.questions: Dict[int, deque[Question]] = defaultdict(deque)

        self.current_player: int = 0
        self.is_getting_out_of_penalty_box = False

        for i in range(50):
            self.questions[Question.Type.POP].append(Question(Question.Type.POP, i))
            self.questions[Question.Type.SCIENCE].append(Question(Question.Type.SCIENCE, i))
            self.questions[Question.Type.SPORTS].append(Question(Question.Type.SPORTS, i))
            self.questions[Question.Type.ROCK].append(Question(Question.Type.ROCK, i))

    def is_playable(self):
        return self.nb_of_players >= 2

    def add(self, player_name: str) -> None:
        new_player_id = self.nb_of_players
        self.players[new_player_id] = Player(new_player_id, player_name)

        print(player_name + " was added")
        print("They are player number %s" % self.nb_of_players)

    @property
    def nb_of_players(self) -> int:
        return len(self.players)

    def get_current_player(self) -> Player:
        return self.players[self.current_player]

    def cycle_to_next_player(self) -> None:
        self.current_player = (self.current_player + 1) % self.nb_of_players

    def roll(self, roll: int) -> None:
        print("%s is the current player" % self.get_current_player().name)
        print("They have rolled a %s" % roll)

        if self.get_current_player().is_in_penalty_box:
            if roll % 2 != 0:
                print("%s is getting out of the penalty box" % self.get_current_player().name)
                self.is_getting_out_of_penalty_box = True
            else:
                print("%s is not getting out of the penalty box" % self.get_current_player().name)
                self.is_getting_out_of_penalty_box = False
                return

        self.get_current_player().place = self.get_current_player().place + roll
        if self.get_current_player().place > 11:
            self.get_current_player().place = self.get_current_player().place - 12

        print(self.get_current_player().name + \
                    '\'s new location is ' + \
                    str(self.get_current_player().place))
        print("The category is %s" % self._current_category)
        self._ask_question()

    def _ask_question(self) -> None:
        if self._current_category == 'Pop': print(self.questions[Question.Type.POP].popleft())
        if self._current_category == 'Science': print(self.questions[Question.Type.SCIENCE].popleft())
        if self._current_category == 'Sports': print(self.questions[Question.Type.SPORTS].popleft())
        if self._current_category == 'Rock': print(self.questions[Question.Type.ROCK].popleft())

    @property
    def _current_category(self) -> str:
        category_idx: int = self.get_current_player().place % Question.Type.COUNT
        return str(Question.Type(category_idx))

    def was_correctly_answered(self) -> bool:
        if (self.get_current_player().is_in_penalty_box
            and (not self.is_getting_out_of_penalty_box)
        ):
            self.cycle_to_next_player()
            return True

        self.get_current_player().purse += 1

        print("Answer was correct!!!!")
        print(f"{self.get_current_player().name} now has {self.get_current_player().purse} Gold Coins.")

        winner = self._did_player_win()
        self.cycle_to_next_player()

        return winner

    def wrong_answer(self) -> bool:
        print('Question was incorrectly answered')
        print(self.get_current_player().name + " was sent to the penalty box")

        self.get_current_player().is_in_penalty_box = True

        self.cycle_to_next_player()

        return True

    def _did_player_win(self) -> bool:
        return self.get_current_player().purse != 6


from random import randrange

if __name__ == '__main__':
    # not_a_winner = False

    # game = Game()

    # game.add('Chet')
    # game.add('Pat')
    # game.add('Sue')

    # while True:
    #     game.roll(randrange(5) + 1)

    #     if randrange(9) == 7:
    #         not_a_winner = game.wrong_answer()
    #     else:
    #         not_a_winner = game.was_correctly_answered()

    #     if not not_a_winner: break

    q = Question(Question.Type.SPORTS, 3)
    pop = 4 % Question.Type.COUNT
    sci = 5 % Question.Type.COUNT
    spo = 6 % Question.Type.COUNT
    roc = 7 % Question.Type.COUNT
    print(Question.Type(pop))
    print(Question.Type(sci))
    print(Question.Type(spo))
    print(Question.Type(roc))
