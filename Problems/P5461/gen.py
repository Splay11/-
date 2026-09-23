# -*- coding: utf-8 -*-
"""P5461 异或区间右端：10 组测例（第一行 w，第二行 p）。"""
from __future__ import annotations

import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
from std import min_right  # noqa: E402

DATA = ROOT / "data"
RNG = random.Random(546120260918)
LIM = 1048576


def write_in(path: Path, w: int, p: int) -> None:
    path.write_bytes(f"{w}\n{p}".encode("utf-8"))


def write_out(path: Path, ans: int) -> None:
    path.write_bytes(f"{ans}\n".encode("utf-8"))


def dump_case(idx: int, w: int, p: int) -> None:
    assert 0 <= w < LIM and 0 <= p < LIM
    write_in(DATA / f"{idx}.in", w, p)
    write_out(DATA / f"{idx}.out", min_right(p, w))


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
    text = """# P5461 测例说明

输入：第一行 $w$，第二行 $p$。输出：最小右端 $q$，无解 $-1$。`.in` 末尾无换行，`.out` 末尾恰好一个换行。

分层（每组 10 分）：

- 1：四级样例 1。$w=1,p=2$，答案 $3$。
- 2：四级样例 2。无解，答案 $-1$。卡漏掉无解。
- 3：$p=w=0$，答案 $0$。卡把 $0$ 当空区间。
- 4：$need=0$ 且 $p>0$，答案落到最近的 $q\\equiv 3\\pmod 4$。
- 5：$need=1$，答案落到最近的 $q\\equiv 1\\pmod 4$。
- 6：唯一候选 $q=need$ 但 $q<p$，答案 $-1$。
- 7：唯一候选 $q=need-1$ 且合法。
- 8：随机中等数据。
- 9：上限附近有解。
- 10：上限附近无解。

hack 点：漏无解、不取最小 $q$、误加上界 $1048575$、$need=0/1$ 只检查单个候选。
"""
    (DATA / "README.md").write_text(text, encoding="utf-8")


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)

    dump_case(1, 1, 2)
    dump_case(2, 2, 5)
    dump_case(3, 0, 0)
    dump_case(4, 0, 100)
    dump_case(5, 1, 8)
    dump_case(6, 4, 8)
    dump_case(7, 3, 1)
    dump_case(8, RNG.randrange(LIM), RNG.randrange(LIM))
    dump_case(9, LIM - 1, 0)
    dump_case(10, 2, LIM - 1)

    write_config()
    write_readme()
    print("generated 10 cases")


if __name__ == "__main__":
    main()
