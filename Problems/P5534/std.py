import math


class Solution:
    def binaryCrossEntropy(self, y, p):
        """二分类 BCE，概率裁剪到 [eps, 1-eps]。"""
        eps = 1e-7
        n = len(y)
        s = 0.0
        for yi, pi in zip(y, p):
            # 裁剪避免 log(0)
            pi = min(max(pi, eps), 1.0 - eps)
            s += yi * math.log(pi) + (1.0 - yi) * math.log(1.0 - pi)
        return -s / n


if __name__ == "__main__":
    N = int(input())
    y = list(map(int, input().split()))
    p = list(map(float, input().split()))
    ans = Solution().binaryCrossEntropy(y, p)
    print(f"{ans:.2f}")
