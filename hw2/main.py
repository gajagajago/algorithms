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

    def __makeNew(self, val: int):
        new = RBNode(val, 1, 'R')
        new.lc = new.rc = self.nil

        return new

    def __leftRotate(self, p: RBNode):
        x = p.rc
        p2 = p.p

        x.p = p2
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
            else: # s.color == 'B':
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
            else: # s.color == 'B':
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

        # Adjust size
        c = new
        while c.p is not None:
            c = c.p
            c.size = c.size + 1

        # Fix tree
        if new.color == 'R' and new.p.color == 'R':
            self.__fixTree(new)

        return 0


if __name__ == '__main__':
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
    if x.p.color == 'B' and x.p.p.color == 'R' and x.p.p.p.color == 'B' and x.p.p.rc.color == 'B':
        print('Test 1-1-1 passed')
    else:
        print('Test 1-1-1 failed')

    # 1-1-2
    tree = RBTree()

    tree.insert(6)
    tree.insert(4)
    tree.insert(7)

    tree.insert(2)
    tree.insert(5)

    tree.insert(3)

    x = tree.get(3)
    if x.p.color == 'B' and x.p.rc.color == 'R':
        print('Test 1-1-2 passed')
    else:
        print('Test 1-1-2 failed')

    # 1-2 p == p2.rc
    # 1-2-1
    tree = RBTree()

    tree.insert(5)
    tree.insert(3)
    tree.insert(7)

    tree.insert(6)
    tree.insert(8)

    tree.insert(9)

    x = tree.get(9)
    if x.p.color == 'B' and x.p.p.color == 'R' and x.p.p.p.color == 'B' and x.p.p.lc.color == 'B':
        print('Test 1-2-1 passed')
    else:
        print('Test 1-2-1 failed')

    # 1-1-2
    tree = RBTree()

    tree.insert(5)
    tree.insert(3)
    tree.insert(8)

    tree.insert(6)
    tree.insert(10)

    tree.insert(9)

    x = tree.get(9)
    if x.p.color == 'B' and x.p.lc.color == 'R':
        print('Test 1-2-2 passed')
    else:
        print('Test 1-2-2 failed')

    # Test 2 Left rotate
    # tree.insert(5)
    # tree.insert(3)
    # tree.insert(7)
    #
    # tree.insert(8)
    #
    #
    # tree.root.display()