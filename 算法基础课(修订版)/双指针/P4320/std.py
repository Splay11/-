# -*- coding: utf-8 -*-
import sys

def count_factor(x: int, p: int) -> int:
    """计算 x 中质因子 p 的个数"""
    c = 0
    while x % p == 0:
        x //= p
        c += 1
    return c

def solve(a, k):
    n = len(a)
    c2 = [0]*n
    c5 = [0]*n
    # 只分解 2 和 5
    for i, v in enumerate(a):
        c2[i] = count_factor(v, 2)
        c5[i] = count_factor(v, 5)

    ans = 0
    l = 0
    r = 0
    cur2 = 0
    cur5 = 0
    # 滑动窗口 [l, r)
    while l < n:
        while r < n and (cur2 < k or cur5 < k):
            cur2 += c2[r]
            cur5 += c5[r]
            r += 1
        if cur2 >= k and cur5 >= k:
            ans += (n - r + 1)
        # 移动左端点
        cur2 -= c2[l]
        cur5 -= c5[l]
        l += 1
    return ans

def main():
    data = sys.stdin.read().strip().split()
    if not data:
        return
    it = iter(data)
    n = int(next(it)); k = int(next(it))
    a = [int(next(it)) for _ in range(n)]
    print(solve(a, k))

if __name__ == "__main__":
    main()
