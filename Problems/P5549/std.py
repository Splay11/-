import numpy as np


class Solution:
    def groupedQueryAttention(self, X, Wq, Wk, Wv, Wo, hq, hkv):
        """GQA：hq 个 Q 头分组共享 hkv 个 KV 头，无 bias，最后乘 Wo。"""
        X = np.asarray(X, dtype=np.float64)
        Wq = np.asarray(Wq, dtype=np.float64)
        Wk = np.asarray(Wk, dtype=np.float64)
        Wv = np.asarray(Wv, dtype=np.float64)
        Wo = np.asarray(Wo, dtype=np.float64)
        L, d = X.shape
        dk = d // hq
        Q = X @ Wq
        K = X @ Wk
        V = X @ Wv
        Qh = Q.reshape(L, hq, dk).transpose(1, 0, 2)
        Kh = K.reshape(L, hkv, dk).transpose(1, 0, 2)
        Vh = V.reshape(L, hkv, dk).transpose(1, 0, 2)
        g = hq // hkv
        heads = []
        for i in range(hq):
            kv = i // g  # 每 g 个 Q 头共享一个 KV 头
            scores = Qh[i] @ Kh[kv].T / np.sqrt(dk)
            scores = scores - scores.max(axis=-1, keepdims=True)
            weights = np.exp(scores)
            weights = weights / weights.sum(axis=-1, keepdims=True)
            heads.append(weights @ Vh[kv])
        return np.concatenate(heads, axis=-1) @ Wo


if __name__ == "__main__":
    import sys
    data = sys.stdin.read().strip().split()
    it = iter(data)
    L = int(next(it)); d = int(next(it)); hq = int(next(it)); hkv = int(next(it))
    dkv = d * hkv // hq
    X = [[float(next(it)) for _ in range(d)] for _ in range(L)]
    Wq = [[float(next(it)) for _ in range(d)] for _ in range(d)]
    Wk = [[float(next(it)) for _ in range(dkv)] for _ in range(d)]
    Wv = [[float(next(it)) for _ in range(dkv)] for _ in range(d)]
    Wo = [[float(next(it)) for _ in range(d)] for _ in range(d)]
    out = Solution().groupedQueryAttention(X, Wq, Wk, Wv, Wo, hq, hkv)
    lines = [" ".join(f"{float(x):.4f}" for x in row) for row in out]
    sys.stdout.write("\n".join(lines) + "\n")
