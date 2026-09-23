import numpy as np


class Solution:
    def polynomialRegression(self, xs, ys, degree):
        """最小二乘多项式回归，返回从高次到常数项的系数。"""
        xs = np.asarray(xs, dtype=float)
        ys = np.asarray(ys, dtype=float)
        # 设计矩阵第 i 行为 [x^n, x^{n-1}, ..., 1]
        A = np.vander(xs, degree + 1, increasing=False)
        # 求解 min ||Ac - y||^2
        coef, _, _, _ = np.linalg.lstsq(A, ys, rcond=None)
        return coef.tolist()


if __name__ == "__main__":
    N = int(input())
    xs = []
    ys = []
    for _ in range(N):
        x, y = map(float, input().split())
        xs.append(x)
        ys.append(y)
    degree = int(input())
    coef = Solution().polynomialRegression(xs, ys, degree)

    def fmt(c):
        # 先按 4 位小数格式化；若末两位为 0 则收成 2 位，对齐题面样例 2.49 -0.25
        s = f"{c:.4f}"
        if s.endswith("00"):
            return s[:-2]
        return s

    print(" ".join(fmt(c) for c in coef))
