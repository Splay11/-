# -*- coding: utf-8 -*-
from typing import List


class Solution:
    def minShareOps(self, pieces: List[int]) -> int:
        if not pieces or len(pieces) < 2:
            return 0
        mx = max(pieces) + 1
        spf = list(range(mx + 1))
        for i in range(2, int(mx**0.5) + 1):
            if spf[i] == i:
                for j in range(i * i, mx + 1, i):
                    if spf[j] == j:
                        spf[j] = i

        def factors(x: int):
            s = set()
            while x > 1:
                p = spf[x]
                s.add(p)
                while x % p == 0:
                    x //= p
            return s

        cnt = {}
        facs = []
        for v in pieces:
            fs = factors(v)
            facs.append(fs)
            for p in fs:
                cnt[p] = cnt.get(p, 0) + 1
        for c in cnt.values():
            if c >= 2:
                return 0

        for i, v in enumerate(pieces):
            for p in factors(v + 1):
                if p in facs[i]:
                    if cnt.get(p, 0) >= 2:
                        return 1
                elif cnt.get(p, 0) >= 1:
                    return 1
        return 2
