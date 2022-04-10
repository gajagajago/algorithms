import time

def insertion_sort(li, p, r):
    '''
    Sort list in ascending order
    :param li: list to be sorted
    :param p: sort starting index
    :param r: sort end index
    '''
    # n = len(li)
    for i in range(p+1, r+1):
        j = i-1
        x = li[i]

        while j >= p and x < li[j]:
            li[j+1] = li[j]
            j -= 1

        li[j+1] = x


def partition(li, p, r, pi):
    '''
    Partition list based on pivot element
    :param li: partition target list
    :param p: start index of li
    :param r: end index of li
    :param pi: pivot index of li
    :return: final index of pivot
    '''
    li[pi], li[r] = li[r], li[pi]
    pivot = li[r]
    i = p-1

    for j in range(p, r):
        if li[j] < pivot:
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
    '''
    if p == r:
        return li[p]

    q = partition(li, p, r, r) # last element as pivot
    k = q-p+1

    if i < k:
        return random_select(li, p, q-1, i)
    elif i > k:
        return random_select(li, q+1, r, i-k)
    else:
        return li[q]

def deterministic_select(li, p, r, i):
    '''
    Finds i-th smallest element of li in worst O(n) time
    :param li: element list
    :param p: start index of li
    :param r: end index of li
    :param i: i-th smallest
    '''
    size = 5
    n = r-p+1

    if n <= size:
        insertion_sort(li)
        return li[i]

    grp_n, lo = divmod(n, size)
    if lo != 0:
        grp_n += 1
    print("Grps[%d], Leftover: %d\n" % (grp_n, lo))

    m = []
    for j in range(0, grp_n-1):
        insertion_sort(li[size*j : size*(j+1)])
        print(li[size*j : size*(j+1)])
        median = li[size*j + size//2]
        m.append(median)
        print("j[%d], median[%d]" % (j, median))

    if lo != 0:
        insertion_sort(li[size*(grp_n-1) : ])
        median = li[size*(grp_n-1) + lo//2]
    else:
        insertion_sort(li[size*(grp_n-1) : ])
        median = li[size*(grp_n-1) + size//2]
    m.append(median)
    print("j[%d], median[%d]" % (grp_n-1, median))

    # 4
    M = deterministic_select(m, 0, len(m)-1, (len(m)+1)//2)
    print("M[%d]" % M)

    q = partition(li, p, r, M)
    print("q[%d]" % q)

    k = q-p+1

    if i < k:
        return deterministic_select(li, p, q-1, i)
    elif i > k:
        return deterministic_select(li, q+1, r, i-k)
    else:
        return li[q]

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
        f_deter_out.write("{}\n{}".format(el, t_end - t_start))

    # check random_select