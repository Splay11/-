from typing import List


class Solution:
    def firstDuplicate(self, users: List[int]) -> int:
        seen = set()
        for u in users:
            if u in seen:
                return u
            seen.add(u)
        return -1
