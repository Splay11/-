class Solution:
    def reviseMarks(self, s: str) -> str:
        i0 = i1 = -1
        for i, ch in enumerate(s):
            if ch == "0" and i0 < 0:
                i0 = i
            elif ch == "1" and i1 < 0:
                i1 = i
            if i0 >= 0 and i1 >= 0:
                break
        out = []
        for i, ch in enumerate(s):
            if i != i0 and i != i1:
                out.append(ch)
        return "".join(out)
