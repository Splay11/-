# -*- coding: utf-8 -*-
"""P5559 货格最少框边：10 组测例。"""
from __future__ import annotations

import math
import random
import sys
from itertools import combinations
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
from std import min_side  # noqa: E402

DATA = ROOT / "data"
RNG = random.Random(555920260922)


def brute(k: int, cols: list[int], rows: list[int]) -> int:
    # 恰好选 k 件，边长 = 列跨度与行跨度的较大值再加 1
    pts = list(zip(cols, rows))
    best = 10**9
    for comb in combinations(pts, k):
        xs = [p[0] for p in comb]
        ys = [p[1] for p in comb]
        side = max(max(xs) - min(xs), max(ys) - min(ys)) + 1
        if side < best:
            best = side
    return best


def write_in(path: Path, k: int, cols: list[int], rows: list[int]) -> None:
    lines = [
        str(k),
        str(len(cols)),
        " ".join(str(x) for x in cols),
        " ".join(str(x) for x in rows),
    ]
    path.write_bytes("\n".join(lines).encode("utf-8"))


def write_out(path: Path, ans: int) -> None:
    path.write_bytes((str(ans) + "\n").encode("utf-8"))


def dump_case(
    idx: int,
    k: int,
    cols: list[int],
    rows: list[int],
    expect: int | None = None,
    check_brute: bool = False,
) -> int:
    if len(cols) != len(rows):
        raise SystemExit(f"case {idx} length mismatch")
    if len(set(zip(cols, rows))) != len(cols):
        raise SystemExit(f"case {idx} duplicate cell")
    ans = min_side(k, cols, rows)
    if expect is not None and ans != expect:
        raise SystemExit(f"case {idx} expect {expect} got {ans}")
    if check_brute:
        if math.comb(len(cols), k) > 200000:
            raise SystemExit(f"case {idx} brute too big")
        got = brute(k, cols, rows)
        if got != ans:
            raise SystemExit(f"case {idx} brute {got} std {ans}")
    write_in(DATA / f"{idx}.in", k, cols, rows)
    write_out(DATA / f"{idx}.out", ans)
    return ans


def write_config() -> None:
    cases = "\n".join(
        f"      - input: {i}.in\n        output: {i}.out" for i in range(1, 11)
    )
    config = f"""type: default
time: 3s
memory: 512m
subtasks:
  - score: 100
    if: []
    id: 1
    type: sum
    cases:
{cases}
langs:
  - c
  - cc.cc14o2
  - cc
  - java
  - py.py3
  - py
"""
    DATA.mkdir(parents=True, exist_ok=True)
    (DATA / "config.yaml").write_text(config, encoding="utf-8")


def write_readme() -> None:
    text = """# P5559 测例说明

输入四行：需要件数 $k$、货件数 $p$、全部列号、全部行号。输出最小正方形边长。`.in` 末尾无换行，`.out` 末尾恰好一个换行。

- 1：四级样例 1。三件货落在边长 $2$ 的框里，远处那件不必纳入。
- 2：四级样例 2。同列两件行号相差 $2$，边长是 $3$。卡忘记「最大坐标差 $+1$」。
- 3：只有 $1$ 件。答案是 $1$。
- 4：相邻两格，要 $2$ 件。答案是 $2$。卡把边长写成坐标差本身。
- 5：四角各一件，要全部盖住。答案是 $1000$。
- 6：左上角 $3\\times 3$ 共 $9$ 件，再加 $(1000,1000)$，只要 $9$ 件。答案是 $3$。卡「把所有货的外接框当答案」。
- 7：列上挨着但行差很大的两件，另有三件能被边长 $9$ 盖住。卡只按一维滑窗。
- 8：$16$ 件小随机，与组合暴力对拍。
- 9：$p=100000$ 均匀散落，$k=200$。压测二分加前缀和。
- 10：$99999$ 件挤在左上角，再加 $(1000,1000)$，要全部盖住。答案是 $1000$。卡漏掉角落、也压测满规模读入。
"""
    (DATA / "README.md").write_text(text, encoding="utf-8")


def fill_block(limit: int) -> tuple[list[int], list[int]]:
    cols: list[int] = []
    rows: list[int] = []
    for c in range(1, 318):
        for r in range(1, 318):
            cols.append(c)
            rows.append(r)
            if len(cols) == limit:
                return cols, rows
    raise SystemExit("block too small")


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    dump_case(1, 3, [2, 3, 2, 9], [1, 1, 2, 9], 2, True)
    dump_case(2, 2, [4, 4, 8], [1, 3, 1], 3, True)
    dump_case(3, 1, [7], [8], 1, True)
    dump_case(4, 2, [1, 1], [1, 2], 2, True)
    dump_case(5, 4, [1, 1, 1000, 1000], [1, 1000, 1, 1000], 1000, True)

    cols6 = [c for c in range(1, 4) for _ in range(3)]
    rows6 = [r for _ in range(3) for r in range(1, 4)]
    cols6.append(1000)
    rows6.append(1000)
    dump_case(6, 9, cols6, rows6, 3, True)

    dump_case(7, 3, [1, 2, 10, 15, 18], [1, 100, 10, 12, 11], 9, True)

    cells = RNG.sample(range(20 * 20), 16)
    cols8 = [x // 20 + 1 for x in cells]
    rows8 = [x % 20 + 1 for x in cells]
    dump_case(8, 6, cols8, rows8, None, True)

    cells9 = RNG.sample(range(1000 * 1000), 100000)
    cols9 = [x // 1000 + 1 for x in cells9]
    rows9 = [x % 1000 + 1 for x in cells9]
    dump_case(9, 200, cols9, rows9)

    cols10, rows10 = fill_block(99999)
    cols10.append(1000)
    rows10.append(1000)
    dump_case(10, 100000, cols10, rows10, 1000)

    # 用标程重读全部输入，核对输出与换行
    for i in range(1, 11):
        raw_in = (DATA / f"{i}.in").read_bytes()
        raw_out = (DATA / f"{i}.out").read_bytes()
        if raw_in.endswith(b"\n") or raw_in.endswith(b"\r"):
            raise SystemExit(f"{i}.in has trailing newline")
        if not raw_out.endswith(b"\n") or raw_out.endswith(b"\n\n"):
            raise SystemExit(f"{i}.out newline rule failed")
        text = raw_in.decode("utf-8").split("\n")
        if len(text) != 4:
            raise SystemExit(f"{i}.in line count {len(text)}")
        k = int(text[0])
        cols = list(map(int, text[2].split()))
        rows = list(map(int, text[3].split()))
        ans = min_side(k, cols, rows)
        if raw_out.decode("utf-8") != f"{ans}\n":
            raise SystemExit(f"{i}.out mismatch")
    write_config()
    write_readme()
    print("ok")


if __name__ == "__main__":
    main()
