def can_cut(a, k, length):
    """判断每段长度为 length 时，能不能切出至少 k 段。
    段数可能很大，累加到 >= k 就可以提前停。
    """
    got = 0
    for x in a:
        got += x // length
        if got >= k:
            return True
    return False


def solve(a, k):
    """二分答案：长度越大越难切够 k 段。题目保证长度为 1 一定可行。"""
    left = 1
    right = max(a)
    ans = 1
    while left <= right:
        mid = left + (right - left) // 2
        if can_cut(a, k, mid):
            # mid 可行，试更长的
            ans = mid
            left = mid + 1
        else:
            # mid 太长，切不够，往短了找
            right = mid - 1
    return ans


def main():
    # 第一行：绳子根数 n、至少要切出的段数 k
    n, k = map(int, input().split())
    a = list(map(int, input().split()))
    print(solve(a, k))


if __name__ == "__main__":
    main()
