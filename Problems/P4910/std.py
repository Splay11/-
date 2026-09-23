import sys


def max_stable_len(n, d, a):
    # 从左到右扫描：相邻差不超过 d 则延伸当前段，否则重置为 1（单点段）
    ans = 1
    cur = 1
    for i in range(1, n):
        if abs(a[i] - a[i - 1]) <= d:
            cur += 1
        else:
            cur = 1
        if cur > ans:
            ans = cur
    return ans


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(newline="\n")
    t = int(input())
    for _ in range(t):
        n_d = input().split()
        n = int(n_d[0])
        d = int(n_d[1])
        a = list(map(int, input().split()))
        print(max_stable_len(n, d, a))


if __name__ == "__main__":
    main()
