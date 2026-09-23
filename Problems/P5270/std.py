def solve(a):
    n = len(a)
    s = sum(a)
    # 偶数长度时，回文要求总和为偶数
    if n % 2 == 0 and s % 2 == 1:
        return -1
    diff = 0
    for i in range(n // 2):
        diff += abs(a[i] - a[n - 1 - i])
    # 最少搬运次数 = ceil(配对差之和 / 2)
    return (diff + 1) // 2


if __name__ == "__main__":
    T = int(input())
    for _ in range(T):
        n = int(input())
        a = list(map(int, input().split()))
        print(solve(a))
