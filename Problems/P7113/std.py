# 区间 DP：每次只能删当前区间的左端或右端


def min_cost(a):
    n = len(a)
    # dp[i][j]：把下标 i..j 这一段全部删完的最小代价
    dp = [[0] * n for _ in range(n)]
    # 长度为 1：当前长度是 1，代价就是元素本身
    for i in range(n):
        dp[i][i] = a[i]
    # 按区间长度从小到大填表，保证转移时子区间已经算好
    for length in range(2, n + 1):
        for i in range(0, n - length + 1):
            j = i + length - 1
            # 先删左端 a[i]，代价为当前长度 * a[i]，再加上删完剩余区间的最优代价
            left = length * a[i] + dp[i + 1][j]
            # 先删右端 a[j]，同理
            right = length * a[j] + dp[i][j - 1]
            dp[i][j] = left if left < right else right
    return dp[0][n - 1]


def main():
    n = int(input())
    a = list(map(int, input().split()))
    print(min_cost(a))


if __name__ == "__main__":
    main()
