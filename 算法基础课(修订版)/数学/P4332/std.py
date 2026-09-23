# 读取输入，枚举质数，用打家劫舍DP计算最优答案
import sys

def primes_upto(m):
    # 简单埃氏筛
    is_p = [True] * (m + 1)
    is_p[0] = is_p[1] = False
    for i in range(2, int(m**0.5) + 1):
        if is_p[i]:
            for j in range(i*i, m+1, i):
                is_p[j] = False
    return [i for i in range(2, m+1) if is_p[i]]

def solve():
    data = sys.stdin.read().strip().split()
    n = int(data[0])
    a = list(map(int, data[1:1+n]))
    ps = primes_upto(100)

    ans = 0
    for p in ps:
        pre2, pre1 = 0, 0  # dp[i-2], dp[i-1]
        for x in a:
            b = 1 if x % p == 0 else 0
            cur = pre1 if pre1 >= pre2 + b else pre2 + b
            pre2, pre1 = pre1, cur
        if pre1 > ans:
            ans = pre1

    print(ans)

if __name__ == "__main__":
    solve()
