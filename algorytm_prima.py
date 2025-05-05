class Graph:
    def __init__(self):
        self.adj = {}
    def insert_vertex(self, v):
        if v not in self.adj:
            self.adj[v] = []
    def insert_edge(self, u, v, w):
        if u not in self.adj:
            self.insert_vertex(u)
        if v not in self.adj:
            self.insert_vertex(v)
        self.adj[u].append((v, w))
    def vertices(self):
        return list(self.adj.keys())
    def neighbours(self, v):
        return list(self.adj.get(v, []))

def printGraph(g):
    print("------GRAPH------")
    for v in g.vertices():
        print(v, end=" -> ")
        for (n, w) in g.neighbours(v):
            print(f"{n} {w}", end=";")
        print()
    print("-------------------")

def prim_mst(graph, start):
    intree   = {v: False for v in graph.vertices()}
    distance = {v: float('inf') for v in graph.vertices()}
    parent   = {v: None for v in graph.vertices()}
    mst = Graph()
    for v in graph.vertices():
        mst.insert_vertex(v)
    distance[start] = 0
    total_weight   = 0
    while True:
        v = None
        min_dist = float('inf')
        for u in graph.vertices():
            if not intree[u] and distance[u] < min_dist:
                min_dist = distance[u]
                v = u
        if v is None:
            break
        intree[v] = True
        if parent[v] is not None:
            u = parent[v]
            w = distance[v]
            mst.insert_edge(u, v, w)
            mst.insert_edge(v, u, w)
            total_weight += w
        for (w, weight) in graph.neighbours(v):
            if not intree[w] and weight < distance[w]:
                distance[w] = weight
                parent[w]   = v
    return mst, total_weight

if __name__ == "__main__":
    graf = [
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
    for u, v, w in graf:
        g.insert_edge(u, v, w)
        g.insert_edge(v, u, w)
    start_vertex = 'A'
    mst, weight = prim_mst(g, start_vertex)
    printGraph(mst)
    #print(f"Total weight of MST: {weight}")
