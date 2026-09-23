from typing import List


class Solution:
    def countNeedUpgrade(self, versions: List[int], baseline: int) -> int:
        # 先排序，才能二分找「第一个 >= baseline」的位置
        a = sorted(versions)
        n = len(a)
        lo, hi = 0, n
        # 标准 lower_bound：找到最左满足 a[i] >= baseline 的下标
        while lo < hi:
            mid = (lo + hi) // 2
            if a[mid] < baseline:
                # 中点仍偏小，答案在右半
                lo = mid + 1
            else:
                # 中点可能就是答案，或还在左边
                hi = mid
        # [lo, n) 都是 >= baseline
        return n - lo
