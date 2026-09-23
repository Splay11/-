# -*- coding: utf-8 -*-
from typing import List
import math


class Solution:
    def stableSigmoid(self, x: List[float]) -> List[List[float]]:
        """数值稳定 Sigmoid 及其导数，返回 [sigmoid, derivative]。"""
        sig, der = [], []
        for v in x:
            # x<0 时用 e^x/(1+e^x)，避免 exp(-x) 溢出
            if v < 0:
                e = math.exp(v)
                s = e / (1.0 + e)
            else:
                s = 1.0 / (1.0 + math.exp(-v))
            sig.append(s)
            # 导数 sigma * (1 - sigma)
            der.append(s * (1.0 - s))
        return [sig, der]


if __name__ == "__main__":
    import sys

    data = sys.stdin.read().strip().split()
    it = iter(data)
    n = int(next(it))
    xs = [float(next(it)) for _ in range(n)]
    sig, der = Solution().stableSigmoid(xs)
    print(" ".join(f"{v:.2f}" for v in sig))
    print(" ".join(f"{v:.2f}" for v in der))
