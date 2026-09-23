# 三串字典序最小 LCS：后缀 DP 求长度，再贪心按字母构造

def main():
    a = input().strip()
    b = input().strip()
    c = input().strip()
    n, m, p = len(a), len(b), len(c)

    # f[i][j][k] = a[i:], b[j:], c[k:] 的 LCS 长度
    f = [[[0] * (p + 1) for _ in range(m + 1)] for _ in range(n + 1)]
    for i in range(n, -1, -1):
        for j in range(m, -1, -1):
            for k in range(p, -1, -1):
                if i == n or j == m or k == p:
                    f[i][j][k] = 0
                elif a[i] == b[j] == c[k]:
                    f[i][j][k] = 1 + f[i + 1][j + 1][k + 1]
                else:
                    f[i][j][k] = max(f[i + 1][j][k], f[i][j + 1][k], f[i][j][k + 1])

    L = f[0][0][0]
    print(L)

    # 从前往后贪心选最小字母，保证剩余仍能凑满 LCS
    i = j = k = 0
    remain = L
    res = []
    while remain > 0:
        for ch in "abcdefghijklmnopqrstuvwxyz":
            ni = a.find(ch, i)
            nj = b.find(ch, j)
            nk = c.find(ch, k)
            if ni < 0 or nj < 0 or nk < 0:
                continue
            # 选中该字符后，后缀 LCS 长度应恰好为 remain-1
            if f[ni + 1][nj + 1][nk + 1] == remain - 1:
                res.append(ch)
                i, j, k = ni + 1, nj + 1, nk + 1
                remain -= 1
                break
    print("".join(res))


if __name__ == "__main__":
    main()
