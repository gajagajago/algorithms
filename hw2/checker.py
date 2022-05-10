import random


if __name__ == '__main__':
    # Fill in the directory where input.txt should be created
    dir = './input1/'
    inst = ['I', 'D', 'S', 'R']

    MAX = 9999  # Do not modify -- has dependency on checker
    NUM_INST = 10**4    # Number of instructions to make

    with open(dir + "input.txt", "w") as f_in:
        for i in range(0, NUM_INST):
            n = random.randint(1, MAX)
            idx = random.randint(0, len(inst))
            f_in.write("{} {}\n".format(inst[idx], n))



