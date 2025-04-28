import polska

class Vertex:
    def __init__(self, key):
        self.key = key
    def __hash__(self):
        return hash(self.key)
    def __eq__(self, other):
        return self.key == other.key
    def __repr__(self):
        return str(self.key)

class NeighbourMatrix:
    def __init__(self, init_value=0):
        self.matrix = []
        self.vertices_list = []
        self.init_value = init_value
    def is_empty(self):
        return len(self.vertices_list) == 0

    def insert_vertex(self, vertex):
        self.vertices_list.append(vertex)
        size = len(self.vertices_list)
        for row in self.matrix:
            row.append(self.init_value)
        self.matrix.append([self.init_value] * size)
    def insert_edge(self, vertex1, vertex2, edge=1):
        idx1 = self.vertices_list.index(vertex1)
        idx2 = self.vertices_list.index(vertex2)
        self.matrix[idx1][idx2] = edge
    def delete_vertex(self, vertex):
        idx = self.vertices_list.index(vertex)
        self.vertices_list.pop(idx)
        self.matrix.pop(idx)
        for row in self.matrix:
            row.pop(idx)
    def delete_edge(self, vertex1, vertex2):
        idx1 = self.vertices_list.index(vertex1)
        idx2 = self.vertices_list.index(vertex2)
        self.matrix[idx1][idx2] = self.init_value
    def neighbours(self, vertex_id):
        idx = vertex_id
        for i, edge in enumerate(self.matrix[idx]):
            if edge != self.init_value:
                yield (i, edge)
    def vertices(self):
        return range(len(self.vertices_list))
    def get_vertex(self, vertex_id):
        return self.vertices_list[vertex_id]

class NeighbourList:
    def __init__(self):
        self.nodes = {}
    def is_empty(self):
        return len(self.nodes) == 0
    def insert_vertex(self, vertex):
        self.nodes[vertex] = {}
    def insert_edge(self, vertex1, vertex2, edge=None):
        self.nodes[vertex1][vertex2] = edge
    def delete_vertex(self, vertex):
        del self.nodes[vertex]
        for neighbours in self.nodes.values():
            if vertex in neighbours:
                del neighbours[vertex]
    def delete_edge(self, vertex1, vertex2):
        if vertex2 in self.nodes[vertex1]:
            del self.nodes[vertex1][vertex2]
    def neighbours(self, vertex_id):
        for neighbour, edge in self.nodes[vertex_id].items():
            yield (neighbour, edge)
    def vertices(self):
        return self.nodes.keys()
    def get_vertex(self, vertex_id):
        return vertex_id


def greedy_coloring(graph, method='BFS'):
    colors = {}
    visited = set()

    def assign_color(u):
        used = set()
        for v, _ in graph.neighbours(u):
            if v in colors:
                used.add(colors[v])
        color = 0
        while color in used:
            color += 1
        colors[u] = color

    for start in graph.vertices():
        if start in visited:
            continue
        if method == 'BFS':
            frontier = [start]
            pop_index = 0
        else:
            frontier = [start]
            pop_index = -1
        visited.add(start)
        while frontier:
            u = frontier.pop(pop_index)
            assign_color(u)
            for v, _ in graph.neighbours(u):
                if v not in visited:
                    visited.add(v)
                    frontier.append(v)
    return colors

if __name__ == '__main__':
    graph_list = NeighbourList()
    verts = {k: Vertex(k) for k in polska.slownik.keys()}
    for v in verts.values():
        graph_list.insert_vertex(v)
    for v1, v2 in polska.graf:
        graph_list.insert_edge(verts[v1], verts[v2])
    graph_list.delete_vertex(verts['K'])
    graph_list.delete_edge(verts['W'], verts['E'])
    colors_bfs = greedy_coloring(graph_list, method='BFS')
    colors_dfs = greedy_coloring(graph_list, method='DFS')
    col_bfs = [
        ( str(graph_list.get_vertex(v_id)), colors_bfs[v_id] )
        for v_id in graph_list.vertices()
    ]
    col_dfs = [
        ( str(graph_list.get_vertex(v_id)), colors_dfs[v_id] )
        for v_id in graph_list.vertices()
    ]
    print("Max colors BFS:", max(colors_bfs.values())+1)
    print("Max colors DFS:", max(colors_dfs.values())+1)
    polska.draw_map(graph_list, col_dfs)
    polska.draw_map(graph_list, col_bfs)
    