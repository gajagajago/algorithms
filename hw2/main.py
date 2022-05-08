class RBNode:
    def __init__(self, val: int, size: int, color: str):
        self.val = val
        self.size = size
        self.color = color  # 'R' OR 'B'
        self.p = self.lc = self.rc = None

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
            self.root = new
        elif new.p.val > new.val:
            p.lc = new
        else:
            p.rc = new

        return 0


if __name__ == '__main__':
    tree = RBTree()

    tree.insert(10)
    tree.insert(3)
    tree.insert(12)
    tree.insert(8)
    tree.insert(1)

    tree.root.display()

