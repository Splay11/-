import numpy as np


class Solution:
    def multiHeadAttention(self, X, Wq, Wk, Wv, Wo, h):
        """无 bias 的 Multi-Head Attention：投影、分头、缩放点积、拼接、Wo。"""
        X = np.asarray(X, dtype=np.float64)
        Wq = np.asarray(Wq, dtype=np.float64)
        Wk = np.asarray(Wk, dtype=np.float64)
        Wv = np.asarray(Wv, dtype=np.float64)
        Wo = np.asarray(Wo, dtype=np.float64)
        Q, K, V = X @ Wq, X @ Wk, X @ Wv
        L, d = X.shape
        dk = d // h
        # (L,d) -> (h,L,dk)
        Qh = Q.reshape(L, h, dk).transpose(1, 0, 2)
        Kh = K.reshape(L, h, dk).transpose(1, 0, 2)
        Vh = V.reshape(L, h, dk).transpose(1, 0, 2)
        heads = []
        for i in range(h):
            scores = Qh[i] @ Kh[i].T / np.sqrt(dk)
            # 数值稳定 softmax
            scores = scores - scores.max(axis=-1, keepdims=True)
            weights = np.exp(scores)
            weights = weights / weights.sum(axis=-1, keepdims=True)
            heads.append(weights @ Vh[i])
        concat = np.concatenate(heads, axis=-1)
        return concat @ Wo


if __name__ == "__main__":
    import sys
    data = sys.stdin.read().strip().split()
    it = iter(data)
    L = int(next(it)); d = int(next(it)); h = int(next(it))
    X = [[float(next(it)) for _ in range(d)] for _ in range(L)]
    Wq = [[float(next(it)) for _ in range(d)] for _ in range(d)]
    Wk = [[float(next(it)) for _ in range(d)] for _ in range(d)]
    Wv = [[float(next(it)) for _ in range(d)] for _ in range(d)]
    Wo = [[float(next(it)) for _ in range(d)] for _ in range(d)]
    out = Solution().multiHeadAttention(X, Wq, Wk, Wv, Wo, h)
    lines = [" ".join(f"{float(x):.4f}" for x in row) for row in out]
    sys.stdout.write("\n".join(lines) + "\n")
