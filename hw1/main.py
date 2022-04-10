import time


def insertion_sort(li, p, r):
    """
    Sort list in ascending order
    :param li: list to be sorted
    :param p: sort starting index
    :param r: sort end index
    """
    for i in range(p + 1, r + 1):
        j = i - 1
        x = li[i]

        while j >= p and x < li[j]:
            li[j + 1] = li[j]
            j -= 1

        li[j + 1] = x


def partition(li, p, r, pi):
    """
    Partition list based on pivot element
    :param li: partition target list
    :param p: start index of li
    :param r: end index of li
    :param pi: pivot index of li
    :return: final index of pivot
    """
    li[pi], li[r] = li[r], li[pi]
    pivot = li[r]
    i = p - 1

    for j in range(p, r):
        if li[j] <= pivot:
            i += 1
            li[i], li[j] = li[j], li[i]
    li[i + 1], li[r] = li[r], li[i + 1]

    return i + 1


def partition_with_pivot(li, p, r, pivot):
    """
    Partition list based on pivot element
    :param li: partition target list
    :param p: start index of li
    :param r: end index of li
    :param pivot: pivot
    :return: final index of pivot
    """
    pi = li.index(pivot, p, r + 1)

    return partition(li, p, r, pi)


def random_select(li, p, r, i):
    """
    Finds i-th smallest element of li in average O(n) time
    :param li: element list
    :param p: start index of li
    :param r: end index of li
    :param i: i-th smallest
    """
    if p == r:
        return li[p]

    q = partition(li, p, r, r)  # last element as pivot
    k = q - p + 1

    if i < k:
        return random_select(li, p, q - 1, i)
    elif i > k:
        return random_select(li, q + 1, r, i - k)
    else:
        return li[q]


def deterministic_select(li, p, r, i):
    """
    Finds i-th smallest element of li in worst O(n) time
    :param li: element list
    :param p: start index of li
    :param r: end index of li
    :param i: i-th smallest
    """

    # make copy of li
    li = li[:]

    size = 5
    n = r - p + 1

    if n <= size:
        insertion_sort(li, p, r)
        print("sorted li: ", li)
        return li[p + i - 1]

    # make groups
    grps = [[] for _ in range((n + 4) // 5)]
    for e in range(p, r + 1):
        grps[(e - p) // 5].append(li[e])

    # find medians
    medians = [deterministic_select(grp, 0, len(grp) - 1, (len(grp) + 1) // 2) for grp in grps]

    print("grps: ", grps)
    print("medians: ", medians)

    # find M of medians
    M = deterministic_select(medians, 0, len(medians) - 1, (len(medians) + 1) // 2)
    print("M: ", M)

    q = partition_with_pivot(li, p, r, M)
    print("li after partition: ", li)
    print("q[%d]" % q)

    k = q - p + 1

    print("k: %d i: %d" % (k, i))
    print("p: %d r: %d" % (p, r))
    if i < k:
        return deterministic_select(li, p, q - 1, i)
    elif i > k:
        return deterministic_select(li, q + 1, r, i - k)
    else:
        return li[q]


if __name__ == '__main__':
    # Source directory of input file
    # Output files will also be saved here
    dir = "./test4/"

    # read input
    with open(dir + "input.txt", "r") as f_in:
        n, li, i = f_in.read().splitlines()
        n = int(n)
        li = [int(el) for el in li.split(" ")]
        i = int(i)

    # random_select
    li_random = li[:]
    t_start = time.time()
    el = random_select(li_random, 0, n - 1, i)
    t_end = time.time()

    with open(dir + "random.txt", "w") as f_random_out:
        f_random_out.write("{}\n{}".format(el, t_end - t_start))

    # check random_select

    # deter_select
    li_deter = li[:]
    t_start = time.time()
    el = deterministic_select(li_deter, 0, n - 1, i)
    t_end = time.time()

    with open(dir + "deter.txt", "w") as f_deter_out:
        f_deter_out.write("{}\n{}".format(el, t_end - t_start))

    # check random_select
