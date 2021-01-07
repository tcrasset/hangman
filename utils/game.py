from typing import List, Union
import random
from collections import Counter


class Hangman:
    mandatory_words = ["becode", "learning", "mathematics", "sessions"]
    blank_char = "*"

    def __init__(self, possible_words: List[str]):
        """Creates the Hangman object.

        Args:
            possible_words (List[str]): list of words that can be selected as the target word
        """
        self.possible_words: List[str] = self._set_possible_words(possible_words)
        self.word_to_find: List[str] = self._select_word_to_find()
        self.lives: int = 5
        self.well_guessed_letters: List[str] = [
            self.blank_char for i in range(len(self.word_to_find))
        ]
        self.wrongly_guessed_letters: List[str] = []
        self.turn_count: int = 0
        self.error_count: int = 0
        self.good_answers_count: int = 0

    def start_game(self) -> None:
        """Starts the Hangman game."""
        while True:
            self.play()
            self.turn_count += 1

            self._display_info()
            if self._has_lost():
                self.game_over()
            elif self._has_won():
                self.well_played()

    def _display_info(self) -> None:
        """Displays information about the current state of the game to terminal."""
        word = "".join(self.well_guessed_letters)
        print(f"[{self.turn_count}] Word: {word}")
        print(f"Wrong guesses: {self.wrongly_guessed_letters}")
        print(f"Lives left: {self.lives}")

    def play(self) -> None:
        """Plays one turn of the hangman game, asking a letter
        from the user.
        """
        letter = self._get_input()
        if letter:
            self._try_guessing_letter(letter)

    def _get_input(self) -> Union[None, str]:
        """Gets the input letter from the user.

        Returns:
            Union[None, str]: Returns the letter chosen by the user.

                Returns None if the user didn't not choose a
                valid letter or more than one.
        """
        user_in = input("Letter to guess: ")
        if user_in.isalpha() and len(user_in) == 1:
            return user_in
        print("Only a single letter is allowed.")

    def _try_guessing_letter(self, letter: str) -> None:
        """Checks if `letter` is present in the word and reveals it
        if it is, possibly at multiple location.

        Otherwise, it decreases the number of lives and updates the list of
        wrongly guessed letters.

        Args:
            letter (str): [description]
        """
        indices = [i for i, x in enumerate(self.word_to_find) if x == letter]
        if indices:
            for index in indices:
                self.well_guessed_letters[index] = letter
        else:
            self.wrongly_guessed_letters.append(letter)
            self.error_count += 1
            self.lives -= 1

    def game_over(self) -> None:
        """Exits the game while showing the user he lost."""
        print("Game over...")
        exit(1)

    def well_played(self) -> None:
        """Exits the game while showing the user he won."""
        word = "".join(self.word_to_find)
        print(
            f"You found the word: {word} in {self.turn_count} turns with {self.error_count} errors!"
        )
        exit(0)

    def _has_won(self) -> bool:
        """Returns True if the game is won. False otherwise.

        The game is won if all the characters of the word in
        question have been uncovered. This is the same as to
        say that there are no blank characters left.

        Returns:
            bool: returns whether the game is won
        """
        return self.well_guessed_letters.count(self.blank_char) == 0

    def _has_lost(self) -> bool:
        """Returns True if the game is lost. False otherwise.

        Returns:
            bool: returns whether the game is won
        """
        return self.lives == 0

    def _set_possible_words(self, possible_words: List[str]) -> List[str]:
        """Creates the list of all the possible words for the game, using
        `possible_words` and appending mandatory words.

        Args:
            possible_words (List[str]): list of possible words to include
        Returns:
            List[str]: final list of possible words, with mandatory words added
        """
        possible_and_mandatory_words = possible_words.copy()
        for word in self.mandatory_words:
            if word not in possible_words:
                possible_and_mandatory_words.append(word)

        return possible_and_mandatory_words

    def _select_word_to_find(self) -> List[str]:
        """Randomly select a word from `self.possible_words`.

        Returns:
            List[str]: list of characters of the word
        """
        chosen_word = random.choice(self.possible_words)
        return [letter for letter in chosen_word]
