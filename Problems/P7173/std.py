def solve(nums):
    """全体异或得到两个落单数的异或。
    取异或结果里最低的 1 作为分组依据，两个落单数一定被分到两边。
    各组再异或一次就分别得到这两个数。
    """
    xor_all = 0
    for x in nums:
        xor_all ^= x
    # 取出最低的 1，用来把数组分成两堆
    lowbit = xor_all & -xor_all
    a = 0
    b = 0
    for x in nums:
        if x & lowbit:
            a ^= x
        else:
            b ^= x
    if a > b:
        a, b = b, a
    return a, b


def main():
    # 第一行 n，第二行 n 个数；输出两个落单数，较小的在前便于对拍
    n = int(input())
    nums = list(map(int, input().split()))
    a, b = solve(nums)
    print(a, b)


if __name__ == "__main__":
    main()
