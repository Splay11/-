import sys


def solve(a):
    n = len(a)
    ans = 0
    # |a_i|<=100 且 sum=L^2 ⇒ L<=100，枚举左端点后最多看 100 长度
    for l in range(n):
        s = 0
        lim = n if n < l + 100 else l + 100
        for r in range(l, lim):
            s += a[r]
            L = r - l + 1
            if s == L * L:
                ans += 1
    return ans


def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    it = iter(data)
    T = next(it)
    out = []
    for _ in range(T):
        n = next(it)
        a = [next(it) for _ in range(n)]
        out.append(str(solve(a)))
    sys.stdout.write("\n".join(out) + "\n")


if __name__ == "__main__":
    main()
