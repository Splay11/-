# -*- coding: utf-8 -*-
class Solution:
    def maxBracketDepth(self, s: str) -> int:
        pair = {")": "(", "]": "[", "}": "{"}
        stack = []
        depth = 0
        best = 0
        for ch in s:
            if ch in "([{":
                stack.append(ch)
                depth += 1
                if depth > best:
                    best = depth
            elif ch in pair:
                if not stack or stack[-1] != pair[ch]:
                    return 0
                stack.pop()
                depth -= 1
            else:
                return 0
        return best if not stack else 0
