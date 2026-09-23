import math


class Solution:
    def logisticRegression(self, X, y, max_iter, alpha, tol, X_test):
        """按题面批量梯度下降训练逻辑回归，返回测试集 (类别, 概率)。"""
        n = len(X)
        d = len(X[0])
        W = [0.0] * d
        b = 0.0

        def sigmoid(z):
            # 数值稳定 sigmoid
            if z >= 0:
                return 1.0 / (1.0 + math.exp(-z))
            ez = math.exp(z)
            return ez / (1.0 + ez)

        prev_loss = None
        for _ in range(max_iter):
            # 前向：p = sigmoid(XW + b)
            p = []
            for i in range(n):
                z = b
                for j in range(d):
                    z += X[i][j] * W[j]
                p.append(sigmoid(z))
            # 交叉熵损失
            loss = 0.0
            for i in range(n):
                pi = min(max(p[i], 1e-15), 1.0 - 1e-15)
                loss -= y[i] * math.log(pi) + (1.0 - y[i]) * math.log(1.0 - pi)
            loss /= n
            if prev_loss is not None and abs(prev_loss - loss) <= tol:
                break
            prev_loss = loss
            # 梯度：W -= alpha/n * X^T (p-y)，b -= alpha * mean(p-y)
            diff = [p[i] - y[i] for i in range(n)]
            for j in range(d):
                g = 0.0
                for i in range(n):
                    g += X[i][j] * diff[i]
                W[j] -= alpha * g / n
            b -= alpha * (sum(diff) / n)

        # 预测测试集
        out = []
        for row in X_test:
            z = b
            for j in range(d):
                z += row[j] * W[j]
            prob = sigmoid(z)
            label = 1 if prob >= 0.5 else 0
            out.append((label, prob))
        return out


if __name__ == "__main__":
    parts = input().split()
    n = int(parts[0])
    max_iter = int(parts[1])
    alpha = float(parts[2])
    tol = float(parts[3])
    X = []
    y = []
    for _ in range(n):
        a, b, c, lab = input().split()
        X.append([float(a), float(b), float(c)])
        y.append(float(lab))
    m = int(input())
    X_test = []
    for _ in range(m):
        X_test.append(list(map(float, input().split())))
    ans = Solution().logisticRegression(X, y, max_iter, alpha, tol, X_test)
    for label, prob in ans:
        print(f"{label} {prob:.4f}")
