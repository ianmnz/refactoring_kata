# Trivia Refactor-kata from
# https://github.com/emilybache/trivia


from dataclasses import dataclass, field
from typing import Dict

@dataclass
class Player:
    id: int
    name: str
    place: int = field(default=0)
    purse: int = field(default=0)
    is_in_penalty_box: bool = field(default=False)


class Game:
    def __init__(self):
        self.players: Dict[int, Player] = dict()

        self.pop_questions = []
        self.science_questions = []
        self.sports_questions = []
        self.rock_questions = []

        self.current_player: int = 0
        self.is_getting_out_of_penalty_box = False

        for i in range(50):
            self.pop_questions.append("Pop Question %s" % i)
            self.science_questions.append("Science Question %s" % i)
            self.sports_questions.append("Sports Question %s" % i)
            self.rock_questions.append(self.create_rock_question(i))

    def create_rock_question(self, index):
        return "Rock Question %s" % index

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

    def roll(self, roll):
        print("%s is the current player" % self.get_current_player().name)
        print("They have rolled a %s" % roll)

        if self.get_current_player().is_in_penalty_box:
            if roll % 2 != 0:
                self.is_getting_out_of_penalty_box = True

                print("%s is getting out of the penalty box" % self.get_current_player().name)
                self.get_current_player().place = self.get_current_player().place + roll
                if self.get_current_player().place > 11:
                    self.get_current_player().place = self.get_current_player().place - 12

                print(self.get_current_player().name + \
                            '\'s new location is ' + \
                            str(self.get_current_player().place))
                print("The category is %s" % self._current_category)
                self._ask_question()
            else:
                print("%s is not getting out of the penalty box" % self.get_current_player().name)
                self.is_getting_out_of_penalty_box = False
        else:
            self.get_current_player().place = self.get_current_player().place + roll
            if self.get_current_player().place > 11:
                self.get_current_player().place = self.get_current_player().place - 12

            print(self.get_current_player().name + \
                        '\'s new location is ' + \
                        str(self.get_current_player().place))
            print("The category is %s" % self._current_category)
            self._ask_question()

    def _ask_question(self):
        if self._current_category == 'Pop': print(self.pop_questions.pop(0))
        if self._current_category == 'Science': print(self.science_questions.pop(0))
        if self._current_category == 'Sports': print(self.sports_questions.pop(0))
        if self._current_category == 'Rock': print(self.rock_questions.pop(0))

    @property
    def _current_category(self):
        if self.get_current_player().place == 0: return 'Pop'
        if self.get_current_player().place == 4: return 'Pop'
        if self.get_current_player().place == 8: return 'Pop'
        if self.get_current_player().place == 1: return 'Science'
        if self.get_current_player().place == 5: return 'Science'
        if self.get_current_player().place == 9: return 'Science'
        if self.get_current_player().place == 2: return 'Sports'
        if self.get_current_player().place == 6: return 'Sports'
        if self.get_current_player().place == 10: return 'Sports'
        return 'Rock'

    def was_correctly_answered(self):
        if self.get_current_player().is_in_penalty_box:
            if self.is_getting_out_of_penalty_box:
                print('Answer was correct!!!!')
                self.get_current_player().purse += 1
                print(self.get_current_player().name + \
                    ' now has ' + \
                    str(self.get_current_player().purse) + \
                    ' Gold Coins.')

                winner = self._did_player_win()
                self.current_player += 1
                if self.current_player == len(self.players): self.current_player = 0

                return winner
            else:
                self.current_player += 1
                if self.current_player == len(self.players): self.current_player = 0
                return True



        else:

            print("Answer was corrent!!!!")
            self.get_current_player().purse += 1
            print(self.get_current_player().name + \
                ' now has ' + \
                str(self.get_current_player().purse) + \
                ' Gold Coins.')

            winner = self._did_player_win()
            self.current_player += 1
            if self.current_player == len(self.players): self.current_player = 0

            return winner

    def wrong_answer(self):
        print('Question was incorrectly answered')
        print(self.get_current_player().name + " was sent to the penalty box")
        self.get_current_player().is_in_penalty_box = True

        self.current_player += 1
        if self.current_player == len(self.players): self.current_player = 0
        return True

    def _did_player_win(self):
        return not (self.get_current_player().purse == 6)


from random import randrange

if __name__ == '__main__':
    not_a_winner = False

    game = Game()

    game.add('Chet')
    game.add('Pat')
    game.add('Sue')

    while True:
        game.roll(randrange(5) + 1)

        if randrange(9) == 7:
            not_a_winner = game.wrong_answer()
        else:
            not_a_winner = game.was_correctly_answered()

        if not not_a_winner: break
