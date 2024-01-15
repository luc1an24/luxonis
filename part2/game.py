## game.py
class Game:
    """
    The Game class represents a game session between two players. It manages the game state,
    including the word to be guessed, hints provided, and the number of attempts made.
    """

    def __init__(self):
        self.word = ""
        self.hints = []
        self.attempts = 0
        self.player1 = ""
        self.player2 = ""

    def start_game(self, player1:str, player2: str, word: str) -> None:
        """
        Initializes a new game with the given word and opponent.

        Args:
            player1 (str): The identifier of the player that initiated the game.
            player2 (str): The identifier of the opponent player.
            word (str): The word to be guessed by the opponent.
        """
        self.player1 = player1
        self.player2 = player2
        self.word = word
        self.hints = []
        self.attempts = 0

    def get_opponent(self) -> str:
        return self.player2

    def guess_word(self, guess: str) -> bool:
        """
        Allows the opponent to guess the word and increments the attempt count.

        Args:
            guess (str): The opponent's guess for the word.

        Returns:
            bool: True if the guess is correct, False otherwise.
        """
        self.attempts += 1
        return guess.lower() == self.word.lower()

    def add_hint(self, hint: str) -> None:
        """
        Adds a hint to the game to help the opponent guess the word.

        Args:
            hint (str): A hint to help the opponent guess the word.
        """
        self.hints.append(hint)
