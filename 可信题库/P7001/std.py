from typing import List


class Solution:
    def peakConcurrent(self, starts: List[int], ends: List[int]) -> int:
        starts = sorted(starts)
        ends = sorted(ends)
        i = j = 0
        cur = ans = 0
        n = len(starts)
        while i < n:
            # 半开区间：终点与起点重合时先结束再开始
            if starts[i] < ends[j]:
                cur += 1
                if cur > ans:
                    ans = cur
                i += 1
            else:
                cur -= 1
                j += 1
        return ans
