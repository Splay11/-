def solve(p, k):
    n = len(p)
    p = p[:]
    # 每次交换消去一个逆序；逆序数不超过 n*(n-1)/2
    limit = n * (n - 1) // 2
    if k >= limit:
        return sorted(p)
    for _ in range(k):
        swapped = False
        for i in range(n - 1):
            if p[i] > p[i + 1]:
                p[i], p[i + 1] = p[i + 1], p[i]
                swapped = True
                break
        if not swapped:
            break
    return p


if __name__ == "__main__":
    T = int(input())
    for _ in range(T):
        n, k = map(int, input().split())
        p = list(map(int, input().split()))
        print(*solve(p, k))
