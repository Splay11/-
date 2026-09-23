# -*- coding: utf-8 -*-


class Solution:
    def minDistinctAfterSwap(self, resA: str, resB: str) -> int:
        countA = [0] * 26
        countB = [0] * 26
        for c in resA:
            countA[ord(c) - ord("a")] += 1
        for c in resB:
            countB[ord(c) - ord("a")] += 1

        dA = sum(1 for x in countA if x > 0)
        dB = sum(1 for x in countB if x > 0)

        ans = -1
        for a in range(26):
            if countA[a] == 0:
                continue
            for b in range(26):
                if countB[b] == 0:
                    continue
                if a == b:
                    if dA != dB:
                        continue
                    cand = dA
                else:
                    da = dA - (1 if countA[a] == 1 else 0) + (1 if countA[b] == 0 else 0)
                    db = dB - (1 if countB[b] == 1 else 0) + (1 if countB[a] == 0 else 0)
                    if da != db:
                        continue
                    cand = da
                if ans == -1 or cand < ans:
                    ans = cand
        return ans
