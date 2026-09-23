# -*- coding: utf-8 -*-
"""P5513 0-1 背包"""


def knapsack(n, W, items):
    # 经典 0-1 背包：dp[j] 表示容量恰好不超过 j 时的最大价值
    dp = [0] * (W + 1)
    for w, v in items:
        # 倒序更新，保证每个物品只用一次
        for j in range(W, w - 1, -1):
            nv = dp[j - w] + v
            if nv > dp[j]:
                dp[j] = nv
    return dp[W]


def main():
    n, W = map(int, input().split())
    items = []
    for _ in range(n):
        w, v = map(int, input().split())
        items.append((w, v))
    print(knapsack(n, W, items))


if __name__ == "__main__":
    main()
