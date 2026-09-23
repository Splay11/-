# -*- coding: utf-8 -*-
from typing import List
import numpy as np


class Solution:
    def infoNCE(self, A: List[List[float]], P: List[List[float]], tau: float) -> float:
        """计算 batch 内 anchor-positive 的 InfoNCE 损失（自然对数）。"""
        A = np.asarray(A, dtype=np.float64)
        P = np.asarray(P, dtype=np.float64)
        n = A.shape[0]
        # L2 归一化后做余弦相似度，再除以温度
        An = A / np.linalg.norm(A, axis=1, keepdims=True)
        Pn = P / np.linalg.norm(P, axis=1, keepdims=True)
        sim = (An @ Pn.T) / tau
        # 数值稳定的 log-softmax：对角为正样本
        row_max = sim.max(axis=1, keepdims=True)
        lse = row_max.ravel() + np.log(np.exp(sim - row_max).sum(axis=1))
        pos = sim[np.arange(n), np.arange(n)]
        loss = -float(np.mean(pos - lse))
        return loss


if __name__ == "__main__":
    import sys
    data = sys.stdin.read().strip().split()
    it = iter(data)
    n = int(next(it)); d = int(next(it)); tau = float(next(it))
    A = [[float(next(it)) for _ in range(d)] for _ in range(n)]
    P = [[float(next(it)) for _ in range(d)] for _ in range(n)]
    ans = Solution().infoNCE(A, P, tau)
    print(f"{ans:.4f}")
