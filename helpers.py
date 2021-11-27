import numpy as np
from enum import Enum


def rand_idx(arrays):
    if len(arrays[0]) == 0: return -1
    rand_int = np.random.randint(len(arrays[0]))
    return (arrays[0][rand_int], arrays[1][rand_int])

def new_start_state():
    s = np.zeros((4, 13))
    val = Cards.PLAYER_1.value
    for i in [0,1]:
        for i in range(0, 10):
            coords = (np.random.randint(0,4), np.random.randint(0,13))
            while s[coords] != 0.0:
                coords = (np.random.randint(0,4), np.random.randint(0,13))
            s[coords] = val
        val = Cards.PLAYER_2.value

    stock = np.where(s == Cards.STOCK.value)
    s[rand_idx(stock)] = Cards.TOP_DISCARD.value
    stock = np.where(s == Cards.STOCK.value)
    s[rand_idx(stock)] = Cards.TOP_STOCK.value

    return s

class Cards(Enum):
    STOCK = 0
    PLAYER_1 = 1
    PLAYER_2 = 2
    TOP_DISCARD = 3
    NON_TOP_DISCARD = 4
    TOP_STOCK = 5