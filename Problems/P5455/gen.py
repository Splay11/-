# -*- coding: utf-8 -*-
"""P5455 推理设备覆盖：10 组测例（首行 d w t，随后 d 行各 w 个数，末行 t 个数）。"""
from __future__ import annotations

import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
from std import min_devices  # noqa: E402

DATA = ROOT / "data"
RNG = random.Random(545520260916)


def write_in(path: Path, specs: list[list[int]], need: list[int]) -> None:
    d = len(specs)
    w = len(specs[0])
    t = len(need)
    lines = [f"{d} {w} {t}"]
    for row in specs:
        lines.append(" ".join(str(x) for x in row))
    lines.append(" ".join(str(x) for x in need))
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
    text = """# P5455 测例说明

输入：第一行 $d,w,t$，随后 $d$ 行每行 $w$ 个条目编号，末行 $t$ 个业务条目。输出：最少台数，无解为 $0$。`.in` 末尾无换行，`.out` 末尾恰好一个换行。

分层（每组 10 分）：

- 1：二级样例 1。四台、业务三条，最优 $2$。
- 2：二级样例 2。业务条目与机器完全不相交，答案 $0$。卡无解输出 $-1$。
- 3：二级样例 3。单条业务、两台都能提供，答案 $1$。
- 4：贪心反例。大集合先拿会变成 $3$ 台，最优 $2$ 台。
- 5：稀疏编号 $100,200,300$。卡把条目当成 $1..t$。
- 6：一台机器覆盖全部业务。答案 $1$。
- 7：$d=8$ 随机小数据，可与 $O(2^d)$ 对拍。
- 8：缺一条业务条目，答案 $0$。
- 9：上限 $d=30,t=20$ 随机。压测 $O(d\\cdot 2^t)$，卡 $O(2^d)$。
- 10：上限构造：每台只覆盖一个业务比特，答案接近 $t$。

hack 点：贪心多选、无解写 $-1$、编号不从 $1$ 起、$O(2^d)$、重复条目。
"""
    (DATA / "README.md").write_text(text, encoding="utf-8")


def covers_of(specs: list[list[int]], need: list[int]) -> list[int]:
    bit = {x: i for i, x in enumerate(need)}
    out = []
    for row in specs:
        mask = 0
        for x in row:
            if x in bit:
                mask |= 1 << bit[x]
        out.append(mask)
    return out


def brute(covers: list[int], t: int) -> int:
    full = (1 << t) - 1
    d = len(covers)
    best = t + 5
    for mask in range(1 << d):
        s = 0
        cnt = 0
        for i in range(d):
            if (mask >> i) & 1:
                s |= covers[i]
                cnt += 1
        if s == full:
            best = min(best, cnt)
    return 0 if best >= t + 5 else best


def rand_row(rng: random.Random, w: int, lo: int, hi: int) -> list[int]:
    return [rng.randint(lo, hi) for _ in range(w)]


def pad(row: list[int], w: int, filler: int) -> list[int]:
    row = list(row)
    while len(row) < w:
        row.append(filler)
    return row[:w]


def validate(idx: int, specs: list[list[int]], need: list[int]) -> None:
    d = len(specs)
    w = len(specs[0])
    t = len(need)
    if not (1 <= d <= 30 and 1 <= w <= 10 and 1 <= t <= 20):
        raise RuntimeError(f"case {idx}: bad d/w/t")
    if any(len(row) != w for row in specs):
        raise RuntimeError(f"case {idx}: ragged specs")
    if len(set(need)) != t:
        raise RuntimeError(f"case {idx}: need not unique")


def make_cases() -> list[tuple[list[list[int]], list[int]]]:
    cases: list[tuple[list[list[int]], list[int]]] = []
    # 1 样例1
    cases.append(([[2, 8], [3, 5], [8, 9], [5, 2]], [2, 5, 8]))
    # 2 样例2
    cases.append(([[1, 2, 3], [4, 5, 6]], [10, 11, 12, 13]))
    # 3 样例3
    cases.append(([[9], [8], [9]], [9]))
    # 4 贪心反例：先拿大集合会变成 3，最优 2
    cases.append(([[1, 2, 3, 4], [1, 2, 5, 7], [3, 4, 6, 8]], [1, 2, 3, 4, 5, 6]))
    # 5 稀疏编号
    cases.append(([[100, 200], [200, 400], [100, 300]], [100, 200, 300]))
    # 6 单台覆盖全部
    cases.append(([[5, 6, 7, 8], [1, 2, 3, 4], [9, 9, 9, 9]], [1, 2, 3, 4]))
    # 7 小随机，可暴力对拍
    specs7 = [rand_row(RNG, 3, 1, 8) for _ in range(8)]
    need7 = list(range(1, 7))
    cases.append((specs7, need7))
    # 8 缺一条
    cases.append(([[1, 2, 3], [2, 3, 4], [3, 4, 1]], [1, 2, 3, 4, 99]))
    # 9 上限随机
    specs9 = [rand_row(RNG, 10, 1, 40) for _ in range(30)]
    need9 = list(range(1, 21))
    cases.append((specs9, need9))
    # 10 上限：每台覆盖一个业务比特，另加干扰编号
    need10 = list(range(101, 121))
    specs10 = []
    for i in range(20):
        specs10.append(pad([need10[i]], 10, 7))
    for i in range(10):
        specs10.append(rand_row(RNG, 10, 1, 50))
    cases.append((specs10, need10))
    return cases


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    cases = make_cases()
    assert len(cases) == 10
    for i, (specs, need) in enumerate(cases, 1):
        validate(i, specs, need)
        ans = min_devices(specs, need)
        if len(specs) <= 12:
            b = brute(covers_of(specs, need), len(need))
            if b != ans:
                raise SystemExit(f"case {i}: 与暴力不一致 {ans} vs {b}")
        write_in(DATA / f"{i}.in", specs, need)
        write_out(DATA / f"{i}.out", ans)
        if min_devices(specs, need) != ans:
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
    for i, (specs, need) in enumerate(cases, 1):
        print(i, "d", len(specs), "t", len(need), "ans", min_devices(specs, need))


if __name__ == "__main__":
    main()
