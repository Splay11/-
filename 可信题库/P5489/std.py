from typing import List


class Solution:
    def bestShotRecords(self, scores: List[int]) -> List[int]:
        cnt = 1
        last = 0
        best = scores[0]
        gap = 0
        for i in range(1, len(scores)):
            if scores[i] > best:
                if i - last > gap:
                    gap = i - last
                last = i
                best = scores[i]
                cnt += 1
        return [cnt, gap]
