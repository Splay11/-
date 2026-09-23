class Solution:
    def maxSplitProduct(self, seq: str) -> int:
        n = len(seq)
        ans = 0
        for k in range(1, n):
            prod = int(seq[:k]) * int(seq[k:])
            if prod > ans:
                ans = prod
        return ans
