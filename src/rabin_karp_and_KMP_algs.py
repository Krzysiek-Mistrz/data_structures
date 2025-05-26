import time

def naive_search(text, pattern):
    n = len(text)
    m = len(pattern)
    count = 0
    comparisons = 0
    t_start = time.perf_counter()
    i = 0
    while i <= n - m:
        match = True
        for j in range(m):
            comparisons += 1
            if text[i + j] != pattern[j]:
                match = False
                break
        if match:
            count += 1
        i += 1
    t_stop = time.perf_counter()
    return count, comparisons, t_stop - t_start

def rabin_karp_basic(text, pattern, d=256, q=101):
    n = len(text)
    m = len(pattern)
    count = 0
    comparisons = 0
    collisions = 0
    def compute_hash(s):
        h = 0
        for ch in s:
            h = (h * d + ord(ch)) % q
        return h
    hW = compute_hash(pattern)
    t_start = time.perf_counter()
    for i in range(n - m + 1):
        hS = compute_hash(text[i:i + m])
        comparisons += 1
        if hS == hW:
            if text[i:i + m] == pattern:
                count += 1
            else:
                collisions += 1
    t_stop = time.perf_counter()
    return count, comparisons, collisions, t_stop - t_start

def rabin_karp_rolling(text, pattern, d=256, q=101):
    n = len(text)
    m = len(pattern)
    count = 0
    comparisons = 0
    collisions = 0
    h = 1
    for _ in range(m - 1):
        h = (h * d) % q
    hW = 0
    hS = 0
    for i in range(m):
        hW = (hW * d + ord(pattern[i])) % q
        hS = (hS * d + ord(text[i])) % q
    t_start = time.perf_counter()
    for i in range(n - m + 1):
        comparisons += 1
        if hS == hW:
            if text[i:i + m] == pattern:
                count += 1
            else:
                collisions += 1
        if i < n - m:
            hS = (d * (hS - ord(text[i]) * h) + ord(text[i + m])) % q
            if hS < 0:
                hS += q
    t_stop = time.perf_counter()
    return count, comparisons, collisions, t_stop - t_start

def kmp_table(pattern):
    m = len(pattern)
    T = [-1] + [0] * m
    pos = 1
    cnd = 0
    while pos < m:
        if pattern[pos] == pattern[cnd]:
            T[pos] = T[cnd]
        else:
            T[pos] = cnd
            cnd = T[cnd]
            while cnd >= 0 and pattern[pos] != pattern[cnd]:
                cnd = T[cnd]
        pos += 1
        cnd += 1
    T[pos] = cnd
    return T

def kmp_search(text, pattern):
    n = len(text)
    m = len(pattern)
    T = kmp_table(pattern)
    comparisons = 0
    count = 0
    t_start = time.perf_counter()
    i = 0
    j = 0
    while i < n:
        comparisons += 1
        if pattern[j] == text[i]:
            i += 1
            j += 1
            if j == m:
                count += 1
                j = T[j]
        else:
            j = T[j]
            if j < 0:
                i += 1
                j += 1
    t_stop = time.perf_counter()
    return count, comparisons, T, t_stop - t_start

if __name__ == '__main__':
    with open('lotr.txt', encoding='utf-8') as f:
        text = ' '.join(f.readlines()).lower()
    pattern = 'time.'

    naive_count, naive_comp, naive_time = naive_search(text, pattern)
    print(f"{naive_count};{naive_comp};{naive_time:.7f}")

    rk_count, rk_comp, rk_coll, rk_time = rabin_karp_basic(text, pattern)
    print(f"{rk_count};{rk_comp};{rk_coll};{rk_time:.7f}")

    rkr_count, rkr_comp, rkr_coll, rkr_time = rabin_karp_rolling(text, pattern)
    print(f"{rkr_count};{rkr_comp};{rkr_coll};{rkr_time:.7f}")

    kmp_count, kmp_comp, kmp_T, kmp_time = kmp_search(text, pattern)
    print(f"{kmp_count};{kmp_comp};{kmp_T}")