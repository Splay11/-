# -*- coding: utf-8 -*-
"""P5462 数位积最小码：10 组测例。"""
from __future__ import annotations

import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
from std import solve_all  # noqa: E402

DATA = ROOT / "data"
RNG = random.Random(546220260918)


def write_in(path: Path, ws: list[int]) -> None:
    lines = [str(len(ws)), " ".join(str(x) for x in ws)]
    path.write_bytes("\n".join(lines).encode("utf-8"))


def write_out(path: Path, ans: list[int]) -> None:
    path.write_bytes((" ".join(str(x) for x in ans) + "\n").encode("utf-8"))


def dump_case(idx: int, ws: list[int]) -> list[int]:
    ans = solve_all(ws)
    write_in(DATA / f"{idx}.in", ws)
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


def write_readme(preview: dict[int, list[int]]) -> None:
    text = """# P5462 测例说明

输入：第一行 $q$，第二行 $q$ 个 $w$。输出一行 $q$ 个答案，空格分隔。`.in` 末尾无换行，`.out` 末尾恰好一个换行。

分层（每组 10 分）：

- 1：四级样例 1。覆盖一位、两位、十一位和为 $1$、普通三位。
- 2：四级样例 2。含 $-1$ 与上界 $10^{16}$。
- 3：最小询问 $q=1,w=1$。
- 4：$w=1..9$，全是一位数本身。
- 5：质数分支。$19,23,29,31$ 应 $-1$；$11,13,17$ 走「和为 $1$ 的长编号」。
- 6：构造方向。卡把余数堆到左边（如 $20$ 应是 $19$ 不是 $91$）。
- 7：上界附近与最大 $w=2500$（无解），以及 $L=16$ 的合法构造。
- 8：小规模随机。
- 9：$q=50000$ 均匀随机。压测 I/O。
- 10：$q=50000$ 混入大量 $17$、$2500$ 与质数。卡漏 $17$ 位、卡质数一律判 $-1$。
"""
    extra = "\n生成答案预览：\n" + "\n".join(
        f"- {i}：{preview[i][:8]}{'...' if len(preview[i])>8 else ''}" for i in range(1, 11)
    ) + "\n"
    (DATA / "README.md").write_text(text + extra, encoding="utf-8")


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    preview: dict[int, list[int]] = {}

    preview[1] = dump_case(1, [1, 10, 11, 27, 16])
    preview[2] = dump_case(2, [8, 29, 17])
    preview[3] = dump_case(3, [1])
    preview[4] = dump_case(4, list(range(1, 10)))
    preview[5] = dump_case(5, [19, 23, 29, 31, 11, 13, 17])
    preview[6] = dump_case(6, [10, 12, 14, 18, 20, 24, 27, 30])
    preview[7] = dump_case(7, [2500, 2499, 144, 160, 17, 16])
    preview[8] = dump_case(8, [RNG.randint(1, 2500) for _ in range(30)])
    preview[9] = dump_case(9, [RNG.randint(1, 2500) for _ in range(50000)])

    mix = []
    for i in range(50000):
        r = RNG.randrange(10)
        if r == 0:
            mix.append(17)
        elif r == 1:
            mix.append(2500)
        elif r == 2:
            mix.append(RNG.choice([19, 23, 29, 31]))
        else:
            mix.append(RNG.randint(1, 2500))
    preview[10] = dump_case(10, mix)

    write_config()
    write_readme(preview)
    print("preview", {k: (v if len(v) <= 10 else v[:6] + ["..."]) for k, v in preview.items()})


if __name__ == "__main__":
    main()
