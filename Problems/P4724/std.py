# -*- coding: utf-8 -*-
from typing import List


class Solution:
    def findMaxOccupiedPaths(self, target: str, files: List[str], sizes: List[int]) -> List[str]:
        exists = any(p == target or (len(p) > len(target) and p.startswith(target + "/")) for p in files)
        if not exists:
            return []
        agg = {}
        for p, sz in zip(files, sizes):
            if p == target:
                continue
            if not (len(p) > len(target) and p.startswith(target + "/")):
                continue
            rel = p[len(target) + 1 :]
            slash = rel.find("/")
            if slash < 0:
                child = p
            else:
                child = target + "/" + rel[:slash]
            agg[child] = agg.get(child, 0) + int(sz)
        if not agg:
            return []
        mx = max(agg.values())
        out = [k for k, v in agg.items() if v == mx]
        out.sort()
        return out
