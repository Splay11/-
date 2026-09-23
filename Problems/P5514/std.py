# -*- coding: utf-8 -*-
"""P5514 不相邻子集最小和"""

INF = 10**30


def min_non_adjacent_sum(a):
    n = len(a)
    # f：选中当前位置；g：不选当前位置（且前面已至少选过一个）
    f = a[0]
    g = INF
    for i in range(1, n):
        # 不选 a[i]：沿用前一位置的最优非空方案
        ng = min(f, g)
        # 选 a[i]：前面要么为空，要么是「不选 a[i-1]」的非空方案
        nf = a[i] + (0 if g >= INF // 2 else min(0, g))
        f, g = nf, ng
    return min(f, g)


def main():
    n = int(input())
    a = list(map(int, input().split()))
    print(min_non_adjacent_sum(a))


if __name__ == "__main__":
    main()
