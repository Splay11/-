# -*- coding: utf-8 -*-


class Solution:
    def processString(self, s: str) -> str:
        digits = [c for c in s if c.isdigit()]
        letters = [c for c in s if c.isalpha()]
        # 只含字母或只含数字：原样返回
        if not digits or not letters:
            return s
        parts = []
        n = min(len(digits), len(letters))
        for i in range(n):
            d = digits[i]
            parts.append(d)
            cnt = ord(d) - ord("0")
            if cnt > 0:
                parts.append(letters[i] * cnt)
        if len(digits) > len(letters):
            parts.extend(digits[n:])
        elif len(letters) > len(digits):
            parts.extend(letters[n:])
        return "".join(parts)
