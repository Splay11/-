# -*- coding: utf-8 -*-
"""P5454 雷达等距计数：10 组测例（首行 m，随后 m 行坐标）。"""
from __future__ import annotations

import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
from std import count_equidistant  # noqa: E402

DATA = ROOT / "data"
RNG = random.Random(545420260916)


def write_in(path: Path, pts: list[tuple[int, int]]) -> None:
    lines = [str(len(pts))]
    for x, y in pts:
        lines.append(f"{x} {y}")
    path.write_bytes("\n".join(lines).encode("utf-8"))


def write_out(path: Path, ans: int) -> None:
    path.write_bytes(f"{ans}\n".encode("utf-8"))


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
    (DATA / "config.yaml").write_text(config, encoding="utf-8")
    (ROOT / "config.yaml").write_text(config, encoding="utf-8")


def write_readme() -> None:
    text = """# P5454 测例说明

输入：第一行 $m$，随后 $m$ 行每行两个整数 $u_p\\ v_p$。输出：一个整数（等心探测组数）。`.in` 末尾无换行，`.out` 末尾恰好一个换行。

分层（每组 10 分）：

- 1：二级样例 1。边长 $3$ 的正方形，答案 $8$。
- 2：二级样例 2。等腰三角形，答案 $2$。卡「只计组合不计排列」会得到 $1$。
- 3：答案为 $0$。$3\\times 4$ 矩形，每个顶点到另外三点距离 $3,4,5$ 全不同。
- 4：三点共线等距。卡浮点比距离、漏计 $(p,r,q)$。
- 5：正方形加中心。中心到四顶点距离相同，卡大桶 $P(c,2)$ 与 $C(c,2)$。
- 6：坐标取到 $\\pm 10^5$。平方距离超 `int` 范围，卡 `dx*dx` 溢出。
- 7：$3\\times 3$ 网格。结构化等距，可与 $O(m^3)$ 暴力对拍。
- 8：随机 $m=50$，坐标在 $[-25,25]$。中等随机且有重复距离。
- 9：上限 $m=2000$，多数点落在 $[-400,400]$，并掺极值坐标。压测 $O(m^2)$，卡 $O(m^3)$。
- 10：上限 $40\\times 50$ 网格。大量重复距离 + 满规模。

hack 点：有序/无序计错、`int` 平方溢出、浮点误差、$O(m^3)$、答案为 $0$、极值坐标。
"""
    (DATA / "README.md").write_text(text, encoding="utf-8")


def unique_random(rng: random.Random, m: int, lo: int, hi: int) -> list[tuple[int, int]]:
    seen: set[tuple[int, int]] = set()
    pts: list[tuple[int, int]] = []
    while len(pts) < m:
        x = rng.randint(lo, hi)
        y = rng.randint(lo, hi)
        if (x, y) not in seen:
            seen.add((x, y))
            pts.append((x, y))
    return pts


def grid(w: int, h: int, ox: int = 0, oy: int = 0, step: int = 1) -> list[tuple[int, int]]:
    return [(ox + i * step, oy + j * step) for i in range(w) for j in range(h)]


def validate(idx: int, pts: list[tuple[int, int]]) -> None:
    m = len(pts)
    if not (3 <= m <= 2000):
        raise RuntimeError(f"case {idx}: bad m={m}")
    seen = set()
    for x, y in pts:
        if not (-100000 <= x <= 100000 and -100000 <= y <= 100000):
            raise RuntimeError(f"case {idx}: coord out of range {(x, y)}")
        if (x, y) in seen:
            raise RuntimeError(f"case {idx}: duplicate {(x, y)}")
        seen.add((x, y))


def brute(pts: list[tuple[int, int]]) -> int:
    m = len(pts)
    ans = 0
    for p in range(m):
        for q in range(m):
            if q == p:
                continue
            dx1 = pts[q][0] - pts[p][0]
            dy1 = pts[q][1] - pts[p][1]
            d1 = dx1 * dx1 + dy1 * dy1
            for r in range(m):
                if r == p or r == q:
                    continue
                dx2 = pts[r][0] - pts[p][0]
                dy2 = pts[r][1] - pts[p][1]
                if dx2 * dx2 + dy2 * dy2 == d1:
                    ans += 1
    return ans


def make_cases() -> list[list[tuple[int, int]]]:
    cases: list[list[tuple[int, int]]] = []
    # 1 样例1：正方形
    cases.append([(0, 0), (0, 3), (3, 0), (3, 3)])
    # 2 样例2：等腰三角形
    cases.append([(0, 0), (4, 0), (2, 3)])
    # 3 答案 0：3-4-5 矩形
    cases.append([(0, 0), (3, 0), (0, 4), (3, 4)])
    # 4 三点共线等距
    cases.append([(1, 2), (4, 2), (7, 2)])
    # 5 正方形 + 中心
    cases.append([(0, 0), (2, 0), (0, 2), (2, 2), (1, 1)])
    # 6 极值坐标，卡 int 平方溢出
    cases.append(
        [
            (0, 0),
            (100000, 0),
            (0, 100000),
            (-100000, 0),
            (0, -100000),
            (100000, 100000),
            (-100000, -100000),
        ]
    )
    # 7 3x3 网格
    cases.append(grid(3, 3, ox=-1, oy=-1))
    # 8 随机小数据：值域收紧，容易出现重复距离
    cases.append(unique_random(RNG, 50, -25, 25))
    # 9 上限随机：落在较小格子里，容易出现重复距离，并掺若干极值点
    pts9 = unique_random(RNG, 1990, -400, 400)
    extra = unique_random(RNG, 10, -100000, 100000)
    seen9 = set(pts9)
    for p in extra:
        if p not in seen9 and len(pts9) < 2000:
            seen9.add(p)
            pts9.append(p)
    while len(pts9) < 2000:
        x = RNG.randint(-400, 400)
        y = RNG.randint(-400, 400)
        if (x, y) not in seen9:
            seen9.add((x, y))
            pts9.append((x, y))
    cases.append(pts9)
    # 10 上限网格
    cases.append(grid(40, 50, ox=-20, oy=-25))
    return cases


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    cases = make_cases()
    assert len(cases) == 10
    for i, pts in enumerate(cases, 1):
        validate(i, pts)
        ans = count_equidistant(pts)
        if len(pts) <= 80:
            brute_ans = brute(pts)
            if brute_ans != ans:
                raise SystemExit(f"case {i}: 与暴力不一致 {ans} vs {brute_ans}")
        write_in(DATA / f"{i}.in", pts)
        write_out(DATA / f"{i}.out", ans)
        got = count_equidistant(pts)
        if got != ans:
            raise SystemExit(f"自校验失败：{i}")
        raw_in = (DATA / f"{i}.in").read_bytes()
        raw_out = (DATA / f"{i}.out").read_bytes()
        if raw_in.endswith(b"\n"):
            raise SystemExit(f"case {i}: .in 末尾有换行")
        if not raw_out.endswith(b"\n") or raw_out.endswith(b"\n\n"):
            raise SystemExit(f"case {i}: .out 换行不符合约定")
    write_config()
    write_readme()
    print("generated 10 cases")
    for i, pts in enumerate(cases, 1):
        print(i, "m", len(pts), "ans", count_equidistant(pts))


if __name__ == "__main__":
    main()
