# -*- coding: utf-8 -*-
from collections import defaultdict
from typing import List


class Solution:
    def getLoadedFileIds(
        self, fileIds: List[int], parentIds: List[int], targetId: int
    ) -> List[int]:
        children = defaultdict(list)
        for fid, pid in zip(fileIds, parentIds):
            children[pid].append(fid)

        ans = []
        stack = [targetId]
        while stack:
            u = stack.pop()
            ans.append(u)
            for v in children[u]:
                stack.append(v)
        ans.sort()
        return ans
