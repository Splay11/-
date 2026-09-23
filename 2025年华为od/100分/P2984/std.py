# -*- coding: utf-8 -*-
class Solution:
    def countFormableGroups(self, a: str, b: str) -> int:
        chars = list(a)
        ans = 0
        while True:
            j = 0
            nxt = []
            for ch in chars:
                if j < len(b) and ch == b[j]:
                    j += 1
                else:
                    nxt.append(ch)
            if j == len(b):
                ans += 1
                chars = nxt
            else:
                break
        return ans
