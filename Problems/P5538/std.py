# -*- coding: utf-8 -*-
from typing import List


class Solution:
    def sgdLinearRegression(
        self,
        X: List[List[float]],
        y: List[float],
        eta: float,
        T: int,
    ) -> List[List[float]]:
        """SGD 训练线性回归，返回 [w, [b]]。"""
        n = len(X)
        d = len(X[0]) if n else 0
        # 参数全部初始化为 0
        w = [0.0] * d
        b = 0.0
        for _ in range(T):
            for i in range(n):
                # 单样本预测与误差
                yhat = b
                for j in range(d):
                    yhat += w[j] * X[i][j]
                err = yhat - y[i]
                # 梯度：dw=2*err*x，db=2*err，立刻更新
                for j in range(d):
                    w[j] -= eta * 2.0 * err * X[i][j]
                b -= eta * 2.0 * err
        return [w, [b]]


if __name__ == "__main__":
    import sys

    data = sys.stdin.read().strip().split()
    it = iter(data)
    n = int(next(it))
    d = int(next(it))
    eta = float(next(it))
    T = int(float(next(it)))
    X, y = [], []
    for _ in range(n):
        row = [float(next(it)) for _ in range(d)]
        yi = float(next(it))
        X.append(row)
        y.append(yi)
    w, bb = Solution().sgdLinearRegression(X, y, eta, T)
    print(" ".join(f"{v:.4f}" for v in w))
    print(f"{bb[0]:.4f}")
