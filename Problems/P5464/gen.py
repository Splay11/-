# -*- coding: utf-8 -*-
"""P5464 加速窗口收益：10 组测例。"""
from __future__ import annotations

import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
from std import max_gain, solve_all  # noqa: E402

DATA = ROOT / "data"
RNG = random.Random(546420260918)


def kadane(v: list[int]) -> int:
    best = cur = v[0]
    for x in v[1:]:
        cur = x if x > cur + x else cur + x
        if cur > best:
            best = cur
    return best


def brute(v: list[int]) -> int:
    n = len(v)
    best = kadane(v)
    for l in range(n):
        s = 0
        for r in range(l, n):
            s += v[r]
            b = v[:]
            for i in range(l, r + 1):
                b[i] *= 2
            got = kadane(b)
            if got > best:
                best = got
    return best


def write_in(path: Path, groups: list[list[int]]) -> None:
    lines = [str(len(groups))]
    for v in groups:
        lines.append(str(len(v)) + " " + " ".join(str(x) for x in v))
    path.write_bytes("\n".join(lines).encode("utf-8"))


def write_out(path: Path, ans: list[int]) -> None:
    path.write_bytes((" ".join(str(x) for x in ans) + "\n").encode("utf-8"))


def dump_case(idx: int, groups: list[list[int]], check_brute: bool = False) -> list[int]:
    ans = solve_all(groups)
    if check_brute:
        for v, a in zip(groups, ans):
            b = brute(v)
            if a != b:
                raise SystemExit(f"brute mismatch case {idx}: {a} vs {b} {v}")
    write_in(DATA / f"{idx}.in", groups)
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
    (ROOT / "config.yaml").write_text(config, encoding="utf-8")


def write_readme() -> None:
    text = """# P5464 测例说明

输入：第一行 $k$，随后 $k$ 行，每行 $m$ 与 $m$ 个 $v_p$。输出一行 $k$ 个答案。`.in` 末尾无换行，`.out` 末尾恰好一个换行。

分层（每组 10 分）：

- 1：四级样例 1。含翻倍得 $8$ 与全负取 $-2$。
- 2：四级样例 2。中间段翻倍得 $12$。
- 3：$m=1$ 正数。
- 4：$m=1$ 负数。卡翻倍后更亏。
- 5：全正。答案是两倍总和。
- 6：全负。答案是最大一项。
- 7：$4,-1,-1,4$。卡「两倍 Kadane」：Kadane 为 $4$，两倍是 $8$，正解把两端一起翻倍得 $12$。
- 8：多组小随机，与 $O(m^3)$ 暴力对拍。
- 9：$m=200000$ 随机。压测。
- 10：$m=200000$ 构造。长负段夹一个大正数，再加「两端正、中间小负」卡只做 Kadane。
"""
    (DATA / "README.md").write_text(text, encoding="utf-8")


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    dump_case(1, [[2, -3, 4, -1], [-5, -2, -7]], True)
    dump_case(2, [[1, 2, -5, 3, -1, 4]], True)
    dump_case(3, [[9]], True)
    dump_case(4, [[-8]], True)
    dump_case(5, [[1, 2, 3, 4]], True)
    dump_case(6, [[-9, -4, -7, -1, -3]], True)
    dump_case(7, [[4, -1, -1, 4], [5, -10, 5, 5], [10, -3, 10]], True)

    groups8 = []
    for _ in range(8):
        m = RNG.randint(1, 25)
        groups8.append([RNG.randint(-20, 20) for _ in range(m)])
    dump_case(8, groups8, True)

    dump_case(9, [[RNG.randint(-10**9, 10**9) for _ in range(200000)]])

    big = [-1] * 100000 + [10**9] + [-1] * 99999
    bridge = [10**8] + [-1] * 10 + [10**8]
    dump_case(10, [big[:199988], bridge])

    write_config()
    write_readme()
    print("ok")


if __name__ == "__main__":
    main()
