def min_subarray_len(nums, target):
    """在全是正整数的数组里，找总和 >= target 的最短连续段长度；没有则返回 0。"""
    n = len(nums)
    s = 0
    left = 0
    # 用 n+1 当「还没找到」的哨兵，保证任何合法长度都会把它更新掉
    ans = n + 1
    for right in range(n):
        # 右端点纳入窗口
        s += nums[right]
        # 元素都是正的，窗口和只会随左端点右移而变小，可以一直收缩
        while s >= target:
            length = right - left + 1
            if length < ans:
                ans = length
            s -= nums[left]
            left += 1
    # 从头到尾都凑不够 target，就没有合法子数组
    if ans == n + 1:
        return 0
    return ans


def main():
    # 第一行：数组长度 n 和目标和 target
    n, target = map(int, input().split())
    # 第二行：n 个正整数
    nums = list(map(int, input().split()))
    print(min_subarray_len(nums, target))


if __name__ == "__main__":
    main()
