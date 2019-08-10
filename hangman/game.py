from .exceptions import *
from random import choice


class GuessAttempt(object):

    def __init__(self, character, hit=False, miss=False):
        self.character = character
        self.hit = hit
        self.miss = miss

        if self.hit and self.miss:
            raise InvalidGuessAttempt()

    def is_hit(self):
        return self.hit

    def is_miss(self):
        return self.miss


class GuessWord(object):

    def __init__(self, answer):

        if not answer:
            raise InvalidWordException()

        self.answer = answer
        self.masked = '*' * len(self.answer)

    def perform_attempt(self, character=None):

        if not character or len(character) != 1:
            raise InvalidGuessedLetterException()

        if character.lower() not in self.answer.lower():
            return GuessAttempt(character, hit=False, miss=True)

        else:
            for index, letter in enumerate(self.answer):
                if letter.lower() == character.lower():
                    self.masked = self.masked[:index] + character.lower() + self.masked[index + 1:]

            return GuessAttempt(character, hit=True, miss=False)


class HangmanGame(object):
    WORD_LIST = ['rmotr', 'python', 'awesome']

    def __init__(self, word_list=WORD_LIST, number_of_guesses=5):
        self.word_list = word_list
        self.remaining_misses = number_of_guesses
        self.word = GuessWord(self.select_random_word(self.word_list))
        self.previous_guesses = []

    @classmethod
    def select_random_word(cls, list_of_words= None):

        if not list_of_words:
            raise InvalidListOfWordsException()

        else:
            return choice(list_of_words)

    def guess(self, character):

        if self.is_finished():
            raise GameFinishedException()

        else:
            last_masked_word = self.word.masked
            attempt = self.word.perform_attempt(character)

            if character not in self.previous_guesses:
                self.previous_guesses.append(character.lower())

            if self.is_won():
                raise GameWonException()

            else:

                if self.word.masked.lower() == last_masked_word.lower():
                    self.remaining_misses -= 1

                if self.is_lost():
                    raise GameLostException()

        return attempt

    def is_finished(self):
        return self.remaining_misses <= 0 or '*' not in self.word.masked

    def is_won(self):
        return self.word.masked == self.word.answer

    def is_lost(self):
        return self.word.masked != self.word.answer and self.remaining_misses == 0
