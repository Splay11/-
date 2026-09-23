# -*- coding: utf-8 -*-
class Solution:
    def countOpenSyllables(self, s: str) -> int:
        vowels = set("aeiou")

        def is_consonant(ch: str) -> bool:
            return "a" <= ch <= "z" and ch not in vowels

        words = s.split(" ")
        parts = []
        for w in words:
            if w and all("a" <= ch <= "z" for ch in w):
                parts.append(w[::-1])
            else:
                parts.append(w)
        text = " ".join(parts)

        ans = 0
        for i in range(len(text) - 3):
            a, b, c, d = text[i], text[i + 1], text[i + 2], text[i + 3]
            if is_consonant(a) and b in vowels and is_consonant(c) and c != "r" and d == "e":
                ans += 1
        return ans
