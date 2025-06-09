import math
import time

def tri_cost(p, q, r):
    return math.dist(p, q) + math.dist(q, r) + math.dist(r, p)

def min_cost_rec(points):
    n = len(points)
    memo = [[None] * n for _ in range(n)]
    def rec(i, j):
        if j < i + 2:
            return 0.0
        if memo[i][j] is not None:
            return memo[i][j]
        best = float('inf')
        for k in range(i + 1, j):
            cost = (tri_cost(points[i], points[k], points[j]) +
                    rec(i, k) + rec(k, j))
            best = min(best, cost)
        memo[i][j] = best
        return best
    return rec(0, n - 1)

def min_cost_iter(points):
    n = len(points)
    dp = [[0.0] * n for _ in range(n)]
    for length in range(2, n):
        for i in range(n - length):
            j = i + length
            best = float('inf')
            for k in range(i + 1, j):
                cost = (tri_cost(points[i], points[k], points[j]) +
                        dp[i][k] + dp[k][j])
                best = min(best, cost)
            dp[i][j] = best
    return dp[0][n - 1]

tests = [
    ([[0, 0], [1, 0], [2, 1], [1, 2], [0, 2]], 15.3006),
    ([[0, 0], [4, 0], [5, 4], [4, 5], [2, 5], [1, 4], [0, 3], [0, 2]], 54.4086)
]

results = []
for pts, expected in tests:
    pts_tuples = [tuple(pt) for pt in pts]
    
    start = time.perf_counter()
    cost_rec = min_cost_rec(pts_tuples)
    time_rec = time.perf_counter() - start
    
    start = time.perf_counter()
    cost_it = min_cost_iter(pts_tuples)
    time_it = time.perf_counter() - start
    
    print(cost_rec, time_rec)
    print(cost_it, time_it, end='\n\n')