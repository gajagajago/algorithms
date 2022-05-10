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

        if p is not self.root:
            if p == p2.lc:
                p2.lc = x
            else:
                p2.rc = x
        else:
            self.root = x

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

        if p is not self.root:
            if p == p2.lc:
                p2.lc = x
            else:
                p2.rc = x
        else:
            self.root = x

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
                return 0

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

        return val

    # x is black. x is p.lc
    def __deleteL(self, x: RBNode):
        p = x.p
        s = p.rc
        l = s.lc
        r = s.rc

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
            # Re-set x due to some error
            x = p.lc
            x.p = p
            #
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
            # Re-set x due to some error
            x = p.rc
            x.p = p
            #
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
        target = self.get(val)

        if target is None:
            return 0
        else:
            self.nr = self.nr - 1
            m = target.successor()

            # When deleting root
            if target == self.root:
                # with no successor
                if target == m:
                    target.lc.p = target.p
                    target.lc.color = 'B'
                    self.root = target.lc
                    return val

            target.val, m.val = m.val, target.val
            p = m.p

            if m == p.lc:
                if m.color == 'R':
                    x = m.rc
                    p.lc = x
                    x.p = p
                else:  # m.color = 'B'
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

                c = x
                while c is not None:
                    c.fixSize()
                    c = c.p

            else:  # m == p.rc
                if m.color == 'R':
                    x = m.lc
                    p.rc = x
                    x.p = p
                else:  # m.color = 'B'
                    if not m.isNil():
                        if m.lc.color == 'R':
                            x = m.lc
                            p.rc = x
                            x.p = p
                            x.color = 'B'
                        elif m.rc.color == 'R':
                            x = m.rc
                            p.rc = x
                            x.p = p
                            x.color = 'B'
                        elif m.lc.color == 'B':
                            x = m.lc
                            p.rc = x
                            x.p = p
                            self.__deleteR(x)

                c = x
                while c is not None:
                    c.fixSize()
                    c = c.p

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


if __name__ == '__main__':
    # Fill in the directory where input.txt is located
    dir = "./input1/"
    line_cnt = 0

    with open(dir + "output.txt", "w") as f_out:
        # print inst list
        with open(dir + "input.txt", "r") as f_in:
            lines = f_in.readlines()
            for line in lines:
                f_out.write(line)
                line_cnt = line_cnt + 1
        tree = RBTree()

        with open(dir + "input.txt", "r") as f_in:
            lines = f_in.readlines()
            wr = ''

            for idx, line in enumerate(lines, start=0):
                inst, val = line.split(" ")
                val = int(val)

                wr = None
                if inst == 'I':
                    wr = tree.insert(val)
                elif inst == 'D':
                    wr = tree.delete(val)
                elif inst == 'S':
                    wr = tree.select(val)
                elif inst == 'R':
                    wr = tree.rank(val)

                f_out.write("{}\n".format(wr))

    ## checker
    MAX = 9999
    A = [0] * (MAX + 1)

    finalCheck = True

    with open(dir + "checker.txt", "w") as f_check:

        with open(dir + "output.txt", "r") as f_out:
            out_lines = f_out.readlines()

            with open(dir + "input.txt", "r") as f_in:
                lines = f_in.readlines()

                for line in lines:
                    inst, val = line.split(" ")
                    val = int(val)
                    result = int(out_lines[line_cnt])
                    check = None    # Result of checker

                    if inst == 'I':
                        if A[val] is 0:
                            A[val] = 1
                            check = val == result

                        elif A[val] is 1:
                            check = result == 0

                    elif inst == 'D':
                        if A[val] is 1:
                            A[val] = 0
                            check = val == result

                        elif A[val] is 0:
                            check = result == 0

                    elif inst == 'S':
                        if val > MAX:
                            check = result == 0

                        else:
                            cnt = 0
                            found = False
                            for i in range(0, MAX + 1):
                                cnt = cnt + A[i]
                                if cnt == val:
                                    found = True
                                    check = i == result
                                    break

                            # could not find
                            if not found:
                                check = result == 0

                    elif inst == 'R':
                        if A[val] == 1:
                            cnt = 0
                            for i in range(0, val + 1):
                                cnt = cnt + A[i]

                            check = cnt == result

                        elif A[val] == 0:
                            check = result == 0

                    # Write check result to checker.txt
                    if check:
                        f_check.write("Correct\n")
                    else:
                        f_check.write("False\n")
                        finalCheck = False

                    line_cnt = line_cnt + 1

    print("Checker {}".format("Passed" if finalCheck else "Failed"))