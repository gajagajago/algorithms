import random
import os

def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print('Error: Creating directory. ' + directory)

def makeInputs():
    dir = input("Directory to save: ")
    n = int(input("Number of elements: "))

    createFolder(dir)

    max_int = 10**3
    i = random.randint(0, n)

    with open(dir+"input.txt", "w") as f:
        f.write("{}\n".format(n))

        for j in range(n):
            f.write("{}".format(random.randint(0, max_int)))
            f.write(" ") if j != n-1 else f.write("\n")

        f.write("{}".format(i))

if __name__ == '__main__':
    makeInputs()