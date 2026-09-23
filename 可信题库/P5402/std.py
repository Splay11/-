from typing import List, Tuple

MASK = (1 << 64) - 1
P = 131
Q = 13331


def _build(g: List[List[str]]) -> Tuple[List[List[int]], int, int]:
    m, n = len(g), len(g[0])
    h = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m):
        for j in range(n):
            v = ord(g[i][j]) - 64
            h[i + 1][j + 1] = (
                h[i][j + 1] * P + h[i + 1][j] * Q - h[i][j] * P * Q + v
            ) & MASK
    return h, m, n


def _pw(k: int, base: int) -> List[int]:
    a = [1] * (k + 1)
    for i in range(1, k + 1):
        a[i] = (a[i - 1] * base) & MASK
    return a


def _rect(h: List[List[int]], r: int, c: int, a: int, b: int, pP: List[int], pQ: List[int]) -> int:
    v = h[r + a][c + b]
    v = (v - h[r][c + b] * pP[a]) & MASK
    v = (v - h[r + a][c] * pQ[b]) & MASK
    v = (v + h[r][c] * pP[a] * pQ[b]) & MASK
    return v


class Solution:
    def findStampPos(self, tray: List[List[str]], stamp: List[List[str]]) -> List[int]:
        ht, m, n = _build(tray)
        hs, a, b = _build(stamp)
        pP = _pw(m, P)
        pQ = _pw(n, Q)
        need = _rect(hs, 0, 0, a, b, pP, pQ)
        for i in range(m - a + 1):
            for j in range(n - b + 1):
                if _rect(ht, i, j, a, b, pP, pQ) == need:
                    return [i, j]
        return [-1, -1]
