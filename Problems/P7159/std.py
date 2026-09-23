def solve(nums, target):
    """正数数组，用滑动窗口找总和 >= target 的最短连续段。
    右端点扩张累加，一旦窗口和够了就尽量收缩左端点，并更新最短长度。
    整段都不够 target 时返回 0。
    """
    n = len(nums)
    left = 0
    s = 0
    ans = n + 1
    for right in range(n):
        s += nums[right]
        # 窗口和已经达标，左端能缩就缩，得到更短的合法段
        while s >= target:
            length = right - left + 1
            if length < ans:
                ans = length
            s -= nums[left]
            left += 1
    # 从未出现合法窗口
    if ans == n + 1:
        return 0
    return ans


def main():
    # 第一行 n、target，第二行 n 个正整数
    n, target = map(int, input().split())
    nums = list(map(int, input().split()))
    print(solve(nums, target))


if __name__ == "__main__":
    main()
