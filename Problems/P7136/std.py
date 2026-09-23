def solve(nums, target):
    """在严格升序数组里二分查找 target，找到返回下标，否则 -1。
    每次把查找区间减半，复杂度 O(log n)。
    """
    left = 0
    right = len(nums) - 1
    while left <= right:
        # 取中点，写成 left+(right-left)//2 避免溢出写法的习惯（Python 无溢出）
        mid = left + (right - left) // 2
        if nums[mid] == target:
            return mid
        if nums[mid] < target:
            # 中点比目标小，答案只可能在右半段
            left = mid + 1
        else:
            # 中点比目标大，答案只可能在左半段
            right = mid - 1
    return -1


def main():
    # 第一行：数组长度 n、要找的 target
    n, target = map(int, input().split())
    nums = list(map(int, input().split()))
    print(solve(nums, target))


if __name__ == "__main__":
    main()
