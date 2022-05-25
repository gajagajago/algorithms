import numpy as np
import sys
from enum import Enum
from time import time

STARTING_VERTEX = 1
GRAPH_REPS = ["adj_mat", "adj_list", "adj_arr"]
RECURSION_LIMIT = 10**6


class Mode(Enum):
    adj_mat = 0
    adj_list = 1
    adj_arr = 2


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

    def addEntity(self, vi, v):
        """
        Add edge on AdjMatrix
        :param vi: Edge starting vertex
        :param v: Edge destination vertex
        """
        self.matrix[vi][v] = 1

    def transpose(self):
        """
        Transpose adjacency matrix
        :return: Transposed matrix
        """
        adj_matrix_t = AdjMatrix(self.nr_vertices)
        adj_matrix_t.matrix = self.matrix.T

        return adj_matrix_t

    def print(self):
        print("<<Adj Matrix>>")
        print(self.matrix)


def dfs_matrix(adjMatrix, nr_vertices, visited, start_vi, stack):
    """
    Perform DFS on AdjMatrix
    :param adjMatrix: Adjacency matrix
    :param nr_vertices: Number of vertices in matrix
    :param visited: Boolean list of visit info for each vertex. Must be init to all False at 1st call
    :param start_vi: Index of vertex to start DFS
    :param stack: Data structure to save DFS order
    :return: DFS order of vertices
    """
    visited[start_vi] = True

    for vi in range(STARTING_VERTEX, nr_vertices + 1):
        """" Recurse on adjacent && unvisited nodes """
        if visited[vi] is False and adjMatrix.matrix[start_vi][vi] == 1:
            dfs_matrix(adjMatrix, nr_vertices, visited, vi, stack)

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

        for vi in range(STARTING_VERTEX, self.nr_vertices + 1):
            entity = self.list[vi].next
            while entity is not None:
                adj_list_t.addEntity(entity.val, ListEntity(vi))
                entity = entity.next

        return adj_list_t

    def print(self):
        print("<<Adj List>>")

        for j in range(STARTING_VERTEX, self.nr_vertices + 1):
            adjacent_vertices = []
            entity = self.list[j].next

            while entity is not None:
                adjacent_vertices.append(str(entity.val))
                entity = entity.next
            print("{}: {}".format(j, "->".join(adjacent_vertices)))


def dfs_list(adjList, visited, start_vi, stack):
    """
    Perform DFS on AdjList
    :param adjList: Adjacency List
    :param visited: Boolean list of visit info for each vertex. Must be init to all False at 1st call
    :param start_vi: Index of vertex to start DFS
    :param stack: Data structure to save DFS order
    :return: DFS order of vertices
    """
    visited[start_vi] = True
    entity = adjList.list[start_vi].next

    """
    Core logic
    While traversing adjacent nodes from start_vi, should not break but just continue if a node is visited
    """
    while entity is not None:
        if visited[entity.val] == 0:
            dfs_list(adjList, visited, entity.val, stack)
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
        self.pos_list = [0 for _ in range(nrv + 1)]
        self.array = [0]

    def addEntity(self, vi, val):
        """
        Add value to adjacency array
        :param vi: Vertex number
        :param val: Value to be added
        """
        for i in range(vi, self.nr_vertices + 1):
            self.pos_list[i] = self.pos_list[i] + 1

        fr = self.pos_list[vi - 1] + 1
        to = self.pos_list[vi]

        if to == fr:
            self.array.insert(to, val)
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

        for start_vi in range(STARTING_VERTEX, self.nr_vertices + 1):
            fr = self.pos_list[start_vi - 1] + 1
            to = self.pos_list[start_vi]

            for i in range(fr, to + 1):
                vi = self.array[i]
                adj_array_t.addEntity(vi, start_vi)

        return adj_array_t

    def print(self):
        print("<<Adj Array>>")

        for j in range(STARTING_VERTEX, self.nr_vertices + 1):
            n = self.pos_list[j] - self.pos_list[j - 1]
            list = self.array[self.pos_list[j] - n + 1: self.pos_list[j] + 1]
            list = [str(li) for li in list]

            print("{}: {}".format(j, "->".join(list)))


def dfs_array(adjArray, visited, start_vi, stack):
    """
    Perform DFS on AdjArray
    :param adjArray: Adjacency array
    :param visited: Boolean list of visit info for each vertex. Must be init to all False at 1st call
    :param start_vi: Index of vertex to start DFS
    :param stack: Data structure to save DFS order
    :return: DFS order of vertices
    """
    visited[start_vi] = True

    fr = adjArray.pos_list[start_vi - 1] + 1
    to = adjArray.pos_list[start_vi]

    for i in range(fr, to + 1):
        vi = adjArray.array[i]
        if visited[vi] == 0:
            dfs_array(adjArray, visited, vi, stack)

    stack.append(start_vi)

    return stack


