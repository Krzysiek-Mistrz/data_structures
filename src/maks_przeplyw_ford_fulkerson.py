from collections import deque

class Edge:
    def __init__(self, capacity, is_residual=False):
        self.capacity = capacity
        self.is_residual = is_residual
        self.flow = 0
        self.residual_capacity = capacity if not is_residual else 0
    def __repr__(self):
        return f"Cap: {self.capacity}, Flow: {self.flow}, Residual: {self.residual_capacity}, ResidualEdge: {self.is_residual}"

class Graph:
    def __init__(self):
        self.adj = {}  #vertex -> list(neighbor, edge)
    def add_vertex(self, v):
        if v not in self.adj:
            self.adj[v] = []
    def add_edge(self, u, v, capacity):
        real = Edge(capacity, is_residual=False)
        resid = Edge(0, is_residual=True)
        real.residual = resid
        resid.residual = real
        self.add_vertex(u)
        self.add_vertex(v)
        self.adj[u].append((v, real))
        self.adj[v].append((u, resid))
    def get_edge(self, u, v):
        for nbr, edge in self.adj.get(u, []):
            if nbr == v:
                return edge
        return None
    def vertices(self):
        return list(self.adj.keys())
    def neighbors(self, u):
        return self.adj.get(u, [])
    def bfs(self, source, sink):
        queue = deque([source])
        parent = {source: None}
        while queue:
            u = queue.popleft()
            for v, edge in self.neighbors(u):
                if v not in parent and edge.residual_capacity > 0:
                    parent[v] = (u, edge)
                    if v == sink:
                        return parent
                    queue.append(v)
        return parent
    def max_flow(self, source, sink):
        flow = 0
        while True:
            parent = self.bfs(source, sink)
            if sink not in parent:
                break
            bottleneck = float('inf')
            v = sink
            path = []
            while v != source:
                u, edge = parent[v]
                bottleneck = min(bottleneck, edge.residual_capacity)
                path.append((u, v, edge))
                v = u
            for u, v, edge in path:
                edge.flow += bottleneck
                edge.residual_capacity -= bottleneck
                edge.residual.residual_capacity += bottleneck
            flow += bottleneck
        return flow

def print_graph(g):
    print("------GRAPH------")
    for u in g.vertices():
        print(f"{u} -> ", end="")
        for v, e in g.neighbors(u):
            print(f"({v}, {e}) ", end="")
        print()
    print("-----------------")

if __name__ == '__main__':
    tests = [
        [('s','u',2), ('u','t',1), ('u','v',3), ('s','v',1), ('v','t',2)],
        [('s','a',16), ('s','c',13), ('c','a',4), ('a','b',12), ('b','c',9), ('b','t',20), ('c','d',14), ('d','b',7), ('d','t',4)],
        [('s','a',3), ('s','c',3), ('a','b',4), ('b','s',3), ('b','c',1), ('b','d',2), ('c','e',6), ('c','d',2), ('d','t',1), ('e','t',9)]
    ]
    for edges in tests:
        g = Graph()
        for u, v, c in edges:
            g.add_edge(u, v, c)
        print_graph(g)
        result = g.max_flow('s', 't')
        print(f"{result}")