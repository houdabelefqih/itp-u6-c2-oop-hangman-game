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
        self.number_of_guesses = number_of_guesses

    def select_random_word(list_of_words= None):

        if not list_of_words:
            raise InvalidListOfWordsException()

        else:
            return choice(list_of_words)
