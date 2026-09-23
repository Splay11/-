# -*- coding: utf-8 -*-
"""生成 P5525 测试数据：样例在前，末两组近上限。"""
from __future__ import annotations

import random
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
STD = ROOT / "std.py"
RNG = random.Random(5525)

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
    # .in 不以换行结尾
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
    if not out.endswith("\n"):
        out += "\n"
    # 保证末尾仅一个换行
    out = out.rstrip("\n") + "\n"
    (DATA / f"{idx}.out").write_bytes(out.encode("utf-8"))


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    cases = [
        "256",  # 样例1
        "72",  # 样例2
        "1",  # 样例3 / 边界
        "2",  # 质数
        "12",  # 需一次乘法
        "8",  # p^3
        str(2**39),  # 纯 2 的高幂，仅开方
        str(2**10 * 3**7 * 5**3),  # 多质数 hack
        str(10**12),  # 近上限
        str(999999999989),  # 近上限大质数
    ]
    assert len(cases) == 10
    for i, c in enumerate(cases, 1):
        write_case(i, c)

    case_lines = "\n".join(
        f"      - input: {i}.in\n        output: {i}.out" for i in range(1, 11)
    )
    cfg = CONFIG.format(cases=case_lines)
    (ROOT / "config.yaml").write_text(cfg, encoding="utf-8")
    (DATA / "config.yaml").write_text(cfg, encoding="utf-8")
    print("P5525 gen done")


if __name__ == "__main__":
    main()
