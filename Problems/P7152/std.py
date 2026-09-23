def solve(nums, k):
    """值域只有 -10000 到 10000，用计数排序从大到小数第 k 个。
    重复值各自占一个名次，不是去重后的第 k 个不同数。
    """
    offset = 10000
    cnt = [0] * (2 * offset + 1)
    for x in nums:
        cnt[x + offset] += 1
    need = k
    # 从大到小扫，减掉该值出现次数，减到 <=0 就是第 k 大
    v = offset
    while v >= -offset:
        need -= cnt[v + offset]
        if need <= 0:
            return v
        v -= 1
    return 0


def main():
    # 第一行 n、k，第二行 n 个整数
    n, k = map(int, input().split())
    nums = list(map(int, input().split()))
    print(solve(nums, k))


if __name__ == "__main__":
    main()
