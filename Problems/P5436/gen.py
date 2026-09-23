# -*- coding: utf-8 -*-
"""P5436 卡槽满载：10 组测例（四级 I/O：fin,beg 逗号分隔，答案两行）。"""
from __future__ import annotations

import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
from std import min_cards_and_full_load  # noqa: E402

DATA = ROOT / "data"
RNG = random.Random(543620260913)


def brute(segs: list[tuple[int, int]]) -> tuple[int, int]:
    pts = sorted({s for s, e in segs} | {e for s, e in segs})
    mx = 0
    total = 0
    for i in range(len(pts) - 1):
        mid_l, mid_r = pts[i], pts[i + 1]
        cur = 0
        for s, e in segs:
            if s <= mid_l and e > mid_l:
                cur += 1
        if cur > mx:
            mx = cur
    for i in range(len(pts) - 1):
        mid_l, mid_r = pts[i], pts[i + 1]
        cur = 0
        for s, e in segs:
            if s <= mid_l and e > mid_l:
                cur += 1
        if cur == mx:
            total += mid_r - mid_l
    return mx, total


def write_in(path: Path, text: str) -> None:
    if text.endswith("\n"):
        text = text[:-1]
    path.write_bytes(text.encode("utf-8"))


def write_out(path: Path, k: int, dur: int) -> None:
    path.write_bytes(f"{k}\n{dur}\n".encode("utf-8"))


def fmt_case(segs: list[tuple[int, int]]) -> str:
    lines = [str(len(segs))]
    for beg, fin in segs:
        lines.append(f"{fin},{beg}")
    return "\n".join(lines)


def write_config() -> None:
    cases = "\n".join(
        f"      - input: {i}.in\n        output: {i}.out" for i in range(1, 11)
    )
    config = f"""type: default
time: 1s
memory: 256m
subtasks:
  - score: 100
    if: []
    id: 1
    type: sum
    cases:
{cases}
langs:
  - cc.cc14o2
  - cc
  - java
  - py.py3
  - py
"""
    (DATA / "config.yaml").write_text(config, encoding="utf-8")
    (ROOT / "config.yaml").write_text(config, encoding="utf-8")


def write_readme() -> None:
    text = """# P5436 测例说明

四级输入：首行 $m$，随后每行 `结束时刻,开始时刻`。输出两行：最少卡数、满载累计时长。
`.in` 末行后无换行；`.out` 两个整数两行，文件末恰有一个换行。

分层（每组 10 分）：

- 1：四级样例 1。交错重叠，答案 `2` / `10`。卡把首尾相接当成冲突。
- 2：四级样例 2。三段互不相交，答案 `1` / `4`。
- 3：四级样例 3。三重叠，答案 `3` / `4`。
- 4：基础。单区间 $[3,11)$，答案 `1` / `8`。
- 5：构造全包含。卡只统计点数或闭区间。
- 6：若干互不相交区间。
- 7：hack。首尾相接的链，同一时刻必须先结束再开始，正确最大占用为 $1$。
- 8：小随机，与暴力对拍。
- 9：大数据 $m=200000$ 随机。
- 10：大数据构造高峰：大量区间叠在同一段上，压测扫描线。

hack 点：闭区间把相接点算冲突、同一时刻先加后减、把所有区间长度之和当成满载时长。
"""
    (DATA / "README.md").write_text(text, encoding="utf-8")


def random_segs(n: int, tmax: int) -> list[tuple[int, int]]:
    segs: list[tuple[int, int]] = []
    for _ in range(n):
        a = RNG.randint(0, tmax - 1)
        b = RNG.randint(a + 1, tmax)
        segs.append((a, b))
    return segs


def make_cases() -> list[list[tuple[int, int]]]:
    cases: list[list[tuple[int, int]]] = []
    # 1-3 样例
    cases.append([(0, 10), (5, 15), (10, 20), (25, 30)])
    cases.append([(1, 2), (4, 6), (8, 9)])
    cases.append([(0, 8), (1, 7), (2, 6)])
    # 4 单区间
    cases.append([(3, 11)])
    # 5 全包含
    cases.append([(0, 100), (10, 90), (20, 80), (30, 70)])
    # 6 不相交
    cases.append([(0, 5), (10, 12), (20, 27), (40, 41)])
    # 7 相接链
    cases.append([(10, 20), (20, 30), (30, 40), (40, 55)])
    # 8 小随机
    cases.append(random_segs(12, 50))
    # 9 满规模随机
    cases.append(random_segs(200000, 10**9))
    # 10 高峰：一半完全覆盖 [0, 10^6)，其余散落
    n = 200000
    peak = [(0, 10**6) for _ in range(n // 2)]
    rest = random_segs(n - n // 2, 10**9)
    cases.append(peak + rest)
    return cases


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    cases = make_cases()
    assert len(cases) == 10

    for _ in range(40):
        segs = random_segs(RNG.randint(1, 8), 20)
        a = min_cards_and_full_load(segs)
        b = brute(segs)
        if a != b:
            raise SystemExit(f"对拍失败 {segs} dp={a} brute={b}")

    for i, segs in enumerate(cases, 1):
        for beg, fin in segs:
            if not (0 <= beg < fin <= 10**9):
                raise SystemExit(f"非法区间 case {i}: {beg} {fin}")
        k, dur = min_cards_and_full_load(segs)
        if len(segs) <= 20:
            bk, bd = brute(segs)
            if (bk, bd) != (k, dur):
                raise SystemExit(f"自校验失败 {i}: {k,dur} vs brute {bk,bd}")
        raw = fmt_case(segs)
        write_in(DATA / f"{i}.in", raw)
        write_out(DATA / f"{i}.out", k, dur)
        print(i, "m=", len(segs), "->", k, dur)

    write_config()
    write_readme()
    print("generated 10 cases")


if __name__ == "__main__":
    main()
