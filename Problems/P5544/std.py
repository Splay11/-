import numpy as np


class Solution:
    def im2col_conv1d(self, x, w, S, P):
        # 返回 (im2col矩阵 O x K, 卷积结果 y)
        x = np.asarray(x, dtype=np.float64)
        w = np.asarray(w, dtype=np.float64)
        K = len(w)
        # 两端补零
        if P > 0:
            xp = np.pad(x, (P, P), mode="constant")
        else:
            xp = x
        L2 = len(xp)
        O = (L2 - K) // S + 1
        C = np.zeros((O, K), dtype=np.float64)
        for i in range(O):
            # 第 i 行取滑窗片段
            C[i] = xp[i * S : i * S + K]
        y = C @ w
        return C, y


if __name__ == "__main__":
    import sys
    data = sys.stdin.read().strip().split()
    it = iter(data)
    L = int(next(it)); K = int(next(it)); S = int(next(it)); P = int(next(it))
    x = [float(next(it)) for _ in range(L)]
    w = [float(next(it)) for _ in range(K)]
    C, y = Solution().im2col_conv1d(x, w, S, P)
    O = C.shape[0]
    lines = [f"{O} {K}"]
    for row in C:
        lines.append(" ".join(f"{float(v):.4f}" for v in row))
    lines.append(" ".join(f"{float(v):.4f}" for v in y))
    sys.stdout.write("\n".join(lines) + "\n")
