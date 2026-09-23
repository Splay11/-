from typing import List


class Solution:
    def hasFiveInRow(self, blackChessPoses: List[List[int]]) -> str:
        s = {(x, y) for x, y in blackChessPoses}
        dirs = ((1, 0), (0, 1), (1, 1), (1, -1))
        for x, y in s:
            for dx, dy in dirs:
                # 只从连线起点枚举，避免重复
                if (x - dx, y - dy) in s:
                    continue
                cnt = 0
                cx, cy = x, y
                while (cx, cy) in s:
                    cnt += 1
                    if cnt >= 5:
                        return "YES"
                    cx += dx
                    cy += dy
        return "NO"
