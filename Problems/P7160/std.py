def solve(nums):
    """用集合记下已经出现过的数。
    扫到某个数已经在集合里，说明至少出现两次，存在重复。
    全部扫完都没撞上，则互不相同。
    """
    seen = set()
    for x in nums:
        if x in seen:
            return True
        seen.add(x)
    return False


def main():
    # 第一行 n，第二行 n 个整数
    n = int(input())
    nums = list(map(int, input().split()))
    # 题面要求输出小写 true / false
    print("true" if solve(nums) else "false")


if __name__ == "__main__":
    main()
