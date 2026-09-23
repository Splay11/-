from typing import List


class Solution:
    def bestBandwidth(self, packages: List[List[int]], budget: int) -> int:
        best_bw = -1
        best_price = None
        for bw, price in packages:
            if price > budget:
                continue
            if best_bw < 0 or bw > best_bw or (bw == best_bw and price < best_price):
                best_bw = bw
                best_price = price
        return best_bw
