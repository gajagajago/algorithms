import random
import os
import numpy as np
import matplotlib.pyplot as plt

# Mode of input distribution
RANDOM = 0
NORMAL = 1
SKEWED = 2


def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print('Error: Creating directory. ' + directory)


def makeInputs():
    dir = input("Directory to save: ")
    if not dir[-1] == "/":
        dir += "/"

    n = int(input("Number of elements: "))
    mode = None
    f_name = None

    while mode is None:
        m = input("Input distribution [Random: 0, Normal: 1, Skewed: 2]: ")
        if m == "0":
            mode = RANDOM
            f_name = "input.txt"
        elif m == "1":
            mode = NORMAL
            f_name = "normal.txt"
        elif m == "2":
            mode = SKEWED
            f_name = "skewed.txt"
        else:
            continue

    createFolder(dir)

    i = random.randint(0, n)

    li = None

    if mode == RANDOM:
        li = (np.random.uniform(-1, 1, n) * n).astype(np.int32)
    elif mode == NORMAL:
        li = (np.random.normal(0, 1, n) * n).astype(np.int32)
    elif mode == SKEWED:
        li = (np.random.triangular(-1, 0.8, 1, n) * n).astype(np.int32)

    # Draw histogram of li distribution
    # plt.hist(li, bins=200, density=True)
    # title = "RANDOM" if mode == RANDOM else "NORMAL" if mode == NORMAL else "SKEWED"
    # plt.title(title + " Distribution(input size: " + str(n) + ")", fontsize=14)
    # plt.show()

    with open(dir + f_name, "w") as f:
        f.write("{}\n".format(n))

        for j in range(n):
            f.write("{}".format(li[j]))
            f.write(" ") if j != n - 1 else f.write("\n")

        f.write("{}".format(i))


if __name__ == '__main__':
    makeInputs()