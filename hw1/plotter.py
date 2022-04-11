import matplotlib.pyplot as plt


def plot2(x1_fig, y1_fig, x2_fig, y2_fig, x1_label, x2_label):
    """
    Plots log scale graph
    :param x1_fig: list of x1 figures
    :param y1_fig: list of y1 figures
    :param x2_fig: list of x2 figures
    :param y2_fig: list of y2 figures
    :param x1_label: label of x1
    :param x2_label: label of x2
    """
    plt.figure(figsize=(8, 6))

    plt.scatter(x1_fig, y1_fig, color="orange")
    plt.plot(x1_fig, y1_fig, label=x1_label, color="orange")
    plt.scatter(x2_fig, y2_fig, color="blue")
    plt.plot(x2_fig, y2_fig, label=x2_label, color="blue")

    plt.grid()
    plt.xscale("log")
    plt.yscale("log")
    plt.xlabel("Input size",fontsize=20)
    plt.ylabel("Time(sec)",fontsize=20)
    plt.legend()
    plt.title("Time for Selection Algorithm", fontsize=20)

    plt.savefig("result.png", bbox_inches="tight")

if __name__ == '__main__':
    """
    Plots for 10**2 ~ 10**8
    """
    x1, y1, x2, y2 = ([] for i in range(4))

    for i in range(2, 9):
        dir = "./test10**{}/".format(i)

        x1.append(10**i)
        with open(dir+"random.txt", "r") as fr:
            lines = fr.readlines()
            sec = float(lines[1])
            y1.append(sec)

        x2.append(10**i)
        with open(dir+"deter.txt", "r") as fr:
            lines = fr.readlines()
            sec = float(lines[1])
            y2.append(sec)

    plot2(x1,y1,x2,y2, "random", "deter")