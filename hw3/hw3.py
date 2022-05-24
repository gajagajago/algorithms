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

    def print(self):
        print("<<Adj List>>")

        for j in range(STARTING_VERTEX, self.nr_vertices+1):
            adjacent_vertices = []
            entity = self.list[j].next

            while entity is not None:
                adjacent_vertices.append(str(entity.val))
                entity = entity.next
            print("{}: {}".format(j, "->".join(adjacent_vertices)))


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
            self.array.append(val)
        else:
            idx = to
            for j in range(fr, to):
                if self.array[j] > val:
                    idx = j
                    break
            self.array.insert(idx, val)

    def print(self):
        print("<<Adj Array>>")

        for j in range(STARTING_VERTEX, self.nr_vertices+1):
            n = self.pos_list[j] - self.pos_list[j-1]
            list = self.array[self.pos_list[j]-n+1: self.pos_list[j]+1]
            list = [str(li) for li in list]

            print("{}: {}".format(j, "->".join(list)))


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

        adj_matrix.print()
        adj_list.print()
        adj_array.print()

