from typing import List


class Solution:
    def minAuditDays(self, loads: List[int]) -> int:
        # 空数组无需抽查
        if not loads:
            return 0
        # 先算总负载；选出之和必须严格大于一半
        total = sum(loads)
        # 贪心：优先抽查负载最大的天，天数才可能最少
        a = sorted(loads, reverse=True)
        s = 0
        for i, x in enumerate(a, 1):
            s += x
            # 2*s > total 等价于 s > total - s
            if s * 2 > total:
                return i
        return len(a)
