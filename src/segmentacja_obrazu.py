import cv2
import numpy as np

I = cv2.imread('sample.png', cv2.IMREAD_GRAYSCALE)
YY, XX = I.shape

edges = []
for j in range(YY):
    for i in range(XX):
        u = j*XX + i
        for dj in (-1,0,1):
          for di in (-1,0,1):
            if dj==0 and di==0: continue
            y, x = j+dj, i+di
            if 0<=y<YY and 0<=x<XX:
                v = y*XX + x
                w = abs(int(I[j,i]) - int(I[y,x]))
                edges.append((u, v, w))

def prim_mst(num_vertices, edges):
    G = [[] for _ in range(num_vertices)]
    for u,v,w in edges:
        G[u].append((v,w))
    intree = [False]*num_vertices
    dist   = [float('inf')]*num_vertices
    parent = [-1]*num_vertices
    dist[0]=0
    mst_edges=[]
    for _ in range(num_vertices):
        v = min((d,u) for u,d in enumerate(dist) if not intree[u])[1]
        intree[v]=True
        if parent[v]>=0:
            mst_edges.append((parent[v], v, dist[v]))
        for (w,wt) in G[v]:
            if not intree[w] and wt<dist[w]:
                dist[w]=wt; parent[w]=v
    return mst_edges

mst = prim_mst(YY*XX, edges)
u_max, v_max, w_max = max(mst, key=lambda x:x[2])
M = [[] for _ in range(YY*XX)]
for u,v,w in mst:
    if (u,v,w)!=(u_max,v_max,w_max):
        M[u].append(v); M[v].append(u)

def dfs_label(start, lab, M, out):
    stack, visited = [start], {start}
    while stack:
        u=stack.pop()
        y,x = divmod(u, XX)
        out[y,x]=lab
        for w in M[u]:
            if w not in visited:
                visited.add(w); stack.append(w)
    return visited

S = np.zeros_like(I, dtype=np.uint8)
dfs_label(u_max, 100, M, S)
dfs_label(v_max, 200, M, S)
cv2.imshow("Segmented MST", S)
cv2.waitKey(0)
cv2.destroyAllWindows()
