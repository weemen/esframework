from esframework.domain import AggregateRoot
from example.hangman.application.commands import StartGame, GuessLetter, GuessWord
from example.hangman.domain.events import GameStarted, LetterGuessed, LetterNotGuessed, WordGuessed, GameWon, GameLost
from example.hangman.exceptions import DomainException


class Game(AggregateRoot):
    """ Game is an aggregate root """
    __aggregate_root_id = None
    __active_game = False
    __tries = 0
    __word = ""
    __letters_guessed = []
    __letters_not_guessed = []
    __word_guessed = ""

    @staticmethod
    def start_game(command: StartGame):
        """ Creates Game and will try to apply GameStarted """
        game = Game()
        game.apply(GameStarted(
            aggregate_root_id=command.get_aggregate_root_id(),
            tries=command.get_tries(),
            word=command.get_word()
        ))

        return game

    def apply_game_started(self, event: GameStarted):
        """ Apply GameStarted on the aggregate root, reset the complete game"""
        self.__aggregate_root_id = event.get_aggregate_root_id()
        self.__active_game = True
        self.__tries = event.get_tries()
        self.__word = event.get_word()
        self.__letters_guessed = []
        self.__letters_not_guessed = []
        self.__word_guessed = ""

    def guess_letter(self, command: GuessLetter):
        """ Try to apply LetterGuessed or LetterNotGuessed """
        self.basic_game_preconditions()

        """ Apply either one the two events """
        if command.get_letter() in list(self.__word):
            self.apply_letter_guessed(
                LetterGuessed(
                    command.get_aggregate_root_id(),
                    command.get_letter()
                )
            )
        else:
            self.apply_letter_not_guessed(
                LetterNotGuessed(
                    command.get_aggregate_root_id(),
                    command.get_letter()
                )
            )

    def apply_letter_guessed(self, event: LetterGuessed):
        """ Apply LetterGuessed on the aggregate root """
        self.__letters_guessed.append(event.get_letter())

        if len(set(self.__word)) == len(set(self.__letters_guessed)):
            self.__active_game = False

    def apply_letter_not_guessed(self, event: LetterNotGuessed):
        """ Apply LetterNotGuessed on the aggregate root """
        self.__letters_not_guessed.append(event.get_letter())
        self.__tries -= 1

    def guess_word(self, command: GuessWord):
        """ Check preconditions try to apply WordGuessed """
        self.basic_game_preconditions()
        self.apply(
            WordGuessed(
                command.get_aggregate_root_id(),
                command.get_word()
            )
        )

        if 'word' == self.__word:
            self.apply_game_won(
                GameWon(command.get_aggregate_root_id()))
        else:
            self.apply_game_lost(
                GameLost(command.get_aggregate_root_id()))

    def apply_word_guessed(self, event: WordGuessed):
        """ Apply WordGuessed on the aggregate root """
        self.__word_guessed = event.get_word()

    def apply_game_won(self, event: GameWon):
        self.__active_game = False

    def apply_game_lost(self, event: GameLost):
        self.__active_game = False

    def get_aggregate_root_id(self):
        """ Get the aggregate root id of this aggregate """
        return self.__aggregate_root_id

    def basic_game_preconditions(self):
        if not self.__active_game:
            raise DomainException("You are game over!")

        if self.__tries <= 0:
            raise DomainException("Game doesn't have any tries left.")