if __name__ == "__main__":
    """ System settings """
    sys.setrecursionlimit(RECURSION_LIMIT)

    """ Parse command line arguments """
    input_path, output_path, graph_rep = sys.argv[1:]
    if graph_rep not in GRAPH_REPS:
        raise Exception("Invalid graph representation")
    else:
        mode = Mode[graph_rep]

    with open(input_path, "r") as f_in:
        nr_vertices = int(f_in.readline())

        """ Setup global data structure """
        if mode is Mode.adj_mat:
            adj_matrix = AdjMatrix(nr_vertices)
        elif mode is Mode.adj_list:
            adj_list = AdjList(nr_vertices)
        elif mode is Mode.adj_arr:
            adj_array = AdjArray(nr_vertices)

        lines = f_in.readlines()
        vi = STARTING_VERTEX

        for line in lines:
            v_list = [int(v) for v in line.split(" ")]
            nr_v = v_list.pop(0)

            if nr_v is not 0:
                for v in v_list:
                    if mode is Mode.adj_mat:
                        adj_matrix.addEntity(vi, v)
                    elif mode is Mode.adj_list:
                        adj_list.addEntity(vi, ListEntity(v))
                    elif mode is Mode.adj_arr:
                        adj_array.addEntity(vi, v)

            vi = vi + 1

        """ Print graph representations """
        # if mode is Mode.adj_mat:
        #     adj_matrix.print()
        # elif mode is Mode.adj_list:
        #     adj_list.print()
        # elif mode is Mode.adj_arr:
        #     adj_array.print()

        """ Get results """
        t_start = time()
        t_end = None
        scc_list = []

        # 1. adj_matrix
        if mode is Mode.adj_mat:
            visited = [False for _ in range(adj_matrix.nr_vertices + 1)]
            stack = []

            while not all(visited):
                start_vi = visited.index(False)
                dfs_matrix(adj_matrix, adj_matrix.nr_vertices, visited, start_vi, stack)

            g_r = adj_matrix.transpose()
            f = stack.copy()

            visited = [False for _ in range(adj_matrix.nr_vertices + 1)]
            stack = []

            while not all(visited):
                start_vi = f.pop()
                if start_vi == 0:
                    break
                if visited[start_vi] is False:
                    tree = dfs_matrix(g_r, adj_matrix.nr_vertices, visited, start_vi, stack)
                    scc_list.append(tree)
                    stack = []

            """ Record time """
            t_end = time()

        # 2. adj_list
        elif mode is Mode.adj_list:
            visited = [False for _ in range(adj_list.nr_vertices + 1)]
            stack = []

            while not all(visited):
                start_vi = visited.index(False)
                dfs_list(adj_list, visited, start_vi, stack)

            g_r = adj_list.transpose()
            f = stack.copy()

            visited = [False for _ in range(adj_list.nr_vertices + 1)]
            stack = []

            while not all(visited):
                start_vi = f.pop()
                if start_vi == 0:
                    break
                if visited[start_vi] is False:
                    tree = dfs_list(g_r, visited, start_vi, stack)
                    scc_list.append(tree)
                    stack = []

            """ Record time """
            t_end = time()

        # 3. adj_array
        elif mode is Mode.adj_arr:
            visited = [False for _ in range(adj_array.nr_vertices + 1)]
            stack = []

            while not all(visited):
                start_vi = visited.index(False)
                dfs_array(adj_array, visited, start_vi, stack)

            g_r = adj_array.transpose()
            f = stack.copy()

            visited = [False for _ in range(adj_array.nr_vertices + 1)]
            stack = []

            while not all(visited):
                start_vi = f.pop()
                if start_vi == 0:
                    break
                if visited[start_vi] is False:
                    tree = dfs_array(g_r, visited, start_vi, stack)
                    scc_list.append(tree)
                    stack = []

            """ Record time"""
            t_end = time()

        """ Save results """
        for i in range(0, len(scc_list)):
            scc = scc_list[i]
            scc.sort()
            scc_list[i] = " ".join(map(str, scc))

        scc_list.sort()

        with open(output_path, "w") as f_out:
            """ Print the found scc to output path """
            for scc in scc_list:
                f_out.write(scc + "\n")

            """ Print elapsed time to output path """
            milliseconds = int((t_end - t_start) * 1000)
            f_out.write("{}ms".format(milliseconds))

            """ Print elapsed time to terminal """
            print("{}ms".format(milliseconds))