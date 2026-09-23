def is_empty(arr):
    # 题面约定：空队列用一行 0 表示，直接输出 0
    return (not arr) or arr == [0]


def min_cost(arr, t, lim):
    # 在连续放掉不超过 lim 的前提下，刚好接 t 项的最小耗时；做不到返回 -1
    n = len(arr)
    if n == 0:
        return 0
    if t == 0:
        # 一项都不接，整段都算放掉，长度必须 <= lim
        return 0 if n <= lim else -1
    if t > n:
        return -1
    # t+1 个空隙（队首、相邻接单之间、队尾）各最多放掉 lim 项
    if n - t > (t + 1) * lim:
        return -1

    inf = 10**18
    # dp[i]：当前已经接了若干项、且最后一项是下标 i 的最小耗时
    dp = [inf] * n
    for i in range(n):
        if i <= lim:
            dp[i] = arr[i]

    # 再接第 2..t 项：相邻两次接单的下标差最多 lim+1（中间放掉 <= lim）
    for _ in range(2, t + 1):
        ndp = [inf] * n
        dq = []  # 单调队列，存上一层下标，队头是窗口最小值
        head = 0
        for i in range(n):
            prev = i - 1
            if prev >= 0 and dp[prev] < inf:
                while head < len(dq) and dp[dq[-1]] >= dp[prev]:
                    dq.pop()
                dq.append(prev)
            lo = i - lim - 1
            while head < len(dq) and dq[head] < lo:
                head += 1
            if head < len(dq):
                ndp[i] = dp[dq[head]] + arr[i]
        dp = ndp

    ans = inf
    for i in range(n):
        # 队尾放掉的项数也不能超过 lim
        if n - 1 - i <= lim and dp[i] < ans:
            ans = dp[i]
    return -1 if ans >= inf else ans


def main():
    arr = list(map(int, input().split()))
    if is_empty(arr):
        print(0)
        return
    t = int(input())
    lim = int(input())
    print(min_cost(arr, t, lim))


if __name__ == "__main__":
    main()
