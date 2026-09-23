MOD = 998244353


def count_arrangements(d, v):
    # 按高度排序后，从矮到高：每个人只能和「不比自己高超过 d」的更矮后缀里的人相邻下落
    # 嵌套后继集合上哈密顿路条数，等于每个位置可选人数的乘积
    a = sorted(v)
    n = len(a)
    ans = 1
    j = 0
    for i in range(n):
        # j 右移到第一个高度大于 a[i]+d 的位置
        while j < n and a[j] - a[i] <= d:
            j += 1
        # 后缀 a[i..] 里高度仍不超过 a[i]+d 的人数
        ans = ans * (j - i) % MOD
    return ans


def main():
    m, d = map(int, input().split())
    v = list(map(int, input().split()))
    print(count_arrangements(d, v))


if __name__ == "__main__":
    main()
