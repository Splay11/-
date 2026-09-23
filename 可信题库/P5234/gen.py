# -*- coding: utf-8 -*-
"""P5234 造数：字母串排序变换。"""
from __future__ import annotations

import random
import string
from pathlib import Path
from typing import List

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
RNG = random.Random(5234)


def sort_letter(s: str) -> str:
    chars = sorted(s)
    out = []
    for c in chars:
        pos = ord(c.lower()) - ord("a") + 1
        new_pos = (pos * pos) % 26 + 1
        ch = chr(ord("A") + new_pos - 1)
        out.append(ch.lower() if c.isupper() else ch.upper())
    return "".join(out)


def write_case(idx: int, s: str) -> None:
    assert 1 <= len(s) <= 10**4
    assert all(c.isalpha() and c.isascii() for c in s)
    text_in = '"' + s + '"'
    (DATA / f"{idx}.in").write_bytes(text_in.encode("utf-8"))
    with open(DATA / f"{idx}.out", "w", encoding="utf-8", newline="\n") as f:
        f.write('"' + sort_letter(s) + '"\n')


def rand_str(n: int) -> str:
    alphabet = string.ascii_letters
    return "".join(RNG.choice(alphabet) for _ in range(n))


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    cases: List[str] = []

    # 1: 题面样例
    cases.append("abB")
    # 2: 单字符大写
    cases.append("A")
    # 3: 单字符小写
    cases.append("z")
    # 4: 已按 ASCII 排好（大写在前）
    cases.append("Ab")
    # 5: 全相同字母不同大小写（卡「忽略大小写排序」假解）
    cases.append("aAaA")
    # 6: 触发 pos^2%26 绕回（如 Z: 26^2=676, 676%26=0 → 1 → A）
    cases.append("ZzY")
    # 7: 中间字母 e：25%26+1=26 → Z
    cases.append("eeeEEE")
    # 8: 中等随机
    cases.append(rand_str(50))
    # 9: 较大
    cases.append(rand_str(1000))
    # 10: 上限
    cases.append(rand_str(10000))

    assert len(cases) == 10
    assert sort_letter(cases[0]) == "eBE"
    assert sort_letter("Z") == "a"  # 26^2%26+1=1 → A → 小写 a
    assert sort_letter("z") == "A"

    for i, s in enumerate(cases, 1):
        write_case(i, s)

    for i in range(1, 11):
        raw = (DATA / f"{i}.in").read_text(encoding="utf-8")
        s = eval(raw)
        got = '"' + sort_letter(s) + '"\n'
        exp = (DATA / f"{i}.out").read_text(encoding="utf-8")
        assert got == exp, (i, got, exp)
        assert not (DATA / f"{i}.in").read_bytes().endswith(b"\n")
        assert (DATA / f"{i}.out").read_bytes().endswith(b"\n")

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
    (DATA / "config.yaml").write_text(config, encoding="utf-8")
    (DATA / "README.md").write_text(
        "主造数脚本：题目根目录 `gen.py`。测例 stdin/stdout 均为带双引号字符串。\n",
        encoding="utf-8",
    )
    print("P5234 data ok:", [sort_letter(c)[:20] for c in cases])


if __name__ == "__main__":
    main()
