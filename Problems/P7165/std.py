def solve(cards):
    """四个数做 24 点：每次取出两个数做加减乘除，把结果放回去继续。
    除法是实数除法；除数接近 0 时跳过。最后只剩一个数且与 24 足够接近就算成功。
    枚举有序对，减法和除法的两种方向都会走到。
    """
    eps = 1e-6

    def dfs(a):
        if len(a) == 1:
            return abs(a[0] - 24.0) < eps
        n = len(a)
        for i in range(n):
            for j in range(n):
                if i == j:
                    continue
                rest = []
                for k in range(n):
                    if k != i and k != j:
                        rest.append(a[k])
                x = a[i]
                y = a[j]
                cands = [x + y, x - y, x * y]
                if abs(y) > eps:
                    cands.append(x / y)
                for v in cands:
                    if dfs(rest + [v]):
                        return True
        return False

    return dfs([float(x) for x in cards])


def main():
    # 一行四个 1..9 的整数
    cards = list(map(int, input().split()))
    print("true" if solve(cards) else "false")


if __name__ == "__main__":
    main()
