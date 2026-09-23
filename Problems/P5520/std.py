# 枚举分割点；用前缀和/平方和 O(1) 算左右方差之和

def main():
    n = int(input())
    a = list(map(int, input().split()))
    # 前缀和、平方和
    ps = [0.0] * (n + 1)
    qs = [0.0] * (n + 1)
    for i in range(n):
        ps[i + 1] = ps[i] + a[i]
        qs[i + 1] = qs[i] + float(a[i]) * a[i]

    best = -1.0
    for k in range(1, n):
        n1 = float(k)
        n2 = float(n - k)
        # Var = E[x^2] - (E[x])^2
        v1 = qs[k] / n1 - (ps[k] / n1) ** 2
        v2 = (qs[n] - qs[k]) / n2 - ((ps[n] - ps[k]) / n2) ** 2
        s = v1 + v2
        if s > best:
            best = s
    print("%.6f" % best)


if __name__ == "__main__":
    main()
