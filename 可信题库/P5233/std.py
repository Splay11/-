from collections import defaultdict
from typing import List


class Solution:
    def countSimilarGroups(self, uriReqs: List[str]) -> int:
        segs = [u[1:].split("/") for u in uriReqs]
        remaining = set(range(len(segs)))
        groups = 0
        while True:
            prefix_members = defaultdict(list)
            for i in remaining:
                s = segs[i]
                for L in range(1, len(s) + 1):
                    prefix_members[tuple(s[:L])].append(i)
            best_L = 0
            best_key = None
            for pref, mems in prefix_members.items():
                if len(mems) >= 2 and len(pref) > best_L:
                    best_L = len(pref)
                    best_key = pref
            if best_L == 0:
                break
            for i in prefix_members[best_key]:
                remaining.discard(i)
            groups += 1
        return groups
