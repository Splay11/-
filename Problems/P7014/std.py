from typing import List


class Solution:
    def maxOnline(self, changes: List[int]) -> int:
        # cur：当前在线；ans：历史峰值
        cur = 0
        ans = 0
        for x in changes:
            # 按时间顺序累加变化量
            cur += x
            # 维护前缀最大值
            if cur > ans:
                ans = cur
        return ans
