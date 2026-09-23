# -*- coding: utf-8 -*-


class Solution:
    def processChunks(self, s: str, n: int) -> str:
        def dedup(chunk: str) -> str:
            last = {}
            for i, c in enumerate(chunk):
                last[c] = i
            return "".join(c for i, c in enumerate(chunk) if last[c] == i)

        parts = []
        for i in range(0, len(s), n):
            parts.append(dedup(s[i : i + n]))
        return "".join(parts)
