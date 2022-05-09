import random

VAL = 1

class RBNode:
    def __init__(self, val: int, size: int, color: str):
        self.val = val
        self.size = size
        self.color = color  # 'R' OR 'B'
        self.p = self.lc = self.rc = None

    def successor(self):
        s = self.rc

        if s.val is None:
            return self
        else:
            while s.lc.val is not None:
                s = s.lc

        return s

    def isNil(self):
        return self.size == 0

    def fixSize(self):
        if not self.isNil():
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

    def __updateRoot(self, x: RBNode):
        while x.p is not None:
            x = x.p

        self.root = x

    def __leftRotate(self, p: RBNode):
        x = p.rc
        p2 = p.p
        x.p = p2
        # if p2 is not self.root:
        # print("__left rotate: x({})p({})p2({}))".format(x.val, p.val, p2.val))

        if p is not self.root:
            # print("P is not root")
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

        # print("show result __left_rotate")
        # self.root.display()
        # if x.p is not None:
        #     print("x.p = ", x.p.val)

    def __rightRotate(self, p: RBNode):
        x = p.lc
        p2 = p.p
        x.p = p2

        if p is not self.root:
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

        # Update root
        self.__updateRoot(new)

        return 0

    # x is black. x is p.lc
    def __deleteL(self, x: RBNode):
        p = x.p
        s = p.rc
        l = s.lc
        r = s.rc

        # print("p({})s({})l({})r({})".format(p.val, s.val, l.val, r.val))

        pslr = p.color, s.color, l.color, r.color

        if pslr == ('R', 'B', 'B', 'B'):
            p.color, s.color = s.color, p.color
        elif pslr == ('R', 'B', 'R', 'R') or pslr == ('R', 'B', 'B', 'R') \
                or pslr == ('B', 'B', 'R', 'R') or pslr == ('B', 'B', 'B', 'R'):
            self.__leftRotate(p)
            p.color, s.color = s.color, p.color
            r.color = 'B'
        elif pslr == ('R', 'B', 'R', 'B') or pslr == ('B', 'B', 'R', 'B'):
            self.__rightRotate(s)
            l.color, s.color = s.color, l.color
            # s, l fix size
            s.fixSize()
            l.fixSize()
            self.__deleteL(x)
        elif pslr == ('B', 'B', 'B', 'B'):
            s.color = 'R'

            if p is not self.root:
                p2 = p.p
                if p == p2.lc:
                    self.__deleteL(p)
                else:
                    self.__deleteR(p)
        else:  # (BRBB)
            self.__leftRotate(p)
            p.color, s.color = s.color, p.color
            self.__deleteL(x)

    # x is black. x is p.rc
    def __deleteR(self, x: RBNode):
        p = x.p
        s = p.lc
        l = s.lc
        r = s.rc
        # print("x({})p({})s({}))".format(x.val, p.val, s.val))
        #
        # print("p({})s({})l({})r({})".format(p.val, s.val, l.val, r.val))
        pslr = p.color, s.color, l.color, r.color

        if pslr == ('R', 'B', 'B', 'B'):
            p.color, s.color = s.color, p.color
        elif pslr == ('R', 'B', 'R', 'R') or pslr == ('R', 'B', 'R', 'B') \
                or pslr == ('B', 'B', 'R', 'R') or pslr == ('B', 'B', 'R', 'B'):
            self.__rightRotate(p)
            p.color, s.color = s.color, p.color
            l.color = 'B'
        elif pslr == ('R', 'B', 'B', 'R') or pslr == ('B', 'B', 'B', 'R'):
            self.__leftRotate(s)
            r.color, s.color = s.color, r.color
            # s, r fix size
            s.fixSize()
            r.fixSize()
            self.__deleteR(x)
        elif pslr == ('B', 'B', 'B', 'B'):
            s.color = 'R'

            if p is not self.root:
                p2 = p.p
                if p == p2.lc:
                    self.__deleteL(p)
                else:
                    self.__deleteR(p)
        else:  # (BRBB)
            self.__rightRotate(p)
            p.color, s.color = s.color, p.color
            self.__deleteR(x)

    def delete(self, val: int):
        if VAL == val: print("delete val({})".format(val))
        target = self.get(val)

        if target is None:
            return 0
        else:
            self.nr = self.nr - 1
            m = target.successor()
            if VAL == val: print("delete m({}) m.p({})".format(m.val, m.p.val))

            target.val, m.val = m.val, target.val
            p = m.p

            if m == p.lc:
                if m.color == 'R':
                    x = m.rc
                    p.lc = x
                    x.p = p
                else:   # m.color = 'B'
                    if not m.isNil():
                        if m.lc.color == 'R':
                            x = m.lc
                            p.lc = x
                            x.p = p
                            x.color = 'B'
                        elif m.rc.color == 'R':
                            x = m.rc
                            p.lc = x
                            x.p = p
                            x.color = 'B'
                        elif m.rc.color == 'B':
                            x = m.rc
                            p.lc = x
                            x.p = p
                            self.__deleteL(x)

                # x = m.rc
                # if VAL == val: print("delete x({})".format(x.val))
                #
                # p.lc = x
                # x.p = p
                #
                # if m.color == 'B' and x.color == 'B':
                #     self.__deleteL(x)
                #
                # if x.color == 'R':
                #     x.color = 'B'

                c = x
                while c is not None:
                    c.fixSize()
                    c = c.p

                # update root
                self.__updateRoot(x)


            else:  # m == p.rc
                if m.color == 'R':
                    x = m.lc
                    p.rc = x
                    x.p = p
                else:   # m.color = 'B'
                    if not m.isNil():
                        if m.lc.color == 'R':
                            x = m.lc
                            p.lc = x
                            x.p = p
                            x.color = 'B'
                        elif m.rc.color == 'R':
                            x = m.rc
                            p.lc = x
                            x.p = p
                            x.color = 'B'
                        elif m.lc.color == 'B':
                            x = m.lc
                            p.rc = x
                            x.p = p
                            self.__deleteR(x)
                # x = m.lc
                # if VAL == val: print("delete x({})".format(x.val))
                #
                # p.rc = x
                # x.p = p
                #
                # if m.color == 'B' and x.color == 'B':
                #     self.__deleteR(x)
                #
                # if x.color == 'R':
                #     x.color = 'B'

                c = x
                while c is not None:
                    c.fixSize()
                    c = c.p

                # update root
                self.__updateRoot(x)

            return val

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


