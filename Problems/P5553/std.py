# -*- coding: utf-8 -*-
from typing import List
import numpy as np


class Solution:
    def sftCrossEntropy(self, tokens: List[int], logits: List[List[float]]) -> float:
        """SFT 交叉熵：shift-right + padding mask（token==-1 不计入）。"""
        tokens = np.asarray(tokens, dtype=np.int64)
        logits = np.asarray(logits, dtype=np.float64)
        # 第 i 个位置预测第 i+1 个 token
        lg = logits[:-1]
        lb = tokens[1:]
        mask = lb != -1
        if not np.any(mask):
            return 0.0
        lg = lg[mask]
        lb = lb[mask]
        # 数值稳定 log-softmax 后取 label 位置
        m = lg.max(axis=1, keepdims=True)
        logp = lg - m - np.log(np.exp(lg - m).sum(axis=1, keepdims=True))
        loss = -float(logp[np.arange(len(lb)), lb].mean())
        return loss


if __name__ == "__main__":
    import sys
    data = sys.stdin.read().strip().split()
    it = iter(data)
    L = int(next(it)); V = int(next(it))
    tokens = [int(next(it)) for _ in range(L)]
    logits = [[float(next(it)) for _ in range(V)] for _ in range(L)]
    print(f"{Solution().sftCrossEntropy(tokens, logits):.4f}")
