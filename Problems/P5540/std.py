# -*- coding: utf-8 -*-
from typing import List
import numpy as np


class Solution:
    def twoLayerFCForwardBackward(
        self,
        x: List[float],
        W1: List[List[float]],
        b1: List[float],
        W2: List[List[float]],
        b2: List[float],
        y: List[float],
    ) -> List:
        """
        两层全连接：前向 + 反向（只返回梯度，不更新参数）。
        结构：x -> W1,b1 -> ReLU -> W2,b2 -> yhat
        损失 L = mean((yhat - y)^2)
        返回 [yhat, L, dW1, db1, dW2, db2]
        """
        x = np.asarray(x, dtype=np.float64).reshape(1, -1)
        W1 = np.asarray(W1, dtype=np.float64)
        b1 = np.asarray(b1, dtype=np.float64)
        W2 = np.asarray(W2, dtype=np.float64)
        b2 = np.asarray(b2, dtype=np.float64)
        y = np.asarray(y, dtype=np.float64)
        d_out = y.shape[0]
        # 前向
        z1 = x @ W1 + b1
        a1 = np.maximum(z1, 0.0)
        yhat = (a1 @ W2 + b2).ravel()
        loss = float(np.mean((yhat - y) ** 2))
        # 反向：dL/dyhat = 2/d_out * (yhat - y)
        dy = (2.0 / d_out) * (yhat - y)
        dW2 = np.outer(a1.ravel(), dy)
        db2 = dy.copy()
        da1 = dy @ W2.T
        dz1 = da1 * (z1.ravel() > 0)
        dW1 = np.outer(x.ravel(), dz1)
        db1 = dz1.copy()
        return [
            yhat.tolist(),
            loss,
            dW1.tolist(),
            db1.tolist(),
            dW2.tolist(),
            db2.tolist(),
        ]


if __name__ == "__main__":
    import sys

    data = sys.stdin.read().strip().split()
    it = iter(data)
    d_in = int(next(it))
    d_h = int(next(it))
    d_out = int(next(it))
    x = [float(next(it)) for _ in range(d_in)]
    W1 = [[float(next(it)) for _ in range(d_h)] for _ in range(d_in)]
    b1 = [float(next(it)) for _ in range(d_h)]
    W2 = [[float(next(it)) for _ in range(d_out)] for _ in range(d_h)]
    b2 = [float(next(it)) for _ in range(d_out)]
    y = [float(next(it)) for _ in range(d_out)]
    yhat, loss, dW1, db1, dW2, db2 = Solution().twoLayerFCForwardBackward(
        x, W1, b1, W2, b2, y
    )
    print(" ".join(f"{v:.4f}" for v in yhat))
    print(f"{loss:.4f}")
    for row in dW1:
        print(" ".join(f"{v:.4f}" for v in row))
    print(" ".join(f"{v:.4f}" for v in db1))
    for row in dW2:
        print(" ".join(f"{v:.4f}" for v in row))
    print(" ".join(f"{v:.4f}" for v in db2))
