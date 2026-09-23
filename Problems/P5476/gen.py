# -*- coding: utf-8 -*-
"""P5476 四因子乘积对：10 组测例。"""
from __future__ import annotations

import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
from std import count_pairs  # noqa: E402

DATA = ROOT / "data"
RNG = random.Random(547620260919)


def n_div(x: int) -> int:
    c = 0
    i = 1
    while i * i <= x:
        if x % i == 0:
            c += 1 if i * i == x else 2
        i += 1
    return c


def brute(vals: list[int]) -> int:
    ans = 0
    n = len(vals)
    for i in range(n):
        for j in range(i + 1, n):
            if n_div(vals[i] * vals[j]) == 4:
                ans += 1
    return ans


def write_in(path: Path, vals: list[int]) -> None:
    text = str(len(vals)) + " " + " ".join(str(x) for x in vals)
    path.write_bytes(text.encode("utf-8"))


def write_out(path: Path, ans: int) -> None:
    path.write_bytes((str(ans) + "\n").encode("utf-8"))


def dump_case(idx: int, vals: list[int], check_brute: bool = False) -> None:
    ans = count_pairs(vals)
    if check_brute:
        b = brute(vals)
        if ans != b:
            raise SystemExit(f"brute mismatch case {idx}: {ans} vs {b} {vals}")
    write_in(DATA / f"{idx}.in", vals)
    write_out(DATA / f"{idx}.out", ans)


def write_config() -> None:
    cases = "\n".join(
        f"      - input: {i}.in\n        output: {i}.out" for i in range(1, 11)
    )
    config = f"""type: default
time: 8s
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
    text = """# P5476 测例说明

输入：一行 $m$ 与 $m$ 个指纹。输出一个整数。`.in` 末尾无换行，`.out` 末尾恰好一个换行。

分层（每组 10 分）：

- 1：四级样例 1。含 $1$ 配 $pq$、$p$ 配 $q$、$p$ 配 $p^{2}$。
- 2：四级样例 2。重复的 $p^{2}$ 与质数。
- 3：$m=1$，答案 $0$。
- 4：全是 $1$。$1\\times 1$ 只有一个因子。
- 5：同一个质数重复。卡「任意两个质数都算」。
- 6：大量 $1$ 配 $6$、$8$；同时有不该配上的 $4$、$12$。
- 7：小随机，与 $O(m^{2})$ 数因子暴力对拍。
- 8：小数据极值。含 $1$、$p^{3}$、半质数、无关合数。
- 9：$m=100000$ 随机。卡两两枚举。
- 10：$50000$ 个 $2$ 和 $50000$ 个 $3$。答案 $2.5\\times 10^{9}$，卡 `int` 溢出。
"""
    (DATA / "README.md").write_text(text, encoding="utf-8")


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    dump_case(1, [6, 2, 3, 9, 1], True)
    dump_case(2, [4, 4, 2, 7], True)
    dump_case(3, [12], True)
    dump_case(4, [1, 1, 1, 1], True)
    dump_case(5, [5, 5, 5, 5, 5], True)
    dump_case(6, [1, 1, 6, 8, 4, 12, 2], True)
    dump_case(7, [RNG.randint(1, 80) for _ in range(35)], True)
    dump_case(8, [1, 8, 27, 6, 15, 4, 9, 30, 16, 7], True)
    dump_case(9, [RNG.randint(1, 10**6) for _ in range(100000)])
    dump_case(10, [2] * 50000 + [3] * 50000)
    write_config()
    write_readme()
    print("ok")


if __name__ == "__main__":
    main()
