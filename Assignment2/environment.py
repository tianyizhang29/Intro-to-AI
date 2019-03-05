import numpy as np

# d * d board contains n mines
# value -1 means this position is mine
def initial_environment(d, n):
    arr_dx = [-1, 0, 1]
    arr_dy = [-1, 0, 1]
    map = np.arange(d * d)
    np.random.shuffle(map)
    map = map.reshape(d, d)
    for i in range(d):
        for j in range(d):
            if map[i][j] < n:
                map[i][j] = -1

    for i in range(d):
        for j in range(d):
            if map[i][j] == -1:
                continue
            else:
                counter = 0
                for dx in arr_dx:
                    for dy in arr_dy:
                        if i + dx >= 0 and i + dx < d and j + dy >= 0 and j + dy < d:
                            if map[i+dx][j+dy] == -1:
                                counter += 1
                map[i][j] = counter

    # np.save("./%s_%s.npy" % (d, n), map)
    return map

if __name__ == '__main__':
    res = initial_environment(16,40)
    print(res)