# -*- coding: utf-8 -*-
"""P5517 重复拼接后的最大连续子数组和"""


def kadane(a):
    # 经典最大子段和（至少取一个元素）
    best = cur = a[0]
    for x in a[1:]:
        cur = max(x, cur + x)
        best = max(best, cur)
    return best


def max_subarray_k(a, k):
    one = kadane(a)
    if k == 1:
        return one
    total = sum(a)
    # 最大前缀和
    s = 0
    max_pref = a[0]
    for x in a:
        s += x
        if s > max_pref:
            max_pref = s
    # 最大后缀和
    s = 0
    max_suf = a[-1]
    for x in reversed(a):
        s += x
        if s > max_suf:
            max_suf = s
    # 跨边界：一段后缀接下一段前缀
    ans = max(one, max_suf + max_pref)
    # 总和为正时，中间可再拼 (k-2) 个完整拷贝
    if k > 2 and total > 0:
        ans = max(ans, max_suf + (k - 2) * total + max_pref)
    return ans


def main():
    n, k = map(int, input().split())
    a = list(map(int, input().split()))
    print(max_subarray_k(a, k))


if __name__ == "__main__":
    main()
