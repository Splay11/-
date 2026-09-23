# -*- coding: utf-8 -*-
"""P5429 无冲突组题：10 组测例（二级 I/O：首行五个整数，次行 m 个负荷）。"""
from __future__ import annotations

import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
from std import collect_schemes  # noqa: E402

DATA = ROOT / "data"
RNG = random.Random(542920260911)


def format_out(count: int, top: list[list[int]]) -> str:
    lines = [str(count)]
    for scheme in top:
        lines.append(" ".join(str(x) for x in scheme))
    return "\n".join(lines) + "\n"


def write_in(path: Path, m: int, t: int, g: int, lo: int, hi: int, w: list[int]) -> None:
    text = f"{m} {t} {g} {lo} {hi}\n" + " ".join(str(x) for x in w)
    path.write_bytes(text.encode("utf-8"))


def write_out(path: Path, count: int, top: list[list[int]]) -> None:
    path.write_bytes(format_out(count, top).encode("utf-8"))


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
    text = """# P5429 测例说明

输入：第一行 $m,t,g,lo,hi$，第二行 $m$ 个负荷。输出：方案总数；若大于 $0$，再按字典序至多 $3$ 行方案（编号空格分隔）。`.in` 末尾无换行，`.out` 末尾恰好一个换行。

分层（每组 10 分）：

- 1：二级样例。$m=6,t=3,g=1,[8,16]$。卡间隔合法但负荷过低的 $(2,4,6)$。
- 2：$t=1$。没有相邻对，只按单点负荷过滤。卡「$t=1$ 仍去做冲突判断」。
- 3：$g=0$，全部 $C(5,2)=10$ 都合法，只打印前 3 份。卡「$g=0$ 仍禁止相邻编号」以及漏计总数。
- 4：答案为 $0$。$t=3,g=2,m=4$ 塞不下。卡强行输出空方案行。
- 5：负荷和恰为下限/上限才算。卡开区间 $[lo,hi]$ 或漏掉边界。
- 6：$t=m$ 且 $g=0$，唯一全选方案，和恰好在区间内。
- 7：$t=m$ 且 $g=1$，相邻编号必冲突，答案 $0$。
- 8：差恰好等于 $g$ 的对应判非法。卡把 $\\le g$ 写成 $< g$。
- 9：$m=20,t=10,g=1$，随机负荷。中等组合数 + 和过滤。
- 10：$m=20,t=10,g=0$，负荷全 $1$，和恒合法。$C(20,10)=184756$，压测计数与只输出前 3 份。

hack 点：冲突 off-by-one、$g=0$、$t=1$、总数大于 3 却只计 3、开区间负荷、输出全部方案。
"""
    (DATA / "README.md").write_text(text, encoding="utf-8")


def make_cases() -> list[tuple[int, int, int, int, int, list[int]]]:
    cases: list[tuple[int, int, int, int, int, list[int]]] = []
    # 1 样例
    cases.append((6, 3, 1, 8, 16, [4, 2, 5, 3, 6, 1]))
    # 2 t=1
    cases.append((5, 1, 2, 3, 5, [2, 4, 6, 3, 1]))
    # 3 g=0 全部合法，count>3
    cases.append((5, 2, 0, 1, 100, [1, 1, 1, 1, 1]))
    # 4 零方案
    cases.append((4, 3, 2, 1, 100, [1, 2, 3, 4]))
    # 5 和恰为边界
    cases.append((4, 2, 0, 10, 10, [5, 5, 6, 4]))
    # 6 全选合法
    cases.append((3, 3, 0, 6, 6, [1, 2, 3]))
    # 7 全选但 g=1 冲突
    cases.append((3, 3, 1, 1, 100, [1, 2, 3]))
    # 8 差==g 非法：g=2 时 (1,3) 差为 2 应排除
    cases.append((6, 2, 2, 1, 200, [10, 10, 10, 10, 10, 10]))
    # 9 上限规模 + 间隔 + 随机负荷
    w9 = [RNG.randint(1, 100) for _ in range(20)]
    cases.append((20, 10, 1, 200, 600, w9))
    # 10 满组合压测
    cases.append((20, 10, 0, 1, 1000, [1] * 20))
    return cases


def validate_case(idx: int, m: int, t: int, g: int, lo: int, hi: int, w: list[int]) -> None:
    if not (1 <= m <= 20):
        raise RuntimeError(f"case {idx}: bad m")
    if not (1 <= t <= m):
        raise RuntimeError(f"case {idx}: bad t")
    if not (0 <= g <= m):
        raise RuntimeError(f"case {idx}: bad g")
    if not (1 <= lo <= hi <= 1000):
        raise RuntimeError(f"case {idx}: bad lo/hi")
    if len(w) != m or any(not (1 <= x <= 100) for x in w):
        raise RuntimeError(f"case {idx}: bad w")


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    cases = make_cases()
    assert len(cases) == 10
    for i, (m, t, g, lo, hi, w) in enumerate(cases, 1):
        validate_case(i, m, t, g, lo, hi, w)
        count, top = collect_schemes(m, t, g, lo, hi, w)
        write_in(DATA / f"{i}.in", m, t, g, lo, hi, w)
        write_out(DATA / f"{i}.out", count, top)
        got_c, got_top = collect_schemes(m, t, g, lo, hi, w)
        if (got_c, got_top) != (count, top):
            raise SystemExit(f"自校验失败：{i}")
        if count == 0 and top:
            raise SystemExit(f"case {i}: count=0 但仍有方案")
        if count > 0 and not top:
            raise SystemExit(f"case {i}: count>0 但未输出方案")
        if len(top) != min(3, count):
            raise SystemExit(f"case {i}: 前三份数量不对")
    write_config()
    write_readme()
    print("generated 10 cases")
    for i, (m, t, g, lo, hi, w) in enumerate(cases, 1):
        count, top = collect_schemes(m, t, g, lo, hi, w)
        print(i, f"m={m} t={t} g={g}", "count", count, "top", top[:1])


if __name__ == "__main__":
    main()
