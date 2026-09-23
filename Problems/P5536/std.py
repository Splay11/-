# -*- coding: utf-8 -*-
from typing import List
import math


class Solution:
    def averageKLDivergence(self, P: List[List[float]], Q: List[List[float]]) -> float:
        """计算 m 组 KL(P||Q) 的平均值。"""
        m = len(P)
        total = 0.0
        for i in range(m):
            # 对每个类别累加 P_j * ln(P_j / Q_j)
            kl = 0.0
            for pj, qj in zip(P[i], Q[i]):
                kl += pj * math.log(pj / qj)
            total += kl
        return total / m


if __name__ == "__main__":
    import sys

    data = sys.stdin.read().strip().split()
    it = iter(data)
    m = int(next(it))
    n = int(next(it))
    P = [[float(next(it)) for _ in range(n)] for _ in range(m)]
    Q = [[float(next(it)) for _ in range(n)] for _ in range(m)]
    ans = Solution().averageKLDivergence(P, Q)
    print(f"{ans:.6f}")
