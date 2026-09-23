from typing import List


class Solution:
    def bestCorrectedTotal(self, scores: List[int]) -> int:
        total = 0
        # 数组非空，先把第一项当作最小值
        mn = scores[0]
        # 一趟循环同时求出原总分与最小项
        for v in scores:
            total += v
            if v < mn:
                mn = v
        # 订正最小项后总分是 total - 2 * mn，这是所有选择里最大的
        return total - 2 * mn
