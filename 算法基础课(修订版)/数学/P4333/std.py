import sys
from collections import Counter

def C2(c: int) -> int:
    return c * (c - 1) // 2 if c >= 2 else 0

def C3(c: int) -> int:
    return c * (c - 1) * (c - 2) // 6 if c >= 3 else 0

def main():
    data = sys.stdin.read().strip().split()
    if not data:
        return
    it = iter(data)
    n = int(next(it))
    arr = [int(next(it)) for _ in range(n)]
    cnt = Counter(arr)

    S2 = 0
    S3 = 0
    self_sum = 0
    for c in cnt.values():
        c2 = C2(c)
        c3 = C3(c)
        S2 += c2
        S3 += c3
        self_sum += c2 * c3

    ans = S3 * S2 - self_sum
    print(ans)

if __name__ == "__main__":
    main()
