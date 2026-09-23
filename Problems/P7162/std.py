def solve(nums):
    """元素互不相同且不为 0。x 与 -x 同时出现计一对。
    用集合判断对面是否存在，只从正数这边数，避免一对算两次。
    """
    s = set(nums)
    ans = 0
    for x in nums:
        if x > 0 and (-x) in s:
            ans += 1
    return ans


def main():
    # 第一行 n，第二行 n 个非 0 且互不相同的整数
    n = int(input())
    nums = list(map(int, input().split()))
    print(solve(nums))


if __name__ == "__main__":
    main()
