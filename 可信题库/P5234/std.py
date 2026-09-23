class Solution:
    def sortLetter(self, lettersStr: str) -> str:
        chars = sorted(lettersStr)
        out = []
        for c in chars:
            pos = ord(c.lower()) - ord("a") + 1
            new_pos = (pos * pos) % 26 + 1
            ch = chr(ord("A") + new_pos - 1)
            out.append(ch.lower() if c.isupper() else ch.upper())
        return "".join(out)
