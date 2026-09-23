# -*- coding: utf-8 -*-


def normalize(story: str) -> str:
    s = story.strip(" ")
    if not s:
        return ""
    out = []
    i = 0
    while i < len(s):
        if s[i] == " ":
            if out:
                out.append(" ")
            while i < len(s) and s[i] == " ":
                i += 1
        else:
            out.append(s[i])
            i += 1
    res = "".join(out)
    if res and res[-1] == " ":
        res = res.rstrip(" ")
    return res


class Solution:
    def lengthOfLongestSubstring(self, story: str) -> int:
        t = normalize(story)
        if not t:
            return 0
        last = {}
        left = 0
        best = 0
        for right, ch in enumerate(t):
            key = ch.lower()
            if key in last and last[key] >= left:
                left = last[key] + 1
            last[key] = right
            best = max(best, right - left + 1)
        return best
