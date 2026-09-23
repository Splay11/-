# -*- coding: utf-8 -*-
from typing import List
import numpy as np


class Solution:
    def trainTwoLayerMLP(
        self,
        X: List[List[float]],
        y: List[float],
        W1: List[List[float]],
        W2: List[List[float]],
        eta: float,
    ) -> List:
        """
        两层 MLP 单步：无偏置、无激活。
        返回 [yhat(list), loss, W1_new, W2_new(flat list)]
        """
        X = np.asarray(X, dtype=np.float64)
        y = np.asarray(y, dtype=np.float64).reshape(-1, 1)
        W1 = np.asarray(W1, dtype=np.float64)
        W2 = np.asarray(W2, dtype=np.float64).reshape(-1, 1)
        n = X.shape[0]
        # 前向：h = X W1，yhat = h W2
        h = X @ W1
        yhat = h @ W2
        # MSE
        loss = float(np.mean((yhat - y) ** 2))
        # dL/dyhat = 2/n * (yhat - y)
        dy = (2.0 / n) * (yhat - y)
        dW2 = h.T @ dy
        dh = dy @ W2.T
        dW1 = X.T @ dh
        # SGD 更新
        W1n = W1 - eta * dW1
        W2n = W2 - eta * dW2
        return [
            yhat.ravel().tolist(),
            loss,
            W1n.tolist(),
            W2n.ravel().tolist(),
        ]


if __name__ == "__main__":
    import sys

    data = sys.stdin.read().strip().split()
    it = iter(data)
    n = int(next(it))
    d_in = int(next(it))
    d_h = int(next(it))
    eta = float(next(it))
    y = [float(next(it)) for _ in range(n)]
    X = [[float(next(it)) for _ in range(d_in)] for _ in range(n)]
    W1 = [[float(next(it)) for _ in range(d_h)] for _ in range(d_in)]
    W2 = [[float(next(it))] for _ in range(d_h)]
    yhat, loss, W1n, W2n = Solution().trainTwoLayerMLP(X, y, W1, W2, eta)
    print(" ".join(f"{v:.4f}" for v in yhat))
    print(f"{loss:.4f}")
    for row in W1n:
        print(" ".join(f"{v:.4f}" for v in row))
    for v in W2n:
        print(f"{v:.4f}")
