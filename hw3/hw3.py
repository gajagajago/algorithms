import numpy as np

STARTING_VERTEX = 1


class ListEntity:
    def __init__(self, val: int):
        self.val = val
        self.next = None

    def isTail(self):
        return self.next is None
    

class AdjMatrix:
    def __init__(self, nrv: int):
        """
        Initialize adjacency matrix
        :param nrv: Number of vertices
        """
        self.matrix = np.zeros((nrv + 1, nrv + 1), dtype=int)
        self.nr_vertices = nrv

    def print(self):
        print("<<Adj Matrix>>")
        print(self.matrix)


def dfs_matrix(matrix, nr_verticies, visited, start_vi, stack):
    visited[start_vi] = True

    for vi in range(STARTING_VERTEX, nr_verticies+1):
        """" Recurse on adjacent && unvisited nodes """
        if visited[vi] is False and matrix[start_vi][vi] == 1:
            dfs_matrix(matrix, nr_verticies, visited, vi, stack)

    stack.append(start_vi)

    return stack


class AdjList:
    def __init__(self, nrv: int):
        """
        Initialize adjacency list.
        Adjacency list must always be sorted
        :param nrv: Number of vertices
        """
        self.list = [ListEntity(None) for _ in range(nrv + 1)]
        self.nr_vertices = nrv

    def addEntity(self, vi: int, e: ListEntity):
        """
        Add entity to adjacency list
        :param vi: Vertex number
        :param e: Adding entity
        """
        curr = self.list[vi]

        while not curr.isTail():
            next = curr.next

            if e.val < next.val:
                e.next = next
                break
            else:
                curr = next

        curr.next = e

    def transpose(self):
        """
        Transpose adjacency list
        :return: Transposed list
        """
        adj_list_t = AdjList(self.nr_vertices)

        for vi in range(STARTING_VERTEX, self.nr_vertices+1):
            entity = self.list[vi].next
            while entity is not None:
                adj_list_t.addEntity(entity.val, ListEntity(vi))
                entity = entity.next

        return adj_list_t

    def print(self):
        print("<<Adj List>>")

        for j in range(STARTING_VERTEX, self.nr_vertices+1):
            adjacent_vertices = []
            entity = self.list[j].next

            while entity is not None:
                adjacent_vertices.append(str(entity.val))
                entity = entity.next
            print("{}: {}".format(j, "->".join(adjacent_vertices)))


def dfs_list(list, nr_verticies, visited, start_vi, stack):
    visited[start_vi] = True
    entity = list[start_vi].next

    """
    Core logic
    While traversing adjacent nodes from start_vi, should not break but just continue if a node is visited
    """
    while entity is not None:
        if visited[entity.val] == 0:
            dfs_list(list, nr_verticies, visited, entity.val, stack)
        entity = entity.next

    stack.append(start_vi)

    return stack


class AdjArray:
    def __init__(self, nrv: int):
        """
        Initialize adjacency array.
        Each 'partition' of adjacency array must always be sorted
        :param nrv: Number of vertices
        """
        self.nr_vertices = nrv
        self.pos_list = [0 for _ in range(nrv+1)]
        self.array = [0]

    def addEntity(self, vi, val):
        """
        Add value to adjacency array
        :param vi: Vertex number
        :param val: Value to be added
        """
        for i in range(vi, self.nr_vertices+1):
            self.pos_list[i] = self.pos_list[i] + 1

        fr = self.pos_list[vi - 1] + 1
        to = self.pos_list[vi]

        if to == fr:
            self.array.insert(to, val)
            # self.array.x(val)
        else:
            idx = to
            for j in range(fr, to):
                if self.array[j] > val:
                    idx = j
                    break
            self.array.insert(idx, val)

    def transpose(self):
        """
        Transpose adjacency array
        :return: Transposed adjacency array
        """
        adj_array_t = AdjArray(self.nr_vertices)

        for start_vi in range(STARTING_VERTEX, self.nr_vertices+1):
            fr = self.pos_list[start_vi - 1] + 1
            to = self.pos_list[start_vi]
            # print("fr: {} to: {}".format(fr, to))
            for i in range(fr, to+1):
                vi = self.array[i]
                # print("start_vi: %d vi: %d" % (start_vi, vi))

                adj_array_t.addEntity(vi, start_vi)

            # adj_array_t.print()

        return adj_array_t


    def print(self):
        print("<<Adj Array>>")

        for j in range(STARTING_VERTEX, self.nr_vertices+1):
            n = self.pos_list[j] - self.pos_list[j-1]
            list = self.array[self.pos_list[j]-n+1: self.pos_list[j]+1]
            list = [str(li) for li in list]

            print("{}: {}".format(j, "->".join(list)))

