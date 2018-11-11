""" commandHandlers """
from esframework.repository import Repository
from example.hangman.application.commands import StartGame, GuessLetter, GuessWord
from example.hangman.domain.aggregate import Game


class GameCommandHandler(object):

    __repository = None

    def __init__(self, repository: Repository):
        self.__repository = repository

    def handle_start_game(self, command: StartGame):
        """ try to start a game """
        game = Game.start_game(command)
        self.__repository.save(game)

    def handle_guess_letter(self, command: GuessLetter):
        """ try to guess a letter """
        game = self.__repository.load(command.get_aggregate_root_id())
        game.guess_letter(command)

    def handle_guess_word(self, command: GuessWord):
        """ try to guess a word """
        game = self.__repository.load(command.get_aggregate_root_id())
        game.guess_word(command)