def test():
    tree = RBTree()

    li = [5, 2, 4, 7, 6, 8, 9, 1, 10, 11, 3]

    for i in li:
        print("-------------------------------")
        print("Insert({})".format(i))
        tree.insert(i)
        print("ROOT({})".format(tree.root.val))
        tree.root.display()
        print("-------------------------------")

    # 문제1
    lj = [9,7,3,11,2,8,4,6,1]
    for i in lj:
        print("-------------------------------")
        print("Delete({})".format(i))
        tree.delete(i)
        print("ROOT({})".format(tree.root.val))
        tree.root.display()
        print("-------------------------------")

    # random.shuffle(li)
    #
    # for i in li:
    #     print("-------------------------------")
    #     print("Delete({})".format(i))
    #     tree.delete(i)
    #     print("ROOT({})".format(tree.root.val))
    #     tree.root.display()
    #     print("-------------------------------")

def deleteTest1():
    tree = RBTree()

    li = [5, 2, 4, 7, 6, 8, 9, 1, 10, 11, 3]

    for i in li:
        tree.insert(i)

    tree.delete(6)

    if tree.root.val == 7:
        print('Delete test 1 passed')
    else:
        print('Delete test 1 failed')

    tree.root.display()

    tree.delete(10)
    tree.root.display()

    # tree.delete(8)
    # tree.root.display()
    #
    # tree.delete(11)
    # tree.root.display()


if __name__ == '__main__':
    # insertTest1()
    # insertTest2()
    # selectTest1()
    # selectTest2()
    # rankTest1()
    # deleteTest1()

    test()
