import numpy as np


class Solution:
    def transformerEncoderBlock(self, X, Wq, Wk, Wv, Wo, W1, b1, W2, b2, h):
        """Post-LN Encoder：MHA -> 残差+LN -> FFN(ReLU) -> 残差+LN；LN 的 gamma=1,beta=0。"""
        X = np.asarray(X, dtype=np.float64)
        Wq = np.asarray(Wq, dtype=np.float64)
        Wk = np.asarray(Wk, dtype=np.float64)
        Wv = np.asarray(Wv, dtype=np.float64)
        Wo = np.asarray(Wo, dtype=np.float64)
        W1 = np.asarray(W1, dtype=np.float64)
        b1 = np.asarray(b1, dtype=np.float64)
        W2 = np.asarray(W2, dtype=np.float64)
        b2 = np.asarray(b2, dtype=np.float64)
        eps = 1e-5

        def mha(X_):
            Q, K, V = X_ @ Wq, X_ @ Wk, X_ @ Wv
            L, d = X_.shape
            dk = d // h
            Qh = Q.reshape(L, h, dk).transpose(1, 0, 2)
            Kh = K.reshape(L, h, dk).transpose(1, 0, 2)
            Vh = V.reshape(L, h, dk).transpose(1, 0, 2)
            heads = []
            for i in range(h):
                scores = Qh[i] @ Kh[i].T / np.sqrt(dk)
                scores = scores - scores.max(axis=-1, keepdims=True)
                w = np.exp(scores)
                w = w / w.sum(axis=-1, keepdims=True)
                heads.append(w @ Vh[i])
            return np.concatenate(heads, axis=-1) @ Wo

        def layernorm(x):
            # 对每个 token 沿特征维：总体方差（除以 d）
            mean = x.mean(axis=-1, keepdims=True)
            var = ((x - mean) ** 2).mean(axis=-1, keepdims=True)
            return (x - mean) / np.sqrt(var + eps)

        x1 = layernorm(X + mha(X))
        # FFN: ReLU(xW1+b1)W2+b2
        ffn = np.maximum(0.0, x1 @ W1 + b1) @ W2 + b2
        return layernorm(x1 + ffn)


if __name__ == "__main__":
    import sys
    data = sys.stdin.read().strip().split()
    it = iter(data)
    L = int(next(it)); d = int(next(it)); h = int(next(it)); dff = int(next(it))

    def read_mat(r, c):
        return [[float(next(it)) for _ in range(c)] for _ in range(r)]

    X = read_mat(L, d)
    Wq = read_mat(d, d)
    Wk = read_mat(d, d)
    Wv = read_mat(d, d)
    Wo = read_mat(d, d)
    W1 = read_mat(d, dff)
    b1 = [float(next(it)) for _ in range(dff)]
    W2 = read_mat(dff, d)
    b2 = [float(next(it)) for _ in range(d)]
    out = Solution().transformerEncoderBlock(X, Wq, Wk, Wv, Wo, W1, b1, W2, b2, h)
    lines = [" ".join(f"{float(x):.4f}" for x in row) for row in out]
    sys.stdout.write("\n".join(lines) + "\n")
