import numpy as np


class Solution:
    def adamUpdate(self, theta, grads, alpha, beta1, beta2, eps):
        """按 Adam（含偏置修正）逐步更新参数，返回每步后的 theta。"""
        theta = np.asarray(theta, dtype=np.float64).copy()
        m = np.zeros_like(theta)
        v = np.zeros_like(theta)
        outs = []
        for t, g in enumerate(grads, 1):
            g = np.asarray(g, dtype=np.float64)
            # 一阶/二阶矩的指数滑动平均
            m = beta1 * m + (1.0 - beta1) * g
            v = beta2 * v + (1.0 - beta2) * (g * g)
            # 偏差修正：抵消 m0=v0=0 的初期偏置
            m_hat = m / (1.0 - beta1 ** t)
            v_hat = v / (1.0 - beta2 ** t)
            theta = theta - alpha * m_hat / (np.sqrt(v_hat) + eps)
            outs.append(theta.copy())
        return outs


if __name__ == "__main__":
    import sys
    data = sys.stdin.read().strip().split()
    it = iter(data)
    d = int(next(it)); T = int(next(it))
    alpha = float(next(it)); beta1 = float(next(it)); beta2 = float(next(it)); eps = float(next(it))
    theta = [float(next(it)) for _ in range(d)]
    grads = [[float(next(it)) for _ in range(d)] for _ in range(T)]
    outs = Solution().adamUpdate(theta, grads, alpha, beta1, beta2, eps)
    lines = [" ".join(f"{float(x):.4f}" for x in row) for row in outs]
    sys.stdout.write("\n".join(lines) + "\n")
