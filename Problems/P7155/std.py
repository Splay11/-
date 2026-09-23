def solve(nums, target):
    """排列型完全背包：dp[t] 表示凑出 t 的有序方案数。
    外层枚举容量、内层枚举数字，这样 1,2 和 2,1 会从不同转移加进来。
    每个数字可以重复使用。
    """
    # 凑出 0 视为一种空方案；凑不出的容量会一直保持 0
    dp = [0] * (target + 1)
    dp[0] = 1
    for t in range(1, target + 1):
        for x in nums:
            if t >= x:
                dp[t] += dp[t - x]
    return dp[target]


def main():
    # 第一行 n、target，第二行 n 个互不相同的正整数
    n, target = map(int, input().split())
    nums = list(map(int, input().split()))
    print(solve(nums, target))


if __name__ == "__main__":
    main()
