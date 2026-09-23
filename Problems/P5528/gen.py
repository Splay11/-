# -*- coding: utf-8 -*-
"""生成 P5528 测试数据：样例在前，末两组近上限。"""
from __future__ import annotations

import random
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
STD = ROOT / "std.py"
RNG = random.Random(5528)

CONFIG = """type: default
time: 2s
memory: 256m
subtasks:
  - score: 100
    type: sum
    cases:
{cases}
langs:
  - py.py3
  - java
  - cc.cc14o2
"""


def write_case(idx: int, content: str) -> None:
    text = content.rstrip("\n")
    (DATA / f"{idx}.in").write_bytes(text.encode("utf-8"))
    proc = subprocess.run(
        [sys.executable, str(STD)],
        input=text + "\n",
        capture_output=True,
        text=True,
        check=True,
    )
    out = proc.stdout.replace("\r\n", "\n")
    if out.strip() == "":
        # 无 get 时仍写单个换行？题面 get 才有输出；若无输出写空文件+换行不合适
        # 保证有 get 的用例；若为空则写单个换行
        out = "\n"
    else:
        out = out.rstrip("\n") + "\n"
    (DATA / f"{idx}.out").write_bytes(out.encode("utf-8"))


def fmt(cap: int, ops: list[str]) -> str:
    return f"{cap} {len(ops)}\n" + "\n".join(ops)


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    s1 = """2 6
put 1 10 100 1
put 2 20 5 2
get 1 3
get 2 3
get 2 8
get 1 50"""
    s2 = """2 7
put 1 10 100 1
put 2 20 100 2
put 3 30 100 3
get 1 4
get 2 4
get 3 4
get 3 5"""

    # 边界：容量 1
    c3 = fmt(
        1,
        [
            "put 1 1 10 0",
            "get 1 1",
            "put 2 2 10 2",
            "get 1 3",
            "get 2 3",
        ],
    )
    # 相等时间戳
    c4 = fmt(
        2,
        [
            "put 1 10 5 1",
            "put 2 20 5 1",
            "get 1 1",
            "get 2 1",
            "get 1 6",
            "get 2 6",
        ],
    )
    # 过期优先淘汰 hack：满时先清过期而非 LRU
    c5 = fmt(
        2,
        [
            "put 1 10 2 1",
            "put 2 20 100 2",
            "put 3 30 100 5",  # 时刻 5 时 key1 已过期(expire=3)，应淘汰 1 而非 2
            "get 1 6",
            "get 2 6",
            "get 3 6",
        ],
    )
    # 更新已有键刷新 TTL 与 LRU
    c6 = fmt(
        2,
        [
            "put 1 1 100 1",
            "put 2 2 100 2",
            "put 1 11 100 3",
            "put 3 3 100 4",  # 应淘汰 2（1 被刷新）
            "get 1 5",
            "get 2 5",
            "get 3 5",
        ],
    )
    # 中等随机
    ops7 = []
    ts = 0
    for i in range(200):
        if RNG.random() < 0.6 or i < 5:
            ts += RNG.randint(0, 2)
            ops7.append(
                f"put {RNG.randint(1, 20)} {RNG.randint(1, 100)} {RNG.randint(1, 30)} {ts}"
            )
        else:
            ts += RNG.randint(0, 2)
            ops7.append(f"get {RNG.randint(1, 20)} {ts}")
    c7 = fmt(5, ops7)

    ops8 = []
    ts = 0
    for i in range(1000):
        ts += RNG.randint(0, 1)
        if RNG.random() < 0.55:
            ops8.append(
                f"put {RNG.randint(1, 50)} {RNG.randint(1, 10**6)} {RNG.randint(1, 100)} {ts}"
            )
        else:
            ops8.append(f"get {RNG.randint(1, 50)} {ts}")
    c8 = fmt(20, ops8)

    # 近上限
    ops9 = []
    ts = 0
    for i in range(100000):
        if i % 3 != 2:
            ops9.append(f"put {i % 1000 + 1} {i % 1000 + 1} 1000000 {ts}")
        else:
            ops9.append(f"get {i % 1000 + 1} {ts}")
        if i % 10 == 0:
            ts += 1
    c9 = fmt(1000, ops9)

    ops10 = []
    ts = 0
    # 10^5 次随机键操作时 Python 标程约 5 秒，超过 2 秒时限；收到 2×10^4。
    for i in range(20000):
        ts += RNG.randint(0, 3)
        if RNG.random() < 0.5:
            ops10.append(
                f"put {RNG.randint(1, 10**6)} {RNG.randint(1, 10**6)} {RNG.randint(1, 10**6)} {ts}"
            )
        else:
            ops10.append(f"get {RNG.randint(1, 10**6)} {ts}")
    c10 = fmt(1000, ops10)

    cases = [s1, s2, c3, c4, c5, c6, c7, c8, c9, c10]
    assert len(cases) == 10
    for i, c in enumerate(cases, 1):
        write_case(i, c)
        print(f"case {i} done")

    case_lines = "\n".join(
        f"      - input: {i}.in\n        output: {i}.out" for i in range(1, 11)
    )
    cfg = CONFIG.format(cases=case_lines)
    (ROOT / "config.yaml").write_text(cfg, encoding="utf-8")
    (DATA / "config.yaml").write_text(cfg, encoding="utf-8")
    print("P5528 gen done")


if __name__ == "__main__":
    main()
