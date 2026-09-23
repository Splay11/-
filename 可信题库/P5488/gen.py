# -*- coding: utf-8 -*-
"""P5488 造数：试味笔记首档。"""
from __future__ import annotations

import json
import random
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
RNG = random.Random(5488)


def first_taste_level(note: str) -> int:
    for ch in note:
        if "0" <= ch <= "9":
            return ord(ch) - ord("0")
    return -1


def write_case(idx: int, note: str) -> None:
    assert 1 <= len(note) <= 10**5
    for ch in note:
        assert ("a" <= ch <= "z") or ("0" <= ch <= "9")
    text_in = json.dumps(note, ensure_ascii=False)
    (DATA / f"{idx}.in").write_bytes(text_in.encode("utf-8"))
    with open(DATA / f"{idx}.out", "w", encoding="utf-8", newline="\n") as f:
        f.write(str(first_taste_level(note)) + "\n")


def rand_letters(n: int) -> str:
    return "".join(RNG.choice("abcdefghijklmnopqrstuvwxyz") for _ in range(n))


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    cases = []

    # 1-3: 题面样例
    cases.append("taste3ok")
    cases.append("nolevel")
    cases.append("0mild")

    # 4: 数字在末尾
    cases.append("abcxyz7")

    # 5: 全数字，hack「当成多位数解析」
    cases.append("409")

    # 6: 多个数字，必须取第一个
    cases.append("aa8bb9cc")

    # 7: 中等随机，保证有数字
    mid = rand_letters(80) + str(RNG.randint(0, 9)) + rand_letters(80)
    cases.append(mid)

    # 8: 中等随机，可能无数字
    cases.append(rand_letters(200))

    # 9: 大：字母铺满后末尾一个数字（卡「扫到最后」）
    cases.append(rand_letters(10**5 - 1) + "5")

    # 10: 大：开头就是 0，hack「跳过 0」
    cases.append("0" + rand_letters(10**5 - 1))

    assert len(cases) == 10
    assert first_taste_level(cases[0]) == 3
    assert first_taste_level(cases[1]) == -1
    assert first_taste_level(cases[2]) == 0

    for i, note in enumerate(cases, 1):
        write_case(i, note)

    import importlib.util

    spec = importlib.util.spec_from_file_location("std_mod", ROOT / "std.py")
    std_mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(std_mod)
    sol = std_mod.Solution()

    for i in range(1, 11):
        raw = (DATA / f"{i}.in").read_text(encoding="utf-8")
        note = json.loads(raw)
        got = str(sol.firstTasteLevel(note)) + "\n"
        exp = (DATA / f"{i}.out").read_text(encoding="utf-8")
        assert got == exp, (i, got, exp)
        assert not (DATA / f"{i}.in").read_bytes().endswith(b"\n")
        assert (DATA / f"{i}.out").read_bytes().endswith(b"\n")
        assert (DATA / f"{i}.out").read_bytes().count(b"\n") == 1

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
    (DATA / "README.md").write_text(
        "主造数脚本：题目根目录 gen.py。stdin 一行 JSON 字符串。\n",
        encoding="utf-8",
    )
    compile_src = Path(r"d:\机考出题\problem-maker\compile.sh")
    exec_src = Path(r"d:\机考出题\problem-maker\核心代码模式模板\execute.sh")
    shutil.copyfile(compile_src, DATA / "compile.sh")
    shutil.copyfile(exec_src, DATA / "execute.sh")
    print("P5488 data ok:", [first_taste_level(c) for c in cases])


if __name__ == "__main__":
    main()
