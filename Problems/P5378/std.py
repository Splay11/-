MOD = 1000000007
MAXN = 200000

# f[i][k]：长度为 i、末尾恰好连续 k 个相同字母的方案数（k = 1,2,3）
f1 = [0] * (MAXN + 1)
f2 = [0] * (MAXN + 1)
f3 = [0] * (MAXN + 1)
ans = [0] * (MAXN + 1)

# 长度为 1：26 种字母，末尾连续段长度只能是 1
f1[1] = 26
ans[1] = 26

for i in range(2, MAXN + 1):
    # 换一个与末尾不同的字母，连续段变成 1，有 25 种选择
    f1[i] = (f1[i - 1] + f2[i - 1] + f3[i - 1]) * 25 % MOD
    # 再重复一次末尾字母：只能接在「恰好 1 个」后面
    f2[i] = f1[i - 1]
    # 再重复一次：只能接在「恰好 2 个」后面（不能接到 3 个上，否则连续 4 个）
    f3[i] = f2[i - 1]
    ans[i] = (f1[i] + f2[i] + f3[i]) % MOD


def count_str(m):
    return ans[m]


def main():
    q = int(input())
    for _ in range(q):
        m = int(input())
        print(count_str(m))


if __name__ == "__main__":
    main()
