# -*- coding: utf-8 -*-
"""造数：涂卡互改。"""
from __future__ import annotations

import random
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
RNG = random.Random(539020260907)


def compress_probe(s: str) -> str:
    i0 = i1 = -1
    for i, ch in enumerate(s):
        if ch == "0" and i0 < 0:
            i0 = i
        elif ch == "1" and i1 < 0:
            i1 = i
        if i0 >= 0 and i1 >= 0:
            break
    return "".join(ch for i, ch in enumerate(s) if i != i0 and i != i1)


def rand_bits(n: int, force0: bool = True, force1: bool = True) -> str:
    chars = [RNG.choice("01") for _ in range(n)]
    if force0 and "0" not in chars:
        chars[RNG.randrange(n)] = "0"
    if force1 and "1" not in chars:
        pos = RNG.randrange(n)
        if chars[pos] == "0" and chars.count("0") == 1:
            pos = (pos + 1) % n
        chars[pos] = "1"
    if "0" not in chars:
        chars[0] = "0"
    if "1" not in chars:
        chars[-1] = "1"
    return "".join(chars)


def write_case(idx: int, s: str) -> None:
    assert 2 <= len(s) <= 10**5
    assert set(s) <= {"0", "1"}
    assert "0" in s and "1" in s
    (DATA / f"{idx}.in").write_bytes(s.encode("utf-8"))
    with open(DATA / f"{idx}.out", "w", encoding="utf-8", newline="\n") as f:
        f.write(compress_probe(s) + "\n")


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    cases = []

    # 1-3 题面样例
    cases.append(("样例1：101", "101"))
    cases.append(("样例2：hack 删前两字符/删最右 0", "0001"))
    cases.append(("样例3：110010", "110010"))

    # 4 最短
    cases.append(("最短 01", "01"))

    # 5 最短另一种
    cases.append(("最短 10", "10"))

    # 6 全 1 夹一个最右 0 —— 卡「删最右」
    cases.append(("最左 0 在末尾前", "1110"))

    # 7 交替，卡只删前缀
    cases.append(("交替 01", "01010101"))

    # 8 中等随机
    cases.append(("中等随机 n=400", rand_bits(400)))

    # 9 大：最左 0 很靠后，卡 O(n^2) 枚举
    big9 = "1" * 80000 + "0" + "1" * 19999
    cases.append(("极限：最左 0 靠后", big9))

    # 10 大：最左 1 很靠后
    big10 = "0" * 90000 + "1" + "0" * 9999
    cases.append(("极限：最左 1 靠后", big10))

    assert len(cases) == 10
    assert compress_probe("101") == "1"
    assert compress_probe("0001") == "00"
    assert compress_probe("110010") == "1010"

    for i, (_, s) in enumerate(cases, 1):
        write_case(i, s)

    import importlib.util

    spec = importlib.util.spec_from_file_location("std_mod", ROOT / "std.py")
    std_mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(std_mod)
    sol = std_mod.Solution()

    for i in range(1, 11):
        raw = (DATA / f"{i}.in").read_bytes()
        assert not raw.endswith(b"\n"), i
        s = raw.decode("utf-8")
        got = sol.reviseMarks(s) + "\n"
        exp = (DATA / f"{i}.out").read_text(encoding="utf-8")
        assert got == exp, (i, got, exp)
        outb = (DATA / f"{i}.out").read_bytes()
        assert outb.endswith(b"\n")
        assert outb.count(b"\n") == 1

    cases_yaml = "\n".join(
        f"      - input: {i}.in\n        output: {i}.out" for i in range(1, 11)
    )
    config = f"""type: default
user_extra_files:
  - template.py
  - template.java
  - template.cc
  - template.js
  - template.c
  - execute.sh
  - compile.sh
  - config.yaml
  - user.cc
  - user.java
  - user.py
  - user.js
  - user.c
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
  - js
  - c
"""
    (DATA / "config.yaml").write_text(config, encoding="utf-8")
    readme = ["# 测试数据说明", "", "主造数脚本：题目根目录 `gen.py`。", "stdin 一行 `0`/`1` 串，与题面样例同形。", "", "| 组 | 说明 |", "|---:|---|"]
    for i, (desc, _) in enumerate(cases, 1):
        readme.append(f"| {i} | {desc} |")
    (DATA / "README.md").write_text("\n".join(readme) + "\n", encoding="utf-8")

    shutil.copyfile(Path(r"d:\机考出题\problem-maker\compile.sh"), DATA / "compile.sh")
    shutil.copyfile(Path(r"d:\机考出题\problem-maker\核心代码模式模板\execute.sh"), DATA / "execute.sh")
    print("P5390 data ok")


if __name__ == "__main__":
    main()
