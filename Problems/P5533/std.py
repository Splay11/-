import math


class Solution:
    def crossEntropy(self, logits, labels):
        """数值稳定交叉熵：返回 per-sample 损失、平均损失、对 logits 的梯度。"""
        n = len(logits)
        k = len(logits[0])
        losses = []
        grads = []
        for i in range(n):
            z = logits[i]
            # log-sum-exp：先减最大值保证数值稳定
            m = max(z)
            exps = [math.exp(v - m) for v in z]
            s = sum(exps)
            # CE = -z_y + logsumexp(z)
            loss = -z[labels[i]] + m + math.log(s)
            losses.append(loss)
            # softmax
            sm = [e / s for e in exps]
            # grad = softmax - one_hot(y)
            g = list(sm)
            g[labels[i]] -= 1.0
            grads.append(g)
        avg = sum(losses) / n
        return losses, avg, grads


if __name__ == "__main__":
    N, K = map(int, input().split())
    logits = []
    for _ in range(N):
        logits.append(list(map(float, input().split())))
    labels = list(map(int, input().split()))
    losses, avg, grads = Solution().crossEntropy(logits, labels)
    print(" ".join(f"{x:.2f}" for x in losses))
    print(f"{avg:.2f}")
    for g in grads:
        print(" ".join(f"{x:.2f}" for x in g))
