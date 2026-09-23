# -*- coding: utf-8 -*-
from typing import List
import numpy as np


class Solution:
    def mlaForward(
        self,
        X: List[List[float]],
        W_DQ: List[List[float]],
        W_UQ: List[List[float]],
        W_DKV: List[List[float]],
        W_UK: List[List[float]],
        W_UV: List[List[float]],
        W_QR: List[List[float]],
        W_KR: List[List[float]],
        W_o: List[List[float]],
        n_h: int,
        d_h: int,
        d_rope: int,
    ) -> List[List[float]]:
        """MLA：KV 低秩潜变量 + 内容/位置分数相加 + 因果掩码。"""
        X = np.asarray(X, dtype=np.float64)
        W_DQ = np.asarray(W_DQ, dtype=np.float64)
        W_UQ = np.asarray(W_UQ, dtype=np.float64)
        W_DKV = np.asarray(W_DKV, dtype=np.float64)
        W_UK = np.asarray(W_UK, dtype=np.float64)
        W_UV = np.asarray(W_UV, dtype=np.float64)
        W_QR = np.asarray(W_QR, dtype=np.float64)
        W_KR = np.asarray(W_KR, dtype=np.float64)
        W_o = np.asarray(W_o, dtype=np.float64)
        N = X.shape[0]
        # 低秩压缩：C_q / C_kv
        C_q = X @ W_DQ
        C_kv = X @ W_DKV
        Q_c = C_q @ W_UQ
        K_c = C_kv @ W_UK
        V = C_kv @ W_UV
        # 位置部分（输入已是旋转后投影）
        Q_r = X @ W_QR
        K_r = X @ W_KR  # 共享 RoPE Key
        heads = []
        for h in range(n_h):
            qc = Q_c[:, h * d_h:(h + 1) * d_h]
            kc = K_c[:, h * d_h:(h + 1) * d_h]
            vv = V[:, h * d_h:(h + 1) * d_h]
            qr = Q_r[:, h * d_rope:(h + 1) * d_rope]
            # 内容分数 + 位置分数
            scores = (qc @ kc.T) / np.sqrt(d_h) + (qr @ K_r.T) / np.sqrt(d_rope)
            # 因果掩码：未来位置 j>i 置 -inf
            mask = np.triu(np.ones((N, N), dtype=bool), k=1)
            scores = scores.copy()
            scores[mask] = -1e9
            scores = scores - scores.max(axis=1, keepdims=True)
            w = np.exp(scores)
            w = w / w.sum(axis=1, keepdims=True)
            heads.append(w @ vv)
        out = np.concatenate(heads, axis=1) @ W_o
        return out.tolist()


if __name__ == "__main__":
    import sys

    def read_mat(it, rows, cols):
        return [[float(next(it)) for _ in range(cols)] for _ in range(rows)]

    data = sys.stdin.read().strip().split()
    it = iter(data)
    N = int(next(it)); d = int(next(it)); n_h = int(next(it)); n_q = int(next(it))
    d_c = int(next(it)); d_h = int(next(it)); d_rope = int(next(it))
    X = read_mat(it, N, d)
    W_DQ = read_mat(it, d, n_q)
    W_UQ = read_mat(it, n_q, n_h * d_h)
    W_DKV = read_mat(it, d, d_c)
    W_UK = read_mat(it, d_c, n_h * d_h)
    W_UV = read_mat(it, d_c, n_h * d_h)
    W_QR = read_mat(it, d, n_h * d_rope)
    W_KR = read_mat(it, d, d_rope)
    W_o = read_mat(it, n_h * d_h, d)
    out = Solution().mlaForward(X, W_DQ, W_UQ, W_DKV, W_UK, W_UV, W_QR, W_KR, W_o, n_h, d_h, d_rope)
    for row in out:
        print(" ".join(f"{x:.4f}" for x in row))
