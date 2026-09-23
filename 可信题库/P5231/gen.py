# -*- coding: utf-8 -*-
"""P5231 造数：定宽字段紧凑拼装为十六进制。"""
from __future__ import annotations

import random
from pathlib import Path
from typing import List, Tuple

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
RNG = random.Random(5231)


def pack_fields(section_width: List[int], section_values: List[int]) -> str:
    acc = 0
    total = 0
    for w, v in zip(section_width, section_values):
        acc = (acc << w) | v
        total += w
    pad = (8 - total % 8) % 8
    acc <<= pad
    total += pad
    nbytes = total // 8
    return f"{acc:0{nbytes * 2}X}"


def fmt_arr(a: List[int]) -> str:
    return "[" + ", ".join(str(x) for x in a) + "]"


def write_pair(idx: int, widths: List[int], values: List[int]) -> None:
    assert len(widths) == len(values)
    assert 1 <= len(widths) <= 10
    total = sum(widths)
    assert total <= 48
    for w, v in zip(widths, values):
        assert 1 <= w <= 31
        assert 0 <= v < (1 << w)
    text_in = fmt_arr(widths) + "\n" + fmt_arr(values)
    # .in 末尾无多余换行
    (DATA / f"{idx}.in").write_bytes(text_in.encode("utf-8"))
    out = '"' + pack_fields(widths, values) + '"\n'
    with open(DATA / f"{idx}.out", "w", encoding="utf-8", newline="\n") as f:
        f.write(out)


def rand_case(n: int, max_sum: int = 48) -> Tuple[List[int], List[int]]:
    widths: List[int] = []
    remain = max_sum
    for i in range(n):
        left_slots = n - i - 1
        # 给后面至少各留 1 bit
        hi = min(31, remain - left_slots)
        w = RNG.randint(1, hi)
        widths.append(w)
        remain -= w
    # 把剩余 bit 尽量塞进最后一个字段（仍 <=31）
    if remain > 0:
        add = min(remain, 31 - widths[-1])
        widths[-1] += add
        remain -= add
    # 若仍有剩余，从前向后能加就加
    i = 0
    while remain > 0 and i < n:
        room = 31 - widths[i]
        if room > 0:
            add = min(room, remain)
            widths[i] += add
            remain -= add
        i += 1
    assert sum(widths) <= max_sum
    values = [RNG.randint(0, (1 << w) - 1) for w in widths]
    return widths, values


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)

    cases: List[Tuple[List[int], List[int]]] = []

    # 1-3: 样例
    cases.append(([5, 3, 6], [10, 5, 40]))
    cases.append(([8], [255]))
    cases.append(([31], [0]))

    # 4: 恰满一字节多字段
    cases.append(([1, 1, 1, 1, 1, 1, 1, 1], [1, 0, 1, 0, 1, 0, 1, 0]))

    # 5: 字段内需高位补 0（卡「低位补 0」假解）
    cases.append(([7, 1], [1, 1]))  # 00000011 vs 错误 10000001 之类

    # 6: 总长需右侧补齐（卡左侧补齐假解）
    cases.append(([3, 3], [7, 1]))  # 6 bit -> pad 2

    # 7: 最大单字段非零
    cases.append(([31], [(1 << 30) + 7]))

    # 8: n=10 小宽度
    w8 = [1] * 10
    v8 = [i % 2 for i in range(10)]
    cases.append((w8, v8))

    # 9-10: 接近 48 bit 上限
    cases.append(rand_case(10, 48))
    cases.append(rand_case(6, 48))

    assert len(cases) == 10
    for i, (w, v) in enumerate(cases, 1):
        write_pair(i, w, v)

    # 自校验
    for i in range(1, 11):
        raw = (DATA / f"{i}.in").read_text(encoding="utf-8")
        lines = raw.split("\n")
        assert len(lines) == 2
        w = eval(lines[0])
        v = eval(lines[1])
        got = '"' + pack_fields(w, v) + '"\n'
        exp = (DATA / f"{i}.out").read_text(encoding="utf-8")
        assert got == exp, (i, got, exp)
        # .in 不以 \n 结尾
        assert not (DATA / f"{i}.in").read_bytes().endswith(b"\n")
        assert (DATA / f"{i}.out").read_bytes().endswith(b"\n")

    # config.yaml
    cases_yaml = "\n".join(
        f"      - input: {i}.in\n        output: {i}.out" for i in range(1, 11)
    )
    config = f"""type: default
user_extra_files:
  - template.py
  - template.java
  - template.cc
  - compile.sh
  - config.yaml
  - user.cc
  - user.java
  - user.py
subtasks:
  - score: 100
    if: []
    id: 1
    type: sum
    cases:
{cases_yaml}
langs:
  - py.py3
  - java
  - cc.cc14o2
  - py
  - cc
"""
    with open(DATA / "config.yaml", "w", encoding="utf-8", newline="\n") as f:
        f.write(config)

    with open(DATA / "README.md", "w", encoding="utf-8", newline="\n") as f:
        f.write(
            "主造数脚本：题目根目录 `gen.py`。\n"
            "hack：`5.in` 卡字段内低位补 0；`6.in` 卡整段左侧补齐到字节。\n"
            "9/10 组逼近总位数 48 上限。\n"
        )
    print("generated 10 cases OK")


if __name__ == "__main__":
    main()
