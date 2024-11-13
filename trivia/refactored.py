# Trivia Refactor-kata from
# https://github.com/emilybache/trivia


import logging
import random
from collections import defaultdict, deque
from dataclasses import dataclass, field
from enum import IntEnum, auto
from typing import Dict, Optional

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
    def __init__(self, logger: Optional[logging.Logger] = None):
        self.players: Dict[int, Player] = dict()
        self.questions: Dict[int, deque[Question]] = defaultdict(deque)

        self.current_player_index: int = -1

        if logger is not None:
            self.logger = logger
        else:
            self.logger = logging.getLogger(__name__)
            self.logger.setLevel("DEBUG")
            self.logger.addHandler(logging.StreamHandler())

        for i in range(50):
            self.questions[Question.Type.POP].append(Question(Question.Type.POP, i))
            self.questions[Question.Type.SCIENCE].append(Question(Question.Type.SCIENCE, i))
            self.questions[Question.Type.SPORTS].append(Question(Question.Type.SPORTS, i))
            self.questions[Question.Type.ROCK].append(Question(Question.Type.ROCK, i))

    @property
    def nb_of_players(self) -> int:
        return len(self.players)

    @property
    def current_player(self) -> Player:
        return self.players[self.current_player_index]

    @property
    def current_category(self) -> Question.Type:
        category_idx: int = self.current_player.place % Question.Type.COUNT
        return Question.Type(category_idx)

    def is_playable(self) -> bool:
        return 2 <= self.nb_of_players <= 6

    def add_new_player(self, player_name: str) -> None:
        new_player_id = self.nb_of_players
        self.players[new_player_id] = Player(new_player_id, player_name)

        self.logger.info(f"{player_name} was added")
        self.logger.info(f"They are player number {self.nb_of_players}")

    def play(self) -> None:
        if not self.is_playable():
            self.logger.info("The number of players must be at least 2 and at most 6!")
            return

        while True:
            self._cycle_to_next_player()

            roll = self._roll_dice()

            if not self._move_player(roll):
                continue

            self._ask_question()

            self._check_answer()

            if self._did_player_win():
                break

    def _is_player_in_penalty_box(self) -> bool:
        return self.current_player.is_in_penalty_box

    def _did_player_win(self) -> bool:
        return self.current_player.purse >= 6

    def _cycle_to_next_player(self) -> None:
        self.current_player_index = (self.current_player_index + 1) % self.nb_of_players

        self.logger.info(f"{self.current_player.name} is the current player")

    def _roll_dice(self) -> int:
        roll = random.randrange(5) + 1
        self.logger.info(f"They have rolled a {roll}")
        return roll

    def _move_player(self, roll: int) -> bool:
        if self._is_player_in_penalty_box():
            if roll % 2 != 0:
                self.logger.info(f"{self.current_player.name} is getting out of the penalty box")
            else:
                self.logger.info(f"{self.current_player.name} is not getting out of the penalty box")
                return False

        self._update_player_position(roll)

        return True

    def _update_player_position(self, nb_steps: int) -> None:
        player = self.current_player
        player.place = (player.place + nb_steps) % 12
        self.logger.info(f"{player.name}'s new location is {player.place}")

    def _ask_question(self) -> None:
        self.logger.info(f"The category is {self.current_category}")
        self.logger.info(self.questions[self.current_category].popleft())

    def _check_answer(self) -> None:
        if random.randrange(9) == 7:
            self._punish_wrong_answer()
        else:
            self._reward_right_answer()

    def _reward_right_answer(self) -> None:
        self.current_player.purse += 1

        self.logger.info("Answer was correct!!!!")
        self.logger.info(f"{self.current_player.name} now has {self.current_player.purse} Gold Coins.")

    def _punish_wrong_answer(self) -> None:
        self.current_player.is_in_penalty_box = True

        self.logger.info("Question was incorrectly answered")
        self.logger.info(f"{self.current_player.name} was sent to the penalty box")


if __name__ == '__main__':
    game = Game()

    game.add_new_player('Chet')
    game.add_new_player('Pat')
    game.add_new_player('Sue')

    game.play()
