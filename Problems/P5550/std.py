import numpy as np


class Solution:
    def crossAttention(self, Xq, Xkv, Wq, Wk, Wv):
        """交叉注意力：Q 来自 Xq，K/V 来自 Xkv；scale=sqrt(d)；无输出投影。"""
        Xq = np.asarray(Xq, dtype=np.float64)
        Xkv = np.asarray(Xkv, dtype=np.float64)
        Wq = np.asarray(Wq, dtype=np.float64)
        Wk = np.asarray(Wk, dtype=np.float64)
        Wv = np.asarray(Wv, dtype=np.float64)
        Q = Xq @ Wq
        K = Xkv @ Wk
        V = Xkv @ Wv
        d = Q.shape[1]
        scores = Q @ K.T / np.sqrt(d)
        scores = scores - scores.max(axis=-1, keepdims=True)
        weights = np.exp(scores)
        weights = weights / weights.sum(axis=-1, keepdims=True)
        return weights @ V


if __name__ == "__main__":
    import sys
    data = sys.stdin.read().strip().split()
    it = iter(data)
    Lq = int(next(it)); Lkv = int(next(it)); d = int(next(it))
    Xq = [[float(next(it)) for _ in range(d)] for _ in range(Lq)]
    Xkv = [[float(next(it)) for _ in range(d)] for _ in range(Lkv)]
    Wq = [[float(next(it)) for _ in range(d)] for _ in range(d)]
    Wk = [[float(next(it)) for _ in range(d)] for _ in range(d)]
    Wv = [[float(next(it)) for _ in range(d)] for _ in range(d)]
    out = Solution().crossAttention(Xq, Xkv, Wq, Wk, Wv)
    lines = [" ".join(f"{float(x):.4f}" for x in row) for row in out]
    sys.stdout.write("\n".join(lines) + "\n")
