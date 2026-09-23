# -*- coding: utf-8 -*-
"""造数：课桌传书。"""
from __future__ import annotations

import json
import random
import shutil
from pathlib import Path
from typing import List

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
RNG = random.Random(539120260907)


def can_shift(a: List[int]) -> bool:
    s = 0
    for i, x in enumerate(a):
        s += x
        k = i + 1
        if s < k * (k + 1) // 2:
            return False
    return True


def fmt_arr(a: List[int]) -> str:
    if len(a) <= 20:
        return "[" + ", ".join(str(x) for x in a) + "]"
    return json.dumps(a, separators=(",", ":"))


def write_case(idx: int, a: List[int]) -> None:
    assert 1 <= len(a) <= 10**5
    for x in a:
        assert 1 <= x <= 10**9
    text_in = fmt_arr(a)
    (DATA / f"{idx}.in").write_bytes(text_in.encode("utf-8"))
    with open(DATA / f"{idx}.out", "w", encoding="utf-8", newline="\n") as f:
        f.write(("true" if can_shift(a) else "false") + "\n")


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    cases: List[tuple[str, List[int]]] = []

    cases.append(("样例1：已递增", [1, 2, 3]))
    cases.append(("样例2：总和不够", [1, 1, 2]))
    cases.append(("样例3：左边可右移", [10, 1, 1]))

    # 4 单张课桌
    cases.append(("单张课桌", [1]))

    # 5 全相等但总和够
    cases.append(("全 2，n=3", [2, 2, 2]))

    # 6 前缀失败：总和够但第二位不够 —— 卡只查总和
    cases.append(("hack：只查总和", [1, 1, 3, 5]))

    # 7 已递增边界 n=1 大值
    cases.append(("单桌大值", [10**9]))

    # 8 中等随机
    mid = [RNG.randint(1, 20) for _ in range(80)]
    cases.append(("中等随机", mid))

    # 9 大：刚好每个前缀卡在需求上 1,2,3,...,n
    n9 = 100000
    big9 = list(range(1, n9 + 1))
    cases.append(("极限：1..n 刚好", big9))

    # 10 大：几乎可行但在中段前缀差 1 —— 卡只看总和 / 32 位溢出
    n10 = 100000
    big10 = [1] * n10
    # 把多余全堆到最后，使总和很大但前缀早期失败
    big10[-1] = 10**9
    cases.append(("极限：前缀不足", big10))

    assert len(cases) == 10
    assert can_shift([1, 2, 3]) is True
    assert can_shift([1, 1, 2]) is False
    assert can_shift([10, 1, 1]) is True
    assert can_shift([1, 1, 3, 5]) is False

    for i, (_, a) in enumerate(cases, 1):
        write_case(i, a)

    import importlib.util

    spec = importlib.util.spec_from_file_location("std_mod", ROOT / "std.py")
    std_mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(std_mod)
    sol = std_mod.Solution()

    for i in range(1, 11):
        raw = (DATA / f"{i}.in").read_bytes()
        assert not raw.endswith(b"\n"), i
        a = json.loads(raw.decode("utf-8"))
        got = ("true" if sol.canPassBooks(a) else "false") + "\n"
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
    readme = [
        "# 测试数据说明",
        "",
        "主造数脚本：题目根目录 `gen.py`。",
        "stdin 一行整数数组，与题面样例同形。",
        "",
        "| 组 | 说明 |",
        "|---:|---|",
    ]
    for i, (desc, _) in enumerate(cases, 1):
        readme.append(f"| {i} | {desc} |")
    (DATA / "README.md").write_text("\n".join(readme) + "\n", encoding="utf-8")

    shutil.copyfile(Path(r"d:\机考出题\problem-maker\compile.sh"), DATA / "compile.sh")
    shutil.copyfile(Path(r"d:\机考出题\problem-maker\核心代码模式模板\execute.sh"), DATA / "execute.sh")
    print("P5391 data ok:", [can_shift(a) for _, a in cases])


if __name__ == "__main__":
    main()
