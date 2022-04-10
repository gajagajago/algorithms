def random_select(n, li, i):
    '''
    Finds i-th smallest element of li in average O(n) time
    :param n: # elements in li
    :param li: element list
    :param i: i-th smallest
    :return el: answer
    :return t: time taken
    '''

    return el, t

def deterministic_select(n, li, i):
    '''
    Finds i-th smallest element of li in worst O(n) time
    :param n: # elements in li
    :param li: element list
    :param i: i-th smallest
    :return el: answer
    :return t: time taken
    '''

    return el, t

if __name__ == '__main__':
    dir = "./test1/"

    # read input
    with open(dir+"input.txt", "r") as f_in:
        n, li, i = f_in.read().splitlines()

    # random_select
    el, t = random_select(n, li, i)
    f_random_out = open(dir+"random.txt", "w")
    f_random_out.write(el)
    f_random_out.write("\n")
    f_random_out.write(t)

    # check random_select

    # deter_select
    el, t = deterministic_select(n, li, i)
    f_deter_out = open(dir+"deter.txt", "w")
    f_deter_out.write(el)
    f_deter_out.write("\n")
    f_deter_out.write(t)

    # check random_select