def dfs_array(adjArray, nr_verticies, visited, start_vi, stack):
    visited[start_vi] = True

    fr = adjArray.pos_list[start_vi - 1] + 1
    to = adjArray.pos_list[start_vi]

    for i in range(fr, to+1):
        vi = adjArray.array[i]
        if visited[vi] == 0:
            dfs_array(adjArray, nr_verticies, visited, vi, stack)

    stack.append(start_vi)

    return stack


if __name__ == "__main__":
    # Fill in the directory where input.txt is located
    dir = "./input/"

    with open(dir + "input.txt", "r") as f_in:
        nr_vertices = int(f_in.readline())

        """ Setup global data structures """
        adj_matrix = AdjMatrix(nr_vertices)
        adj_list = AdjList(nr_vertices)
        adj_array = AdjArray(nr_vertices)

        lines = f_in.readlines()
        vi = STARTING_VERTEX

        for line in lines:
            v_list = [int(v) for v in line.split(" ")]
            nr_v = v_list.pop(0)

            if nr_v is not 0:
                for v in v_list:
                    adj_matrix.matrix[vi][v] = 1
                    adj_list.addEntity(vi, ListEntity(v))
                    adj_array.addEntity(vi, v)

            vi = vi + 1

        """ Print graph representations """
        # adj_matrix.print()
        # adj_list.print()
        # adj_array.print()

        """ Get results """
        # 1. adj_matrix
        print("[Result] Adj Matrix")
        visited = [False for _ in range(adj_matrix.nr_vertices + 1)]
        stack = []

        while not all(visited):
            start_vi = visited.index(False)
            dfs_matrix(adj_matrix.matrix, adj_matrix.nr_vertices, visited, start_vi, stack)
        # print("Adj matrix stack", stack)

        g_r = adj_matrix.matrix.T
        f = stack.copy()

        visited = [False for _ in range(adj_matrix.nr_vertices + 1)]
        stack = []

        while not all(visited):
            start_vi = f.pop()
            if start_vi == 0:
                break
            if visited[start_vi] is False:
                tree = dfs_matrix(g_r, adj_matrix.nr_vertices, visited, start_vi, stack)
                print(tree)
                stack = []

        # 2. adj_list
        print("\n[Result] Adj List")
        visited = [False for _ in range(adj_list.nr_vertices + 1)]
        stack = []

        while not all(visited):
            start_vi = visited.index(False)
            dfs_list(adj_list.list, adj_list.nr_vertices, visited, start_vi, stack)

        g_r = adj_list.transpose()

        # print("Transposed adj list")
        # g_r.print()
        f = stack.copy()

        visited = [False for _ in range(adj_list.nr_vertices + 1)]
        stack = []

        while not all(visited):
            start_vi = f.pop()
            if start_vi == 0:
                break
            if visited[start_vi] is False:
                tree = dfs_list(g_r.list, adj_list.nr_vertices, visited, start_vi, stack)
                print(tree)
                stack = []

        # 3. adj_array
        print("\n[Result] Adj array")
        # print("Adj array position ", adj_array.pos_list)
        # print("Adj array vanilla ", adj_array.array)
        visited = [False for _ in range(adj_list.nr_vertices + 1)]
        stack = []

        while not all(visited):
            start_vi = visited.index(False)
            dfs_array(adj_array, adj_array.nr_vertices, visited, start_vi, stack)

        # print("Adj array stack", stack)
        g_r = adj_array.transpose()
        # print("Transposed adj array")
        # g_r.print()
        f = stack.copy()

        visited = [False for _ in range(adj_list.nr_vertices + 1)]
        stack = []

        while not all(visited):
            start_vi = f.pop()
            if start_vi == 0:
                break
            if visited[start_vi] is False:
                tree = dfs_array(g_r, adj_array.nr_vertices, visited, start_vi, stack)
                print(tree)
                stack = []