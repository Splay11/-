# -*- coding: utf-8 -*-
from typing import List
import numpy as np


class Solution:
    def ppoClippedLoss(self, advantages: List[float], logprobs: List[float],
                       old_logprobs: List[float], epsilon: float) -> float:
        """PPO 裁剪代理损失：min(rho*A, clip(rho)*A) 再取负平均。"""
        A = np.asarray(advantages, dtype=np.float64)
        pi = np.asarray(logprobs, dtype=np.float64)
        pi_old = np.asarray(old_logprobs, dtype=np.float64)
        # 重要性采样比
        rho = np.exp(pi - pi_old)
        clipped = np.clip(rho, 1.0 - epsilon, 1.0 + epsilon)
        # 对裁剪前后取较保守者（逐元素 min）
        surr = np.minimum(rho * A, clipped * A)
        return -float(surr.mean())


if __name__ == "__main__":
    import sys
    data = sys.stdin.read().strip().split()
    it = iter(data)
    n = int(next(it)); eps = float(next(it))
    adv, lp, olp = [], [], []
    for _ in range(n):
        adv.append(float(next(it)))
        lp.append(float(next(it)))
        olp.append(float(next(it)))
    print(f"{Solution().ppoClippedLoss(adv, lp, olp, eps):.4f}")
