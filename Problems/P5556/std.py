# -*- coding: utf-8 -*-
from typing import List
import numpy as np


class Solution:
    def loraForward(
        self,
        X: List[List[float]],
        W: List[List[float]],
        A: List[List[float]],
        B: List[List[float]],
        alpha: float,
    ) -> List[List[float]]:
        """LoRA 前向：y = xW + alpha * xAB。"""
        X = np.asarray(X, dtype=np.float64)
        W = np.asarray(W, dtype=np.float64)
        A = np.asarray(A, dtype=np.float64)
        B = np.asarray(B, dtype=np.float64)
        # 主路径 + 低秩增量
        Y = X @ W + alpha * (X @ A @ B)
        return Y.tolist()


if __name__ == "__main__":
    import sys

    def read_mat(it, rows, cols):
        return [[float(next(it)) for _ in range(cols)] for _ in range(rows)]

    data = sys.stdin.read().strip().split()
    it = iter(data)
    n = int(next(it)); d_in = int(next(it)); d_out = int(next(it)); r = int(next(it))
    alpha = float(next(it))
    X = read_mat(it, n, d_in)
    W = read_mat(it, d_in, d_out)
    A = read_mat(it, d_in, r)
    B = read_mat(it, r, d_out)
    out = Solution().loraForward(X, W, A, B, alpha)
    for row in out:
        print(" ".join(f"{x:.4f}" for x in row))
