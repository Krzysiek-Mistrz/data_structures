import time

BASE = 256
MOD = 2**61 - 1

def compute_hash(s, length):
    h = 0
    for i in range(length):
        h = (h * BASE + ord(s[i])) % MOD
    high_pow = pow(BASE, length-1, MOD)
    return h, high_pow

def rabin_karp_multi(text, patterns):
    if not patterns:
        return {}, 0
    m = len(patterns[0])
    n = len(text)
    pat_hashes = {}
    for pat in patterns:
        h, _ = compute_hash(pat, m)
        pat_hashes.setdefault(h, []).append(pat)

    t_hash, high_pow = compute_hash(text, m)
    results = {pat: [] for pat in patterns}
    false_positives = 0

    if t_hash in pat_hashes:
        substr = text[0:m]
        for pat in pat_hashes[t_hash]:
            if substr == pat:
                results[pat].append(0)
            else:
                false_positives += 1

    for i in range(1, n - m + 1):
        leading = ord(text[i-1])
        trailing = ord(text[i+m-1])
        t_hash = (t_hash - leading * high_pow) % MOD
        t_hash = (t_hash * BASE + trailing) % MOD
        if t_hash in pat_hashes:
            substr = text[i:i+m]
            for pat in pat_hashes[t_hash]:
                if substr == pat:
                    results[pat].append(i)
                else:
                    false_positives += 1

    return results, false_positives

def main():
    import sys
    with open('lotr.txt', 'r', encoding='utf-8') as f:
        text = f.read()
    patterns = ['gandalf', 'looking', 'blocked', 'comment', 'pouring', 'finally',
                'hundred', 'hobbits', 'however', 'popular', 'nothing', 'enjoyed',
                'stuffed', 'relaxed', 'himself', 'present', 'deliver', 'welcome',
                'baggins', 'further']

    m = len(patterns[0])
    assert all(len(p) == m for p in patterns), "All patterns must same length"

    test = input("Enter test number (1 or 2): ")
    if test.strip() == '1':
        single = patterns[0]
        start = time.perf_counter()
        for pat in patterns:
            rabin_karp_multi(text, [pat])
        t_multi = time.perf_counter() - start

        start = time.perf_counter()
        rabin_karp_multi(text, patterns)
        t_batch = time.perf_counter() - start

        print(f"{t_multi:.6f} s")
        print(f"{t_batch:.6f} s")

    elif test.strip() == '2':
        results, false_pos = rabin_karp_multi(text, patterns)
        total_correct = 0
        for pat in patterns:
            count = len(results[pat])
            total_correct += count
            print(f"{pat} {count}")
        print(f"{total_correct}")
        print(f"{false_pos}")
    else:
        print("Invalid test number")

if __name__ == '__main__':
    main()
