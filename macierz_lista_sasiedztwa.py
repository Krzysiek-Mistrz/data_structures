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


graph = NeighbourList()
vertices = {}
for woj in polska.slownik.keys():
    v = Vertex(woj)
    vertices[woj] = v
    graph.insert_vertex(v)
for v1, v2 in polska.graf:
    graph.insert_edge(vertices[v1], vertices[v2], None)
graph.delete_vertex(vertices['K'])
graph.delete_edge(vertices['W'], vertices['E'])
polska.draw_map(graph)

graph = NeighbourMatrix()
vertices = {}
for woj in polska.slownik.keys():
    v = Vertex(woj)
    vertices[woj] = v
    graph.insert_vertex(v)
for v1, v2 in polska.graf:
    graph.insert_edge(vertices[v1], vertices[v2], None)
graph.delete_vertex(vertices['K'])
graph.delete_edge(vertices['W'], vertices['E'])
polska.draw_map(graph)