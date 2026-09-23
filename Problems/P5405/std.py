# 标准 DP：dp[j][k] 表示当前占用体积为 j、是否已触发优惠 k 时的最大货值


def max_value(n, W, T, v, w):
    # 不可达状态记为 -1；0 是合法的「一件都不装」
    NEG = -1
    dp = [[NEG, NEG] for _ in range(W + 1)]
    dp[0][0] = 0
    for i in range(n):
        # 先复制上一轮，对应不装第 i 件
        new_dp = [row[:] for row in dp]
        for vol in range(W + 1):
            for trig in (0, 1):
                if dp[vol][trig] < 0:
                    continue
                # 装第 i 件：未触发用原体积，已触发用折半
                cost = v[i] // 2 if trig else v[i]
                nvol = vol + cost
                if nvol > W:
                    continue
                # 装上后体积首次达到 T，之后才算触发
                ntrig = 1 if (trig or nvol >= T) else 0
                val = dp[vol][trig] + w[i]
                if val > new_dp[nvol][ntrig]:
                    new_dp[nvol][ntrig] = val
        dp = new_dp
    # 所有可达状态里取最大货值
    ans = 0
    for vol in range(W + 1):
        for trig in (0, 1):
            if dp[vol][trig] > ans:
                ans = dp[vol][trig]
    return ans


def main():
    # 第一行：货物件数、载重上限、优惠阈值
    n, W, T = map(int, input().split())
    v = []
    w = []
    for _ in range(n):
        vi, wi = map(int, input().split())
        v.append(vi)
        w.append(wi)
    print(max_value(n, W, T, v, w))


if __name__ == "__main__":
    main()
