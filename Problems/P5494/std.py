def can_divide(nums, divisor, threshold):
    # 除数越大，向上取整之和越小；超过阈值就可以提前结束
    total = 0
    for x in nums:
        total += (x + divisor - 1) // divisor
        if total > threshold:
            return False
    return True


def smallest_divisor(nums, threshold):
    # 答案具有单调性，在 [1, max(nums)] 上二分最小可行除数
    left = 1
    right = nums[0]
    for x in nums:
        if x > right:
            right = x
    while left < right:
        mid = (left + right) // 2
        if can_divide(nums, mid, threshold):
            right = mid
        else:
            left = mid + 1
    return left


def main():
    # 第一行 n 与阈值，第二行 n 个数
    parts = list(map(int, input().split()))
    n = parts[0]
    threshold = parts[1]
    nums = list(map(int, input().split()))
    print(smallest_divisor(nums[:n], threshold))


if __name__ == "__main__":
    main()
