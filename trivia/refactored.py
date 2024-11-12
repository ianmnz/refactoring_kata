# Trivia Refactor-kata from
# https://github.com/emilybache/trivia


import random
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


@dataclass(frozen=True)
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

    @property
    def nb_of_players(self) -> int:
        return len(self.players)

    @property
    def _current_category(self) -> str:
        category_idx: int = self.get_current_player().place % Question.Type.COUNT
        return str(Question.Type(category_idx))

    def is_playable(self) -> bool:
        return 2 <= self.nb_of_players <= 6

    def get_current_player(self) -> Player:
        return self.players[self.current_player]

    def _did_player_win(self) -> bool:
        return self.get_current_player().purse != 6

    def is_player_in_penalty_box(self) -> bool:
        return self.get_current_player().is_in_penalty_box

    def cycle_to_next_player(self) -> None:
        self.current_player = (self.current_player + 1) % self.nb_of_players

    def add_player(self, player_name: str) -> None:
        new_player_id = self.nb_of_players
        self.players[new_player_id] = Player(new_player_id, player_name)

        print(player_name + " was added")
        print("They are player number %s" % self.nb_of_players)

    def run(self) -> None:
        not_a_winner = False

        if not self.is_playable():
            print("The number of players must be at least 2 and at most 6!")
            return

        while True:
            self.roll(random.randrange(5) + 1)

            if random.randrange(9) == 7:
                not_a_winner = self.wrong_answer()
            else:
                not_a_winner = self.was_correctly_answered()

            self.cycle_to_next_player()
            if not not_a_winner: break

    def roll(self, roll: int) -> None:
        print("%s is the current player" % self.get_current_player().name)
        print("They have rolled a %s" % roll)

        if self.is_player_in_penalty_box():
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

    def was_correctly_answered(self) -> bool:
        if (self.get_current_player().is_in_penalty_box
            and (not self.is_getting_out_of_penalty_box)
        ):
            return True

        self.get_current_player().purse += 1

        print("Answer was correct!!!!")
        print(f"{self.get_current_player().name} now has {self.get_current_player().purse} Gold Coins.")

        return self._did_player_win()

    def wrong_answer(self) -> bool:
        print('Question was incorrectly answered')
        print(self.get_current_player().name + " was sent to the penalty box")

        self.get_current_player().is_in_penalty_box = True

        return True


if __name__ == '__main__':
    game = Game()

    game.add_player('Chet')
    game.add_player('Pat')
    game.add_player('Sue')

    game.run()
