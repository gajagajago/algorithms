import random


class RBNode:
    def __init__(self, val: int, size: int, color: str):
        self.val = val
        self.size = size
        self.color = color  # 'R' OR 'B'
        self.p = self.lc = self.rc = None

    def fixSize(self):
        self.size = self.lc.size + self.rc.size + 1

    def display(self):
        lines, *_ = self.__display_aux()
        for line in lines:
            print(line)

    def __display_aux(self):
        """Returns list of strings, width, height, and horizontal coordinate of the root."""
        # No child.
        if self.rc is None and self.lc is None:
            line = '{}({},{})'.format(self.val, self.size, self.color)
            width = len(line)
            height = 1
            middle = width // 2
            return [line], width, height, middle

        # Only left child.
        if self.rc is None:
            lines, n, p, x = self.lc.__display_aux()
            s = '{}({},{})'.format(self.val, self.size, self.color)
            u = len(s)
            first_line = (x + 1) * ' ' + (n - x - 1) * '_' + s
            second_line = x * ' ' + '/' + (n - x - 1 + u) * ' '
            shifted_lines = [line + u * ' ' for line in lines]
            return [first_line, second_line] + shifted_lines, n + u, p + 2, n + u // 2

        # Only right child.
        if self.lc is None:
            lines, n, p, x = self.rc.__display_aux()
            s = '{}({},{})'.format(self.val, self.size, self.color)
            u = len(s)
            first_line = s + x * '_' + (n - x) * ' '
            second_line = (u + x) * ' ' + '\\' + (n - x - 1) * ' '
            shifted_lines = [u * ' ' + line for line in lines]
            return [first_line, second_line] + shifted_lines, n + u, p + 2, u // 2

        # Two children.
        left, n, p, x = self.lc.__display_aux()
        right, m, q, y = self.rc.__display_aux()
        s = '{}({},{})'.format(self.val, self.size, self.color)
        u = len(s)
        first_line = (x + 1) * ' ' + (n - x - 1) * '_' + s + y * '_' + (m - y) * ' '
        second_line = x * ' ' + '/' + (n - x - 1 + u + y) * ' ' + '\\' + (m - y - 1) * ' '
        if p < q:
            left += [n * ' '] * (q - p)
        elif q < p:
            right += [m * ' '] * (p - q)
        zipped_lines = zip(left, right)
        lines = [first_line, second_line] + [a + u * ' ' + b for a, b in zipped_lines]
        return lines, n + m + u, max(p, q) + 2, n + u // 2


class RBTree:
    def __init__(self):
        self.nil = RBNode(None, 0, 'B')  # Assume nil node can't track its parent
        self.root = self.nil
        self.nr = 0

    def __makeNew(self, val: int):
        new = RBNode(val, 1, 'R')
        new.lc = new.rc = self.nil

        return new

    def __leftRotate(self, p: RBNode):
        x = p.rc
        p2 = p.p
        x.p = p2

        if p is self.root:
            self.root = x
        else:
            if p == p2.lc:
                p2.lc = x
            else:
                p2.rc = x

        p.rc = x.lc
        x.lc.p = p
        p.p = x
        x.lc = p

        # do not fix order
        p.fixSize()
        x.fixSize()

    def __rightRotate(self, p: RBNode):
        x = p.lc
        p2 = p.p
        x.p = p2

        if p is self.root:
            self.root = x
        else:
            if p == p2.lc:
                p2.lc = x
            else:
                p2.rc = x

        p.lc = x.rc
        x.rc.p = p
        p.p = x
        x.rc = p

        # do not fix order
        p.fixSize()
        x.fixSize()

    def __fixTree(self, x: RBNode):
        p = x.p
        p2 = p.p

        if p == p2.lc:
            s = p2.rc
            # case 1
            if s.color == 'R':
                p.color = s.color = 'B'
                p2.color = 'R'

                if p2 == self.root:
                    p2.color = 'B'
                    return
                else:
                    if p2.p.color == 'R':
                        self.__fixTree(p2)

            # case 2
            else:  # s.color == 'B':
                if x == p.rc:
                    self.__leftRotate(p)
                    self.__fixTree(p)
                else:
                    self.__rightRotate(p2)
                    p2.color, p.color = p.color, p2.color
        else:
            s = p2.lc
            # case 1
            if s.color == 'R':
                p.color = s.color = 'B'
                p2.color = 'R'

                if p2 == self.root:
                    p2.color = 'B'
                    return
                else:
                    if p2.p.color == 'R':
                        self.__fixTree(p2)

            # case 2
            else:  # s.color == 'B':
                if x == p.lc:
                    self.__rightRotate(p)
                    self.__fixTree(p)
                else:
                    self.__leftRotate(p2)
                    p2.color, p.color = p.color, p2.color

    def get(self, val: int):
        c = self.root

        while c is not self.nil:
            if c.val > val:
                c = c.lc
            elif c.val < val:
                c = c.rc
            else:
                return c

        print('RBNode with val %s not exist' % val)
        return None

    def insert(self, val: int):
        new = self.__makeNew(val)

        p = None
        c = self.root
        while c != self.nil:
            p = c
            if new.val < c.val:
                c = c.lc
            elif new.val > c.val:
                c = c.rc
            else:
                return val

        new.p = p
        if new.p is None:
            new.color = 'B'
            self.root = new
        elif new.p.val > new.val:
            p.lc = new
        else:
            p.rc = new

        # Adjust nr
        self.nr = self.nr + 1

        # Adjust size
        c = new
        while c.p is not None:
            c = c.p
            c.size = c.size + 1

        # Fix tree
        if new.color == 'R' and new.p.color == 'R':
            self.__fixTree(new)

        return 0

    def __select(self, x: RBNode, i: int):
        r = x.lc.size + 1

        if i == r:
            return x.val
        elif i < r:
            return self.__select(x.lc, i)
        else:
            return self.__select(x.rc, i - r)

    def select(self, i: int):
        if self.nr < i:
            return 0
        else:
            return self.__select(self.root, i)

    def rank(self, val: int):
        x = self.get(val)

        if x is None:
            return 0
        else:
            r = x.lc.size + 1
            y = x

            while y is not self.root:
                if y == y.p.rc:
                    r = r + y.p.lc.size + 1
                y = y.p

            return r


