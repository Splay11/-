def solve(a):
    n = len(a)
    if n == 1:
        return 0
    a = sorted(a, reverse=True)
    # 全部非正：最大元素单独作为较小 b，答案 max*(n-1)
    if a[0] <= 0:
        return a[0] * (n - 1)
    # 正数赋严格递增的较小 b；非正数共享最大 b，贡献为 0
    ans = 0
    for i, x in enumerate(a):
        if x <= 0:
            break
        ans += x * (n - 1 - i)
    return ans


if __name__ == "__main__":
    T = int(input())
    for _ in range(T):
        n = int(input())
        a = list(map(int, input().split()))
        print(solve(a))
