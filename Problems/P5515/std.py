# -*- coding: utf-8 -*-
"""P5515 打靶凑总分的方案数"""


def count_ways(S):
    # dp[s]：用若干次射击得到总分 s 的方案数
    dp = [0] * (S + 1)
    dp[0] = 1
    for _ in range(10):
        ndp = [0] * (S + 1)
        for s in range(S + 1):
            if dp[s] == 0:
                continue
            # 本枪得 0..10 分
            for v in range(11):
                if s + v <= S:
                    ndp[s + v] += dp[s]
        dp = ndp
    return dp[S]


def main():
    S = int(input())
    print(count_ways(S))


if __name__ == "__main__":
    main()
