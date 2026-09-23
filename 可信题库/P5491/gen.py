# -*- coding: utf-8 -*-
from __future__ import annotations

import json
import random
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
RNG = random.Random(5491)


def max_split_product(seq: str) -> int:
    n = len(seq)
    ans = 0
    for k in range(1, n):
        ans = max(ans, int(seq[:k]) * int(seq[k:]))
    return ans


def write_case(idx: int, seq: str) -> None:
    assert 2 <= len(seq) <= 9
    assert seq.isdigit()
    (DATA / f"{idx}.in").write_bytes(json.dumps(seq).encode("utf-8"))
    with open(DATA / f"{idx}.out", "w", encoding="utf-8", newline="\n") as f:
        f.write(str(max_split_product(seq)) + "\n")


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    cases = [
        "2222",
        "4051",
        "10",
        "99",
        "1001",
        "20202",
        "87654321",
        "00012",
        "999999999",
        "".join(str(RNG.randint(0, 9)) for _ in range(9)),
    ]
    assert len(cases) == 10
    assert max_split_product(cases[0]) == 484
    assert max_split_product(cases[1]) == 2040
    assert max_split_product(cases[2]) == 0

    for i, seq in enumerate(cases, 1):
        write_case(i, seq)

    import importlib.util

    spec = importlib.util.spec_from_file_location("std_mod", ROOT / "std.py")
    std_mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(std_mod)
    sol = std_mod.Solution()
    for i in range(1, 11):
        seq = json.loads((DATA / f"{i}.in").read_text(encoding="utf-8"))
        got = str(sol.maxSplitProduct(seq)) + "\n"
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
    (DATA / "README.md").write_text("主造数脚本：题目根目录 gen.py。stdin 一行 JSON 字符串。\n", encoding="utf-8")
    shutil.copyfile(Path(r"d:\机考出题\problem-maker\compile.sh"), DATA / "compile.sh")
    shutil.copyfile(Path(r"d:\机考出题\problem-maker\核心代码模式模板\execute.sh"), DATA / "execute.sh")
    print("P5491 data ok", [max_split_product(c) for c in cases])


if __name__ == "__main__":
    main()
