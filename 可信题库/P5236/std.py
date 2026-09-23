class Cell:
    def __init__(self, rowNum: int, colNum: int, content: str):
        self.rowNum = rowNum
        self.colNum = colNum
        self.content = content


class Solution:
    def transformTable(self, table: list) -> list:
        cells = []
        for c in table:
            if isinstance(c, Cell):
                cells.append(c)
            else:
                cells.append(Cell(int(c[0]), int(c[1]), str(c[2])))
        if not cells:
            return []

        # 1-based：列数为 max(col)；行只保留出现过的 rowNum
        rows = sorted({c.rowNum for c in cells})
        C = max(c.colNum for c in cells)
        grid = {r: [""] * C for r in rows}
        for cell in cells:
            grid[cell.rowNum][cell.colNum - 1] = cell.content

        w = 3
        for r in rows:
            for content in grid[r]:
                w = max(w, len(content))

        def pad(s: str) -> str:
            return s + " " * (w - len(s))

        sep = "+" + "+".join(["-" * w] * C) + "+"
        lines = [sep]
        for r in rows:
            lines.append("|" + "|".join(pad(grid[r][c]) for c in range(C)) + "|")
        lines.append(sep)
        return lines
