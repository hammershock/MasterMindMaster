import random

from cbindings import compare_

# 如果 NumPy 可用，则导入
NUMPY_READY = True
try:
    import numpy as np
except:
    NUMPY_READY = False


class ActionSpace:
    """
    ActionSpace 类用于生成和管理所有可能的动作（数字组合）。

    Attributes:
        actions_ (list): 存储所有可能动作的列表。
        number_of_digit (int): 数字组合的位数。

    Methods:
        init(): 初始化动作空间，生成所有可能的数字组合。
        sample(): 从动作空间中随机选择一个动作。
    """

    def __init__(self, number_of_digit):
        """
        构造函数。

        Args:
            number_of_digit (int): 数字组合的位数。
        """
        self.actions_: list = []
        self.number_of_digit = number_of_digit
        self.init()

    def init(self):
        """初始化动作空间，生成所有可能的数字组合。"""
        self.actions_ = [str(n).zfill(self.number_of_digit).encode() for n in range(10 ** self.number_of_digit)]

    def sample(self):
        """从动作空间中随机选择一个动作。

        Returns:
            str: 随机选取的动作。
        """
        return random.choice(self.actions_)


class Game:
    """
    Game 类用于创建和管理 Mastermind 游戏。

    Attributes:
        number_of_digit (int): 游戏中数字组合的位数。
        action_space (ActionSpace): 可执行动作的集合。
        __answer (str): 游戏的正确答案。
        steps (int): 当前已执行的步数。
        finished (bool): 游戏是否已结束。

    Methods:
        reset(): 重置游戏。
        peek_answer(): 查看当前的正确答案。
        step(guess: str): 执行一步游戏动作，返回游戏的反馈。
    """

    def __init__(self, number_of_digit=4):
        """
        构造函数。

        Args:
            number_of_digit (int): 游戏中数字组合的位数，默认为4。
        """
        self.number_of_digit = number_of_digit
        self.action_space = ActionSpace(number_of_digit)
        self.__answer = None
        self.steps = 0
        self.finished = False
        self.reset()

    def reset(self):
        """重置游戏，生成新的答案，并将步数和游戏状态重置。"""
        self.steps = 0
        self.finished = False
        self.__answer = str(random.randint(0, 10 ** self.number_of_digit - 1)).zfill(self.number_of_digit)

    def peek_answer(self) -> str:
        """
        获取游戏的当前答案。

        Returns:
            str: 当前游戏的正确答案。
        """
        return self.__answer

    def step(self, guess: str) -> str:
        """
        执行一步游戏动作。

        Args:
            guess (str): 玩家的猜测。

        Returns:
            str: 游戏根据玩家的猜测返回的反馈。
        """
        if not self.finished:
            assert len(guess) == self.number_of_digit, "输入必须为数字"
            num_a, num_b = compare_(self.__answer.encode(), guess.encode())
            self.steps += 1
            if num_a == self.number_of_digit:
                print(f"game finished in {self.steps} steps, congratulations!")
                self.finished = True
            return f"{num_a}A{num_b}B"


if __name__ == "__main__":
    game = Game()
    result = game.step("0156")
    print(result, game.peek_answer())


