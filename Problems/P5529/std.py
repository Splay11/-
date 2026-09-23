class Solution:
    def binaryAUC(self, y, pred):
        """根据标签与预测概率计算二分类 AUC。"""
        pos = []
        neg = []
        # 按标签拆成正负样本的预测概率
        for yi, pi in zip(y, pred):
            if yi == 1:
                pos.append(pi)
            else:
                neg.append(pi)
        # AUC = 正样本分数大于负样本的概率；相等计 0.5
        total = len(pos) * len(neg)
        good = 0.0
        for p in pos:
            for q in neg:
                if p > q:
                    good += 1.0
                elif p == q:
                    good += 0.5
        return good / total


if __name__ == "__main__":
    n = int(input())
    y = []
    pred = []
    for _ in range(n):
        yi, pi = input().split()
        y.append(int(yi))
        pred.append(float(pi))
    ans = Solution().binaryAUC(y, pred)
    print(f"{ans:.4f}")
