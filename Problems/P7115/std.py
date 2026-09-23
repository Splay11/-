# 区间 DP：当前行动者从 a[i..j] 能拿到的最大得分


def first_score(a):
    n = len(a)
    # pre[k] 为前 k 个数的和，用来 O(1) 求区间和
    pre = [0] * (n + 1)
    for i in range(n):
        pre[i + 1] = pre[i] + a[i]
    # dp[i][j]：轮到当前玩家时，从下标 i..j 能拿到的最大得分
    dp = [[0] * n for _ in range(n)]
    for i in range(n):
        dp[i][i] = a[i]
    # 按区间长度从小到大填表
    for length in range(2, n + 1):
        for i in range(0, n - length + 1):
            j = i + length - 1
            tot = pre[j + 1] - pre[i]
            # 取左端则对手在剩余区间得 dp[i+1][j]；取右端则对手得 dp[i][j-1]
            # 当前得分 = 区间和 - 对手得分，应让对手拿到的更少
            opp = dp[i + 1][j] if dp[i + 1][j] < dp[i][j - 1] else dp[i][j - 1]
            dp[i][j] = tot - opp
    return dp[0][n - 1]


def main():
    n = int(input())
    a = list(map(int, input().split()))
    print(first_score(a))


if __name__ == "__main__":
    main()
