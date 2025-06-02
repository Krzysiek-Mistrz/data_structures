import numpy as np

def edit_distance_recursive(P, T, i, j):
    if i == 0:
        return j
    if j == 0:
        return i
    if P[i-1] == T[j-1]:
        return edit_distance_recursive(P, T, i-1, j-1)
    insert_cost = 1 + edit_distance_recursive(P, T, i, j-1)
    delete_cost = 1 + edit_distance_recursive(P, T, i-1, j)
    replace_cost = 1 + edit_distance_recursive(P, T, i-1, j-1)
    return min(insert_cost, delete_cost, replace_cost)

P_a = ' kot'
T_a = ' pies'
cost_a = edit_distance_recursive(P_a, T_a, len(P_a), len(T_a))
print(cost_a)

def edit_distance_dp(P, T):
    m, n = len(P), len(T)
    D = np.zeros((m+1, n+1), dtype=int)
    parent = np.full((m+1, n+1), 'X', dtype='<U1')
    for i in range(1, m+1):
        D[i][0] = i
        parent[i][0] = 'D'
    for j in range(1, n+1):
        D[0][j] = j
        parent[0][j] = 'I'
    for i in range(1, m+1):
        for j in range(1, n+1):
            if P[i-1] == T[j-1]:
                cost_diag = D[i-1][j-1]
            else:
                cost_diag = D[i-1][j-1] + 1
            cost_del = D[i-1][j] + 1
            cost_ins = D[i][j-1] + 1
            min_cost = min(cost_diag, cost_del, cost_ins)
            D[i][j] = min_cost
            if min_cost == cost_diag:
                parent[i][j] = 'M' if P[i-1] == T[j-1] else 'S'
            elif min_cost == cost_del:
                parent[i][j] = 'D'
            else:
                parent[i][j] = 'I'
    return D, parent

P_b = ' biały autobus'
T_b = ' czarny autokar'
D_b, parent_b = edit_distance_dp(P_b, T_b)
cost_b = D_b[len(P_b)][len(T_b)]
print(cost_b)

def reconstruct_path(P, T, parent):
    i, j = len(P), len(T)
    ops = []
    while i > 0 or j > 0:
        op = parent[i][j]
        ops.append(op)
        if op in ['M', 'S']:
            i -= 1
            j -= 1
        elif op == 'D':
            i -= 1
        elif op == 'I':
            j -= 1
        else:
            break
    ops = list(reversed(ops))
    if ops and ops[0] == 'M' and len(P) > 0 and len(T) > 0 and P[0] == T[0]:
        ops = ops[1:]
    return ''.join(ops)

P_c = ' thou shalt not'
T_c = ' you should not'
_, parent_c = edit_distance_dp(P_c, T_c)
path_c = reconstruct_path(P_c, T_c, parent_c)
print(path_c)

def approximate_substring_search(P, T):
    m, n = len(P), len(T)
    D = np.zeros((m+1, n+1), dtype=int)
    parent = np.full((m+1, n+1), 'X', dtype='<U1')
    for i in range(1, m+1):
        D[i][0] = i
        parent[i][0] = 'D'
    for i in range(1, m+1):
        for j in range(1, n+1):
            if P[i-1] == T[j-1]:
                cost_diag = D[i-1][j-1]
            else:
                cost_diag = D[i-1][j-1] + 1
            cost_del = D[i-1][j] + 1
            cost_ins = D[i][j-1] + 1
            min_cost = min(cost_diag, cost_del, cost_ins)
            D[i][j] = min_cost
            if min_cost == cost_diag:
                parent[i][j] = 'M' if P[i-1] == T[j-1] else 'S'
            elif min_cost == cost_del:
                parent[i][j] = 'D'
            else:
                parent[i][j] = 'I'
    min_j = np.argmin(D[m])
    start_index = min_j - m
    return D, parent, start_index

P_d1 = ' ban'
T_d = ' mokeyssbanana'
_, parent_d1, start_index_d1 = approximate_substring_search(P_d1, T_d)
print(start_index_d1)

P_d2 = ' bin'
_, parent_d2, start_index_d2 = approximate_substring_search(P_d2, T_d)
print(start_index_d2)

def longest_common_subsequence(P, T):
    m, n = len(P), len(T)
    D = np.zeros((m+1, n+1), dtype=int)
    parent = np.full((m+1, n+1), 'X', dtype='<U1')
    BIG = max(m, n) + 1
    for i in range(1, m+1):
        D[i][0] = i
        parent[i][0] = 'D'
    for j in range(1, n+1):
        D[0][j] = j
        parent[0][j] = 'I'
    for i in range(1, m+1):
        for j in range(1, n+1):
            if P[i-1] == T[j-1]:
                cost_diag = D[i-1][j-1]
            else:
                cost_diag = D[i-1][j-1] + BIG
            cost_del = D[i-1][j] + 1
            cost_ins = D[i][j-1] + 1
            min_cost = min(cost_diag, cost_del, cost_ins)
            D[i][j] = min_cost
            if min_cost == cost_diag:
                parent[i][j] = 'M' if P[i-1] == T[j-1] else 'S'
            elif min_cost == cost_del:
                parent[i][j] = 'D'
            else:
                parent[i][j] = 'I'
    i, j = m, n
    lcs_chars = []
    while i > 0 and j > 0:
        op = parent[i][j]
        if op == 'M':
            lcs_chars.append(P[i-1])
            i -= 1
            j -= 1
        elif op == 'S':
            i -= 1
            j -= 1
        elif op == 'D':
            i -= 1
        else:
            j -= 1
    return ''.join(reversed(lcs_chars))

P_e = ' democrat'
T_e = ' republican'
lcs_e = longest_common_subsequence(P_e, T_e)
print(lcs_e)

T_f = ' 243517698'
P_f = ''.join([' '] + sorted(T_f.strip()))
lcs_f = longest_common_subsequence(P_f, T_f)
print(lcs_f)
