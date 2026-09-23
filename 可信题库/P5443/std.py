from typing import List


class Solution:
    def minAdjacentGap(self, cookies: List[int]) -> int:
        # 先把第一对相邻烤盘的差当作当前最小答案
        ans = abs(cookies[1] - cookies[0])
        for i in range(1, len(cookies) - 1):
            # 算第 i 盘和第 i+1 盘的差，差值不分方向，取绝对值
            gap = abs(cookies[i + 1] - cookies[i])
            # 出现更小的差就更新答案
            if gap < ans:
                ans = gap
        return ans
