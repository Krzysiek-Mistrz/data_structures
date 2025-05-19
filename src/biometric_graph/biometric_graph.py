import math
from collections import defaultdict


class BiometricGraph:
    def __init__(self):
        self.vertices = []
        self.adj = defaultdict(set)

    def add_vertex(self, coord):
        idx = len(self.vertices)
        self.vertices.append(coord)
        return idx

    def add_edge(self, u, v):
        self.adj[u].add(v)
        self.adj[v].add(u)

    def remove_vertex(self, idx):
        for nbr in list(self.adj[idx]):
            self.adj[nbr].remove(idx)
        del self.adj[idx]
        self.vertices[idx] = None

    def transform(self, tx, ty, theta):
        cos_t, sin_t = math.cos(theta), math.sin(theta)
        new_vs = []
        for v in self.vertices:
            x, y = v
            x0, y0 = x + tx, y + ty
            x1 =  x0 * cos_t + y0 * sin_t
            y1 = -x0 * sin_t + y0 * cos_t
            new_vs.append((x1, y1))
        self.vertices = new_vs

    def plot_graph(self, v_color='r', e_color='k'):
        import matplotlib.pyplot as plt
        for i, v in enumerate(self.vertices):
            if v is None: continue
            x, y = v
            plt.scatter(x, y, c=v_color)
            for j in self.adj[i]:
                x2, y2 = self.vertices[j]
                plt.plot([x, x2], [y, y2], color=e_color)


def fill_biometric_graph_from_image(img, graph):
    h, w = img.shape
    idx_map = {}
    directions = [(-1,0),(1,0),(0,-1),(0,1),(-1,-1),(-1,1),(1,-1),(1,1)]
    for y in range(h):
        for x in range(w):
            if img[y,x] == 255:
                idx = graph.add_vertex((x, y))
                idx_map[(y,x)] = idx
    for (y,x), idx in idx_map.items():
        for dy,dx in directions:
            ny, nx = y+dy, x+dx
            if 0 <= ny < h and 0 <= nx < w and img[ny,nx]==255:
                graph.add_edge(idx, idx_map[(ny,nx)])

def unclutter_biometric_graph(graph):
    to_remove = set()
    to_add = set()
    visited = set()
    for v in range(len(graph.vertices)):
        if graph.vertices[v] is None: continue
        deg = len(graph.adj[v])
        if deg != 2 or v in visited:
            continue
        path = [v]
        prev = None
        cur = v
        ends = list(graph.adj[cur])
        u1, u2 = ends
        to_remove.add(cur)
        visited.add(cur)
        to_add.add((u1, u2))
        to_add.add((u2, u1))
    for v in to_remove:
        graph.remove_vertex(v)
    for u, v in to_add:
        if graph.vertices[u] is not None and graph.vertices[v] is not None:
            graph.add_edge(u, v)

def merge_near_vertices(graph, thr=5):
    n = len(graph.vertices)
    groups = []
    assigned = set()
    for i in range(n):
        if graph.vertices[i] is None or i in assigned:
            continue
        xi, yi = graph.vertices[i]
        group = [i]
        assigned.add(i)
        for j in range(i+1, n):
            if graph.vertices[j] is None or j in assigned:
                continue
            xj, yj = graph.vertices[j]
            if math.hypot(xi-xj, yi-yj) < thr:
                group.append(j)
                assigned.add(j)
        if len(group) > 1:
            groups.append(group)
    for group in groups:
        xs = [graph.vertices[i][0] for i in group]
        ys = [graph.vertices[i][1] for i in group]
        new_coord = (sum(xs)/len(xs), sum(ys)/len(ys))
        new_idx = graph.add_vertex(new_coord)
        neighbors = set()
        for i in group:
            for nbr in graph.adj[i]:
                if nbr not in group and graph.vertices[nbr] is not None:
                    neighbors.add(nbr)
        for i in group:
            graph.remove_vertex(i)
        for nbr in neighbors:
            graph.add_edge(new_idx, nbr)

def biometric_graph_registration(g1, g2, Ni=50, eps=10):
    def edge_list(graph):
        edges = []
        for u in range(len(graph.vertices)):
            if graph.vertices[u] is None: continue
            for v in graph.adj[u]:
                if u < v:
                    x1,y1 = graph.vertices[u]
                    x2,y2 = graph.vertices[v]
                    vec = (x2-x1, y2-y1)
                    length = math.hypot(*vec)
                    angle = math.atan2(y2-y1, x2-x1)
                    edges.append((u,v,length,angle))
        return edges
    E1 = edge_list(g1)
    E2 = edge_list(g2)
    sabs = []
    for (u1,v1,l1,a1) in E1:
        for (u2,v2,l2,a2) in E2:
            dlen = abs(l1-l2)
            dang = abs(math.atan2(math.sin(a1-a2), math.cos(a1-a2)))
            sab = math.hypot(dlen, dang)
            sabs.append( (sab, (u1,v1), (u2,v2)) )
    sabs.sort(key=lambda x: x[0])
    best = sabs[:Ni]
    best_score = float('inf')
    best_pair = None
    best_transforms = None
    for sab, (u1,v1), (u2,v2) in best:
        import copy
        G1 = copy.deepcopy(g1)
        G2 = copy.deepcopy(g2)
        x1,y1 = G1.vertices[u1]
        x2,y2 = G2.vertices[u2]
        tx = -x1
        ty = -y1
        G1.transform(tx, ty, 0)
        dx1, dy1 = G1.vertices[v1][0] - 0, G1.vertices[v1][1] - 0
        theta1 = -math.atan2(dy1, dx1)
        G1.transform(0,0,theta1)
        tx2, ty2 = -x2, -y2
        G2.transform(tx2, ty2, 0)
        dx2, dy2 = G2.vertices[v2][0], G2.vertices[v2][1]
        theta2 = -math.atan2(dy2, dx2)
        G2.transform(0,0,theta2)
        matched = set()
        C = 0
        for i, (xi, yi) in enumerate(G1.vertices):
            if yi is None: continue
            for j, (xj, yj) in enumerate(G2.vertices):
                if yj is None: continue
                if i in matched: continue
                if math.hypot(xi-xj, yi-yj) <= eps:
                    matched.add(i)
                    C += 1
                    break
        m, m2 = len([v for v in g1.vertices if v is not None]), len([v for v in g2.vertices if v is not None])
        dk = 1 - C / max(m, m2)
        if dk < best_score:
            best_score = dk
            best_pair = ((u1,v1),(u2,v2))
            best_transforms = (G1, G2)
    return best_transforms if best_transforms else (g1, g2)
