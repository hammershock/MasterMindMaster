import ctypes
from typing import List

lib = ctypes.CDLL('./libsolver.so')

lib.compare2.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int)]
lib.compare2.restype = None
lib.calculate.argtypes = [ctypes.c_char_p, ctypes.POINTER(ctypes.c_char_p), ctypes.c_size_t]
lib.calculate.restype = None


def compare_(answer: bytes, guess: bytes):
    num_a = ctypes.c_int()
    num_b = ctypes.c_int()
    lib.compare2(answer, guess, ctypes.byref(num_a), ctypes.byref(num_b))
    return num_a.value, num_b.value


def calculate(action: bytes, memory: List[bytes], number_of_digit):
    entropy = ctypes.c_double()
    array_type = ctypes.c_char_p * len(memory)
    n = ctypes.c_int(number_of_digit)
    memory_array = array_type(*memory)
    lib.calculate(action, memory_array, len(memory), ctypes.byref(entropy), n)
    return entropy.value, action.decode()


# 使用python的numpy完成compare_函数

# import numpy as np
# def compare_(answer: str, guess: str):
#     answer = np.array(list(answer))
#     guess = np.array(list(guess))
#     mask = answer == guess
#     num_a = np.sum(mask)
#     num_b = len(set.intersection(set(answer[~mask]), set(guess[~mask])))
#     return num_a, num_b