def insertTest1():
    # Test 1 Insertion
    # 1-1 p == p2.lc
    # 1-1-1
    tree = RBTree()

    tree.insert(5)
    tree.insert(3)
    tree.insert(7)
    tree.insert(2)
    tree.insert(4)
    tree.insert(1)

    x = tree.get(1)
    if x.p.color == 'B' and x.p.p.color == 'R' and x.p.p.rc.color == 'B':
        print('Test 1-1-1 passed')
    else:
        print('Test 1-1-1 failed')

    # 1-1-2
    tree = RBTree()

    tree.insert(6)
    tree.insert(4)
    tree.insert(7)

    tree.insert(2)
    tree.insert(3)

    x = tree.get(3)
    if x.p.color == 'B' and x.lc.color == 'R' and x.rc.color == 'R' and x.rc.rc.color == 'B':
        print('Test 1-1-2 passed')
    else:
        print('Test 1-1-2 failed')


def insertTest2():
    # Test 2 Insertion
    # 1-2 p == p2.rc
    # 1-2-1
    tree = RBTree()

    tree.insert(5)
    tree.insert(3)
    tree.insert(8)
    tree.insert(7)
    tree.insert(9)
    tree.insert(6)

    x = tree.get(6)
    if x.p.color == 'B' and x.p.p.color == 'R' and x.p.p.lc.color == 'B':
        print('Test 1-2-1 passed')
    else:
        print('Test 1-2-1 failed')

    # 1-1-2
    tree = RBTree()

    tree.insert(6)
    tree.insert(4)
    tree.insert(7)

    tree.insert(9)
    tree.insert(8)

    x = tree.get(8)
    if x.p.color == 'B' and x.lc.color == 'R' and x.rc.color == 'R' and x.lc.lc.color == 'B':
        print('Test 1-2-2 passed')
    else:
        print('Test 1-2-2 failed')


def selectTest1():
    tree = RBTree()

    tree.insert(1)
    tree.insert(2)
    tree.insert(3)
    tree.insert(4)
    tree.insert(5)

    x = tree.select(5)

    if x == 5:
        print('Select test 1 passed')
    else:
        print('Select test 1 failed')


def selectTest2():
    tree = RBTree()
    ith = 5

    li = [5, 2, 4, 7, 6, 8, 9, 1, 10, 11, 3]

    for i in li:
        tree.insert(i)

    li.sort()
    ithItem = li[ith - 1]

    x = tree.select(ith)

    if x == ithItem:
        print('Select test 2 passed')
    else:
        print('Select test 2 failed')


def rankTest1():
    tree = RBTree()

    li = [i for i in range(1, 20)]
    random.shuffle(li)

    for i in li:
        tree.insert(i)

    random.shuffle(li)
    r = tree.rank(li[0])

    if r == li[0]:
        print('Rank test 1 passed')
    else:
        print('Rank test 1 failed')


if __name__ == '__main__':
    insertTest1()
    insertTest2()
    selectTest1()
    selectTest2()
    rankTest1()
