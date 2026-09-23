# -*- coding: utf-8 -*-
from typing import List


class Solution:
    def gradientDescentSqrt(self, a: float, x0: float, eta: float, T: int) -> List[List[float]]:
        """梯度下降求平方根，返回每次迭代后的 [x, L]。"""
        x = x0
        out = []
        for _ in range(T):
            # 梯度 4x(x^2 - a)，按题面更新
            grad = 4.0 * x * (x * x - a)
            x = x - eta * grad
            # 可取绝对值保证非负（题面提示）
            if x < 0:
                x = -x
            loss = (x * x - a) * (x * x - a)
            out.append([x, loss])
        return out


if __name__ == "__main__":
    import sys

    data = sys.stdin.read().strip().split()
    it = iter(data)
    a = float(next(it))
    x0 = float(next(it))
    eta = float(next(it))
    T = int(next(it))
    rows = Solution().gradientDescentSqrt(a, x0, eta, T)
    for x, L in rows:
        print(f"{x:.4f} {L:.4f}")
