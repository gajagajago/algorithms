import random
import os

def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print('Error: Creating directory. ' + directory)

if __name__ == '__main__':
    # Directory to save file
    dir = "./test5/"
    createFolder(dir)

    n = 10**8
    i = random.randint(0, n)

    with open(dir+"input.txt", "w") as f:
        f.write("{}\n".format(n))

        for j in range(n):
            f.write("{}".format(random.randint(0, n)))
            f.write(" ") if j != n-1 else f.write("\n")

        f.write("{}".format(i))