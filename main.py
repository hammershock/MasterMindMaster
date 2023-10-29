import multiprocessing
from functools import partial
from typing import Dict

import numpy as np

from cbindings import compare_, calculate
from game import Game

tqdm_exists = True
try:
    from tqdm import tqdm
except ModuleNotFoundError:
    tqdm_exists = False


class Solver:
    """
        A Solver class for the Mastermind game, implementing an algorithm that
        optimizes guesses based on prior feedback to efficiently solve the game.

        Attributes:
            game (Game): An instance of the Game class representing the current game.
            last_guess (str or None): The last guess made by the solver.
            memory (list): A list of potential answers still remaining, updated as the game progresses.

        Methods:
            guess(vbar=False): Makes an optimized guess based on the current state of the game.
            update(feedback, guess=None): Updates the solver's memory based on the feedback received.
            step(guess): Makes a guess in the game and updates the game state.
            auto(pbar=False): Automatically plays the game until it's solved, making and updating guesses.
        """

    def __init__(self, game: Game):
        """
                Initializes the Solver with a Game instance.

                Args:
                    game (Game): An instance of the Game class.
                """
        self.game = game
        self.last_guess = None
        self.memory = game.action_space.actions_.copy()
        self.history = ()
        self.cache: Dict[tuple, bytes] = {}

    def reset(self, answer=None):
        self.last_guess = None
        self.memory = game.action_space.actions_.copy()
        self.game.reset(answer=answer)
        self.history = ()

    def guess(self, vbar=False):
        """
                Makes an optimized guess by evaluating all possible actions and selecting the one
                with the highest expected information gain.

                Args:
                    vbar (bool): If True and tqdm is available, displays a progress bar for the calculation.
                    entropy_threshold (float):
                Returns:
                    str: The best guess based on the current game state.

                """
        if len(self.memory) == 1:
            return self.memory[0].decode()
        if self.history in self.cache:
            return self.cache[self.history].decode()
        if len(self.memory) == 10 ** self.game.number_of_digit:
            return ("0123456789"*(self.game.number_of_digit//10+1))[:self.game.number_of_digit]

        process = partial(calculate, memory=self.memory, number_of_digit=self.game.number_of_digit)
        actions = self.game.action_space.actions_
        wrapper = tqdm if vbar and tqdm_exists else lambda x, total: x
        with multiprocessing.Pool(processes=multiprocessing.cpu_count()) as pool:
            entropy, self.last_guess = max(wrapper(pool.imap(process, actions), total=len(actions)))
            return self.last_guess

    def update(self, feedback, guess: str = None):
        """
                Updates the memory of the Solver based on the feedback from the last guess.

                Args:
                    feedback (tuple or str): The feedback received from the last guess.
                    guess (str, optional): The last guess. If None, uses the solver's last_guess attribute.

                Returns:
                    None
                """
        feedback = (int(feedback[0]), int(feedback[2])) if isinstance(feedback, str) else feedback
        guess = self.last_guess if guess is None else guess.encode()  # bytes
        self.cache[self.history] = guess
        self.history += (feedback, )
        self.memory = [answer for answer in self.memory if compare_(answer, guess) == feedback]

    def step(self, guess):
        """
                Executes a guessing step in the game, including making a guess, receiving feedback,
                and updating the solver's state.

                Args:
                    guess (str): The guess to be made in this step.

                Returns:
                    str: The feedback received from the guess.
                """
        feedback = self.game.step(guess)
        self.update(feedback, guess)
        return feedback

    def auto(self, pbar=False, verbose=False):
        """
                Automatically plays through the Mastermind game, making and updating guesses
                until the game is solved.

                Args:
                    pbar (bool): If True and tqdm is available, shows a progress bar during the game.

                Returns:
                    None
                """
        while not self.game.finished:
            guess = self.guess(pbar)
            feedback = self.step(guess)
            if verbose:
                print(game.steps, f"guess {guess} -> {feedback}", len(self.memory))
        return self.game.steps

    def benchmark(self):
        total_steps = 0
        pbar = tqdm(enumerate(game.action_space.actions_), total=10 ** self.game.number_of_digit)
        for i, answer in pbar:
            self.reset(answer.decode())
            steps = self.auto()
            total_steps += steps
            mean_steps = total_steps / (i + 1)
            pbar.set_postfix(mean_steps=np.array(mean_steps), current_steps=steps)


if __name__ == "__main__":
    game = Game(4, verbose=False)
    solver = Solver(game)
    # solver.auto(pbar=True)
    solver.benchmark()
