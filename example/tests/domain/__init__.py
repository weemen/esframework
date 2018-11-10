from esframework.tooling.aggregate import AggregateRootTestCase
from example.hangman.application.commands import StartGame, GuessLetter, GuessWord
from example.hangman.domain.aggregate import Game
from example.hangman.exceptions import DomainException


class GameTest(AggregateRootTestCase):

    def test_it_can_start_a_game(self):
        game_start_command = StartGame(
            '297F2CE9-CB4F-4BE2-8C86-21B911FC2663',
            'birthday',
            9
        )

        aggregate = Game.start_game(game_start_command)
        self.withAggregate(aggregate)\
            .assert_aggregate_property_state_equal_to('__tries', 9)
        self.withAggregate(aggregate) \
            .assert_aggregate_property_state_equal_to('__word', 'birthday')
        self.withAggregate(aggregate) \
            .assert_aggregate_property_state_equal_to('__active_game', True)
        self.withAggregate(aggregate) \
            .assert_aggregate_property_state_equal_to('__letters_guessed', [])
        self.withAggregate(aggregate) \
            .assert_aggregate_property_state_equal_to('__letters_not_guessed', [])
        self.withAggregate(aggregate) \
            .assert_aggregate_property_state_equal_to('__word_guessed', "")

    def test_it_can_guess_a_letter(self):
        aggregate_id = '297F2CE9-CB4F-4BE2-8C86-21B911FC2663'

        aggregate = Game.start_game(StartGame(aggregate_id, 'birthday', 9))
        aggregate.guess_letter(GuessLetter(aggregate_id, 'r'))

        self.withAggregate(aggregate) \
            .assert_aggregate_property_state_equal_to('__tries', 9)
        self.withAggregate(aggregate) \
            .assert_aggregate_property_state_equal_to('__word', 'birthday')
        self.withAggregate(aggregate) \
            .assert_aggregate_property_state_equal_to('__active_game', True)
        self.withAggregate(aggregate) \
            .assert_aggregate_property_state_equal_to('__letters_guessed', ['r'])
        self.withAggregate(aggregate) \
            .assert_aggregate_property_state_equal_to('__letters_not_guessed', [])
        self.withAggregate(aggregate) \
            .assert_aggregate_property_state_equal_to('__word_guessed', "")

    def test_it_can_guess_multiple_letters(self):
        aggregate_id = '297F2CE9-CB4F-4BE2-8C86-21B911FC2663'

        aggregate = Game.start_game(StartGame(aggregate_id, 'birthday', 9))
        aggregate.guess_letter(GuessLetter(aggregate_id, 'r'))
        aggregate.guess_letter(GuessLetter(aggregate_id, 'b'))

        self.withAggregate(aggregate) \
            .assert_aggregate_property_state_equal_to('__tries', 9)
        self.withAggregate(aggregate) \
            .assert_aggregate_property_state_equal_to('__word', 'birthday')
        self.withAggregate(aggregate) \
            .assert_aggregate_property_state_equal_to('__active_game', True)
        self.withAggregate(aggregate) \
            .assert_aggregate_property_state_equal_to('__letters_guessed', ['r', 'b'])
        self.withAggregate(aggregate) \
            .assert_aggregate_property_state_equal_to('__letters_not_guessed', [])
        self.withAggregate(aggregate) \
            .assert_aggregate_property_state_equal_to('__word_guessed', "")

    def test_it_can_guess_not_guess_letters(self):
        aggregate_id = '297F2CE9-CB4F-4BE2-8C86-21B911FC2663'

        aggregate = Game.start_game(StartGame(aggregate_id, 'birthday', 9))
        aggregate.guess_letter(GuessLetter(aggregate_id, 'x'))

        self.withAggregate(aggregate) \
            .assert_aggregate_property_state_equal_to('__tries', 8)
        self.withAggregate(aggregate) \
            .assert_aggregate_property_state_equal_to('__word', 'birthday')
        self.withAggregate(aggregate) \
            .assert_aggregate_property_state_equal_to('__active_game', True)
        self.withAggregate(aggregate) \
            .assert_aggregate_property_state_equal_to('__letters_guessed', [])
        self.withAggregate(aggregate) \
            .assert_aggregate_property_state_equal_to('__letters_not_guessed', ['x'])
        self.withAggregate(aggregate) \
            .assert_aggregate_property_state_equal_to('__word_guessed', "")

    def test_it_can_guess_word(self):
        aggregate_id = '297F2CE9-CB4F-4BE2-8C86-21B911FC2663'

        aggregate = Game.start_game(StartGame(aggregate_id, 'birthday', 9))
        aggregate.guess_word(GuessWord(aggregate_id, 'birthday'))

        self.withAggregate(aggregate) \
            .assert_aggregate_property_state_equal_to('__tries', 9)
        self.withAggregate(aggregate) \
            .assert_aggregate_property_state_equal_to('__word', 'birthday')
        self.withAggregate(aggregate) \
            .assert_aggregate_property_state_equal_to('__active_game', False)
        self.withAggregate(aggregate) \
            .assert_aggregate_property_state_equal_to('__letters_guessed', [])
        self.withAggregate(aggregate) \
            .assert_aggregate_property_state_equal_to('__letters_not_guessed', [])
        self.withAggregate(aggregate) \
            .assert_aggregate_property_state_equal_to('__word_guessed', "birthday")

    def test_it_can_not_guess_a_word(self):
        aggregate_id = '297F2CE9-CB4F-4BE2-8C86-21B911FC2663'

        aggregate = Game.start_game(StartGame(aggregate_id, 'birthday', 9))
        aggregate.guess_word(GuessWord(aggregate_id, 'pony'))

        self.withAggregate(aggregate) \
            .assert_aggregate_property_state_equal_to('__tries', 9)
        self.withAggregate(aggregate) \
            .assert_aggregate_property_state_equal_to('__word', 'birthday')
        self.withAggregate(aggregate) \
            .assert_aggregate_property_state_equal_to('__active_game', False)
        self.withAggregate(aggregate) \
            .assert_aggregate_property_state_equal_to('__letters_guessed', [])
        self.withAggregate(aggregate) \
            .assert_aggregate_property_state_equal_to('__letters_not_guessed', [])
        self.withAggregate(aggregate) \
            .assert_aggregate_property_state_equal_to('__word_guessed', "pony")

    def test_it_can_win_by_guessing_all_letters(self):
        aggregate_id = '297F2CE9-CB4F-4BE2-8C86-21B911FC2663'
        aggregate = Game.start_game(StartGame(aggregate_id, 'bird', 9))

        aggregate.guess_letter(GuessLetter(aggregate_id, 'x'))
        aggregate.guess_letter(GuessLetter(aggregate_id, 'r'))
        aggregate.guess_letter(GuessLetter(aggregate_id, 'd'))
        aggregate.guess_letter(GuessLetter(aggregate_id, 'b'))
        aggregate.guess_letter(GuessLetter(aggregate_id, 'i'))

        self.withAggregate(aggregate) \
            .assert_aggregate_property_state_equal_to('__tries', 8)
        self.withAggregate(aggregate) \
            .assert_aggregate_property_state_equal_to('__word', 'bird')
        self.withAggregate(aggregate) \
            .assert_aggregate_property_state_equal_to('__active_game', False)
        self.withAggregate(aggregate) \
            .assert_aggregate_property_state_equal_to('__letters_guessed', ['r','d','b','i'])
        self.withAggregate(aggregate) \
            .assert_aggregate_property_state_equal_to('__letters_not_guessed', ['x'])
        self.withAggregate(aggregate) \
            .assert_aggregate_property_state_equal_to('__word_guessed', "")

    def test_it_cant_guess_letters_when_no_tries_are_left(self):
        aggregate_id = '297F2CE9-CB4F-4BE2-8C86-21B911FC2663'
        aggregate = Game.start_game(StartGame(aggregate_id, 'birthday', 1))
        aggregate.guess_letter(GuessLetter(aggregate_id, 'x'))

        self.withAggregate(aggregate).expects_exception(
            DomainException,
            "Game doesn't have any tries left.",
            "guess_letter",
            GuessLetter(aggregate_id, 'x')
        )

    def test_it_cant_guess_words_when_game_over(self):
        aggregate_id = '297F2CE9-CB4F-4BE2-8C86-21B911FC2663'
        aggregate = Game.start_game(StartGame(aggregate_id, 'birthday', 1))
        aggregate.guess_word(GuessWord(aggregate_id, 'dog'))

        self.withAggregate(aggregate).expects_exception(
            DomainException,
            "You are game over!",
            "guess_word",
            GuessWord(aggregate_id, 'cat')
        )
