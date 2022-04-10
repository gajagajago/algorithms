import time

def insertion_sort(li):
    '''
    Sort list in ascending order
    :param li: list to be sorted
    '''
    n = len(li)
    for i in range(1, n):
        j = i-1
        x = li[i]

        while j >= 0 and x < li[j]:
            li[j+1] = li[j]
            j -= 1

        li[j+1] = x

def partition(li, p ,r):
    '''
    Partition list based on seed element
    Seed will be li[r] for this algorithm
    :param li: partition target list
    :param p: start index of li
    :param r: end index of li
    :return: final index of seed
    '''
    seed = li[r]
    i = p-1

    for j in range(p, r):
        if li[j] < seed:
            i += 1
            li[i], li[j] = li[j], li[i]
    li[i+1], li[r] = li[r], li[i+1]

    return i+1

def random_select(li, p, r, i):
    '''
    Finds i-th smallest element of li in average O(n) time
    :param li: element list
    :param p: start index of li
    :param r: end index of li
    :param i: i-th smallest
    :return el: answer
    '''
    if p == r:
        return li[p]

    q = partition(li, p, r)
    k = q-p+1

    if i < k:
        return random_select(li, p, q-1, i)
    elif i > k:
        return random_select(li, q+1, r, i-k)
    else:
        return li[q]

    return el

def deterministic_select(li, p, r, i):
    '''
    Finds i-th smallest element of li in worst O(n) time
    :param li: element list
    :param p: start index of li
    :param r: end index of li
    :param i: i-th smallest
    :return el: answer
    '''

    return el

if __name__ == '__main__':
    dir = "./test1/"

    # read input
    with open(dir+"input.txt", "r") as f_in:
        n, li, i = f_in.read().splitlines()
        n = int(n)
        li = [int(el) for el in li.split(" ")]
        i = int(i)

    # random_select
    li_random = li[:]
    t_start = time.time()
    el = random_select(li_random, 0, n-1, i)
    t_end = time.time()

    with open(dir+"random.txt", "w") as f_random_out:
        f_random_out.write("{}\n{}".format(el, t_end - t_start))

    # check random_select

    # deter_select
    li_deter = li[:]
    t_start = time.time()
    el = deterministic_select(li_deter, 0, n-1, i)
    t_end = time.time()

    with open(dir+"deter.txt", "w") as f_deter_out:
        f_deter_out.write(el)
        f_deter_out.write("\n")
        f_random_out.write(t_end - t_start)

    # check random_select