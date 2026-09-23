# -*- coding: utf-8 -*-
"""P5473 主题积压清零：10 组测例。"""
from __future__ import annotations

import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
from std import min_starts  # noqa: E402

DATA = ROOT / "data"
RNG = random.Random(547320260919)


def write_in(path: Path, p: int, q: int, w: list[int]) -> None:
    lines = [str(len(w)), f"{p} {q}", " ".join(str(x) for x in w)]
    path.write_bytes("\n".join(lines).encode("utf-8"))


def write_out(path: Path, ans: int) -> None:
    path.write_bytes(f"{ans}\n".encode("utf-8"))


def dump(idx: int, p: int, q: int, w: list[int]) -> None:
    write_in(DATA / f"{idx}.in", p, q, w)
    write_out(DATA / f"{idx}.out", min_starts(w, p, q))


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
    text = """# P5473 测例说明

输入三行：$m$，然后 $p\\ q$，然后 $m$ 个 $w_i$。输出最少次数。`.in` 末尾无换行，`.out` 末尾恰好一个换行。

分层（每组 10 分）：

- 1：四级样例 1。三台，答案 $3$。
- 2：四级样例 2。单台，答案 $3$。
- 3：全部积压相同。
- 4：$p=q+1$，差额极小。
- 5：一条积压特别大，其余很小。
- 6：答案贴近只靠顺带消费的上界。
- 7：随机小数据。
- 8：$m=200$，中等。
- 9：$m=10^5$ 随机压测。
- 10：$m=10^5$ 且 $w_i$ 接近上限，卡 `int` 溢出。

hack 点：每轮点当前积压最大、`int` 乘爆、二分下界忘记上取整。
"""
    (DATA / "README.md").write_text(text, encoding="utf-8")


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)

    dump(1, 10, 3, [15, 8, 4])
    dump(2, 5, 1, [12])
    dump(3, 4, 2, [10, 10, 10])
    dump(4, 3, 2, [9, 6, 5, 4, 1])
    dump(5, 100, 1, [500, 3, 3, 3, 2])
    dump(6, 7, 6, [20, 19, 18, 17])
    dump(7, 9, 4, [RNG.randint(1, 50) for _ in range(8)])
    dump(8, 1000, 37, [RNG.randint(1, 10000) for _ in range(200)])
    dump(9, 10**9 - 5, 10**6, [RNG.randint(1, 10**9) for _ in range(100000)])
    dump(10, 10**9, 10**9 - 1, [10**9] * 100000)

    write_config()
    write_readme()
    print("generated 10 cases")


if __name__ == "__main__":
    main()
