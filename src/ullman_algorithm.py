import copy

def build_adj_matrix(vertices, edges):
    n = len(vertices)
    idx = {v: i for i, v in enumerate(vertices)}
    M = [[0] * n for _ in range(n)]
    for u, v, w in edges:
        i, j = idx[u], idx[v]
        M[i][j] = w
        M[j][i] = w
    return M

def vertex_degrees(adj):
    return [sum(row) for row in adj]

def prune(P_adj, G_adj, M):
    changed = True
    while changed:
        changed = False
        m = len(M)
        n = len(M[0])
        for i in range(m):
            for j in range(n):
                if M[i][j] == 1:
                    P_nei = [x for x, val in enumerate(P_adj[i]) if val]
                    G_nei = [y for y, val in enumerate(G_adj[j]) if val]
                    for x in P_nei:
                        if not any(M[x][y] == 1 for y in G_nei):
                            M[i][j] = 0
                            changed = True
                            break
    return M

def ullman_base(P_adj, G_adj):
    m, n = len(P_adj), len(G_adj)
    M = [[0]*n for _ in range(m)]
    used = [False]*n
    iso_count = 0
    calls = 0
    def rec(depth, M):
        nonlocal iso_count, calls
        calls += 1
        if depth == m:
            MG = [[sum(M[i][k] * G_adj[k][j] for k in range(n)) for j in range(n)] for i in range(m)]
            MGT = [[sum(MG[i][k] * M[j][k] for k in range(n)) for j in range(m)] for i in range(m)]
            if MGT == P_adj:
                iso_count += 1
            return
        for j in range(n):
            if not used[j]:
                used[j] = True
                M2 = copy.deepcopy(M)
                for c in range(n): M2[depth][c] = 0
                M2[depth][j] = 1
                rec(depth+1, M2)
                used[j] = False
    rec(0, M)
    return iso_count, calls

def ullman_M0(P_adj, G_adj):
    m, n = len(P_adj), len(G_adj)
    degP = vertex_degrees(P_adj)
    degG = vertex_degrees(G_adj)
    M0 = [[1 if degP[i] <= degG[j] else 0 for j in range(n)] for i in range(m)]
    used = [False]*n
    iso_count = 0
    calls = 0
    def rec(depth, M):
        nonlocal iso_count, calls
        calls += 1
        if depth == m:
            MG = [[sum(M[i][k] * G_adj[k][j] for k in range(n)) for j in range(n)] for i in range(m)]
            MGT = [[sum(MG[i][k] * M[j][k] for k in range(n)) for j in range(m)] for i in range(m)]
            if MGT == P_adj:
                iso_count += 1
            return
        for j in range(n):
            if not used[j] and M[depth][j] == 1:
                used[j] = True
                M2 = copy.deepcopy(M)
                for c in range(n): M2[depth][c] = 0
                M2[depth][j] = 1
                rec(depth+1, M2)
                used[j] = False
    rec(0, M0)
    return iso_count, calls

def ullman_prune(P_adj, G_adj):
    m, n = len(P_adj), len(G_adj)
    degP = vertex_degrees(P_adj)
    degG = vertex_degrees(G_adj)
    M0 = [[1 if degP[i] <= degG[j] else 0 for j in range(n)] for i in range(m)]
    used = [False]*n
    iso_count = 0
    calls = 0
    def rec(depth, M):
        nonlocal iso_count, calls
        calls += 1
        M = prune(P_adj, G_adj, M)
        if depth == m:
            MG = [[sum(M[i][k] * G_adj[k][j] for k in range(n)) for j in range(n)] for i in range(m)]
            MGT = [[sum(MG[i][k] * M[j][k] for k in range(n)) for j in range(m)] for i in range(m)]
            if MGT == P_adj:
                iso_count += 1
            return
        for j in range(n):
            if not used[j] and M[depth][j] == 1:
                used[j] = True
                M2 = copy.deepcopy(M)
                for c in range(n): M2[depth][c] = 0
                M2[depth][j] = 1
                rec(depth+1, M2)
                used[j] = False
    rec(0, M0)
    return iso_count, calls

if __name__ == "__main__":
    G_vertices = ['A', 'B', 'C', 'D', 'E', 'F']
    P_vertices = ['A', 'B', 'C']
    graph_G = [('A','B',1), ('B','F',1), ('B','C',1), ('C','D',1), ('C','E',1), ('D','E',1)]
    graph_P = [('A','B',1), ('B','C',1), ('A','C',1)]
    G_adj = build_adj_matrix(G_vertices, graph_G)
    P_adj = build_adj_matrix(P_vertices, graph_P)
    iso1, calls1 = ullman_base(P_adj, G_adj)
    iso2, calls2 = ullman_M0(P_adj, G_adj)
    iso3, calls3 = ullman_prune(P_adj, G_adj)
    print(f"{iso1} {calls1}")
    print(f"{iso2} {calls2}")
    print(f"{iso3} {calls3}")
