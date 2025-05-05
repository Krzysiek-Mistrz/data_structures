class UnionFind:
    def __init__(self, n):
        self.p = list(range(n))
        self.size = [1] * n
    def find(self, v):
        if self.p[v] != v:
            self.p[v] = self.find(self.p[v])
        return self.p[v]
    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return False
        if self.size[ra] < self.size[rb]:
            ra, rb = rb, ra
        self.p[rb] = ra
        self.size[ra] += self.size[rb]
        return True
    def same(self, a, b):
        return self.find(a) == self.find(b)


class Graph:
    def __init__(self):
        self.adj = {}
        self.edges = []
    def insert_vertex(self, v):
        if v not in self.adj:
            self.adj[v] = []
    def insert_edge(self, u, v, w):
        self.insert_vertex(u)
        self.insert_vertex(v)
        self.adj[u].append((v, w))
        self.adj[v].append((u, w))
        self.edges.append((u, v, w))
    def vertices(self):
        return list(self.adj.keys())
    def neighbours(self, v):
        return list(self.adj[v])


def kruskal_mst(graph):
    verts = sorted(graph.vertices())
    idx = {v:i for i,v in enumerate(verts)}
    uf = UnionFind(len(verts))
    sorted_edges = sorted(graph.edges, key=lambda x: x[2])
    mst = Graph()
    total_weight = 0
    for u, v, w in sorted_edges:
        iu, iv = idx[u], idx[v]
        if uf.union(iu, iv):
            mst.insert_edge(u, v, w)
            total_weight += w
    return mst, total_weight


if __name__ == "__main__":
    edges = [
        ('A','B',4), ('A','C',1), ('A','D',4),
        ('B','E',9), ('B','F',9), ('B','G',7), ('B','C',5),
        ('C','G',9), ('C','D',3),
        ('D','G',10), ('D','J',18),
        ('E','I',6), ('E','H',4), ('E','F',2),
        ('F','H',2), ('F','G',8),
        ('G','H',9), ('G','J',8),
        ('H','I',3), ('H','J',9),
        ('I','J',9)
    ]
    g = Graph()
    for u, v, w in edges:
        g.insert_edge(u, v, w)
    mst, weight = kruskal_mst(g)
    def printGraph(h):
        print("------MST------")
        for x in h.vertices():
            print(x, "->", end=" ")
            for (n,w) in h.neighbours(x):
                print(f"{n} {w}", end="; ")
            print()
        print("----------------")
    printGraph(mst)
    #print("Total weight of MST:", weight)
