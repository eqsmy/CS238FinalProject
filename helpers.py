import numpy as np

def rand_idx(arrays):
    if len(arrays[0]) == 0: return -1
    rand_int = np.random.randint(len(arrays[0]))
    return (arrays[0][rand_int], arrays[1][rand_int])

def new_start_state():
    s = np.zeros((4, 13))
    val = 1
    for i in [0,1]:
        for i in range(0, 10):
            coords = (np.random.randint(0,4), np.random.randint(0,13))
            while s[coords] != 0.0:
                coords = (np.random.randint(0,4), np.random.randint(0,13))
            s[coords] = val
        val = 2

    stock = np.where(s == 0)
    s[rand_idx(stock)] = 3
    return s