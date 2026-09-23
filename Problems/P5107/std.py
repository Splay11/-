# -*- coding: utf-8 -*-


class Solution:
    def rearrangeSN(self, sn: str, m: int) -> str:
        # 仅允许字母、数字与破折号；其它字符视为异常
        for c in sn:
            if not (c.isalnum() or c == "-"):
                return ""

        chars = []
        # 按原顺序提取字母数字并转大写
        for c in sn:
            if c.isalnum():
                chars.append(c.upper())

        if not chars:
            return ""

        n = len(chars)
        rem = n % m
        groups = []
        idx = 0
        # 有余数时首段长度不足 m
        if rem != 0:
            groups.append("".join(chars[idx : idx + rem]))
            idx += rem
        while idx < n:
            groups.append("".join(chars[idx : idx + m]))
            idx += m
        return "-".join(groups)
