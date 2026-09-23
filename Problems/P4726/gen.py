# -*- coding: utf-8 -*-
"""生成 data/*.in/*.out；与 std.py 自校验。样例形态与题面一致：[[...]],maxDiff（逗号后无多余空格）。.in 末尾无换行，.out 末尾单换行。"""

import ast
import importlib.util
import random
from pathlib import Path

SEED = 472608917
RNG = random.Random(SEED)


def fmt_in(grid, k: int) -> str:
    """与题面样例同形：无空格、无行末换行。"""
    rows = []
    for row in grid:
        rows.append("[" + ",".join(str(x) for x in row) + "]")
    return "[" + ",".join(rows) + "]," + str(k)


def split_grid_k(line: str):
    line = line.strip()
    d = 0
    end = -1
    for i, c in enumerate(line):
        if c == "[":
            d += 1
        elif c == "]":
            d -= 1
            if d == 0:
                end = i
                break
    if end < 0:
        raise ValueError("unbalanced")
    grid_s = line[: end + 1]
    tail = line[end + 1 :].strip()
    if not tail.startswith(","):
        raise ValueError("need comma")
    k = int(tail[1:].strip())
    return ast.literal_eval(grid_s), k


def fmt_out(v: int) -> str:
    return str(int(v)) + "\n"


def build_cases():
    cases = []

    cases.append(fmt_in([[1, 2], [3, 5]], 2))
    cases.append(fmt_in([[4, 3], [3, 2]], 1))
    cases.append(fmt_in([[1, 3], [3, 4]], 1))

    cases.append(fmt_in([[1, 10, 20], [5, 15, 25], [30, 35, 40]], 50))

    cases.append(fmt_in([[1, 2, 3], [2, 3, 4], [3, 4, 5]], 1))

    cases.append(fmt_in([[1, 100], [50, 200]], 49))

    # 7：10x10，唯一最小 0、唯一最大 9999
    g7 = [[RNG.randint(10, 9990) for _ in range(10)] for _ in range(10)]
    g7[3][4] = 0
    g7[8][1] = 9999
    for i in range(10):
        for j in range(10):
            if (i, j) == (3, 4) or (i, j) == (8, 1):
                continue
            if g7[i][j] <= 0:
                g7[i][j] = RNG.randint(1, 5000)
            if g7[i][j] >= 9999:
                g7[i][j] = RNG.randint(1, 8000)
    cases.append(fmt_in(g7, 250))

    # 8：10x10 阶梯矩阵（整体 +2 避免与强行写入的 1 冲突），maxDiff 适中
    g8 = [[i * 10 + j + 2 for j in range(10)] for i in range(10)]
    g8[0][0] = 1
    g8[9][9] = 200
    cases.append(fmt_in(g8, 12))

    cases.append(fmt_in([[1, 4, 7, 10, 13, 16, 19, 22, 25, 28], [2, 5, 8, 11, 14, 17, 20, 23, 26, 50]], 3))

    # 10：5x5 明确唯一最小/最大
    cases.append(
        fmt_in(
            [
                [10, 20, 30, 40, 50],
                [11, 21, 31, 41, 51],
                [12, 22, 32, 42, 52],
                [13, 23, 33, 43, 53],
                [14, 24, 34, 44, 99],
            ],
            15,
        )
    )

    assert len(cases) == 10
    return cases


def load_solution_class():
    p = Path(__file__).resolve().parent / "std.py"
    spec = importlib.util.spec_from_file_location("p4726_std", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.Solution


def main() -> None:
    data = Path(__file__).resolve().parent / "data"
    data.mkdir(parents=True, exist_ok=True)
    Sol = load_solution_class()
    cases = build_cases()
    for i, line in enumerate(cases, start=1):
        grid, k = split_grid_k(line)
        want = int(Sol().countHikingPaths(grid, k))
        inp = data / f"{i}.in"
        outp = data / f"{i}.out"
        inp.write_bytes(line.encode("utf-8"))
        with outp.open("w", encoding="utf-8", newline="\n") as f:
            f.write(fmt_out(want))
    for i in range(1, len(cases) + 1):
        raw = (data / f"{i}.in").read_bytes()
        if raw.endswith(b"\n"):
            raise SystemExit(f".in {i} must not end with newline")
        line = raw.decode("utf-8")
        grid, k = split_grid_k(line)
        disk = int((data / f"{i}.out").read_text(encoding="utf-8").strip())
        got = int(Sol().countHikingPaths(grid, k))
        if got != disk:
            raise SystemExit(f"reverify fail {i}: disk={disk} got={got}")
    print("ok:", len(cases), "pairs")


if __name__ == "__main__":
    main()
