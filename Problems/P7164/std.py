def solve(nums, k):
    """每个值的出现次数必须能被 k 整除，才能恰好分成每组 k 个相同元素。
    n 能被 k 整除只是必要条件，不够充分。
    """
    cnt = {}
    for x in nums:
        cnt[x] = cnt.get(x, 0) + 1
    for v in cnt.values():
        if v % k != 0:
            return False
    return True


def main():
    # 第一行 n、k，第二行 n 个整数
    n, k = map(int, input().split())
    nums = list(map(int, input().split()))
    print("true" if solve(nums, k) else "false")


if __name__ == "__main__":
    main()
