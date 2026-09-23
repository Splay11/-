# -*- coding: utf-8 -*-
"""造数：多球力度窗口。"""
from __future__ import annotations

import json
import random
import shutil
from pathlib import Path
from typing import List

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
RNG = random.Random(540120260909)


def min_force_window(hits: List[int]) -> int:
    n = len(hits)
    tot = 0
    for x in hits:
        tot |= x
    if tot == 0:
        return 1
    ans = 1
    for b in range(31):
        if ((tot >> b) & 1) == 0:
            continue
        prev = -1
        mx = 0
        for i, x in enumerate(hits):
            if (x >> b) & 1:
                mx = max(mx, i - prev)
                prev = i
        mx = max(mx, n - prev)
        ans = max(ans, mx)
    return ans


def fmt_arr(a: List[int]) -> str:
    if len(a) <= 20:
        return "[" + ", ".join(str(x) for x in a) + "]"
    return json.dumps(a, separators=(",", ":"))


def write_case(idx: int, a: List[int]) -> None:
    assert 1 <= len(a) <= 10**5
    for x in a:
        assert 0 <= x <= 10**9
    text_in = fmt_arr(a)
    (DATA / f"{idx}.in").write_bytes(text_in.encode("utf-8"))
    with open(DATA / f"{idx}.out", "w", encoding="utf-8", newline="\n") as f:
        f.write(str(min_force_window(a)) + "\n")


def write_config() -> None:
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
    shutil.copyfile(Path(r"d:\机考出题\problem-maker\compile.sh"), DATA / "compile.sh")
    shutil.copyfile(Path(r"d:\机考出题\problem-maker\核心代码模式模板\execute.sh"), DATA / "execute.sh")


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    cases: List[tuple[str, List[int]]] = []
    cases.append(("样例1", [1, 2, 3]))
    cases.append(("样例2：高位只在开头", [8, 1, 2]))
    cases.append(("样例3：全 0", [0, 0, 0]))
    cases.append(("单元素", [7]))
    cases.append(("hack：漏掉右端哨兵", [1, 2, 4, 0, 0, 0, 0]))
    cases.append(("hack：只看值种类", [3, 3, 3, 3]))
    cases.append(("中等随机", [RNG.randint(0, 255) for _ in range(80)]))
    cases.append(("构造：两位交错很远", [1] + [0] * 40 + [2] + [0] * 40 + [1]))
    big9 = [RNG.randint(0, 10**9) for _ in range(100000)]
    cases.append(("极限随机 n=1e5", big9))
    big10 = [(1 << 29)] + [0] * 99998 + [1]
    cases.append(("极限：最高位只在左端", big10))

    assert len(cases) == 10
    assert min_force_window([1, 2, 3]) == 2
    assert min_force_window([8, 1, 2]) == 3
    assert min_force_window([0, 0, 0]) == 1

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
        got = str(sol.minForceWindow(a)) + "\n"
        exp = (DATA / f"{i}.out").read_text(encoding="utf-8")
        assert got == exp, (i, got, exp)
        assert (DATA / f"{i}.out").read_bytes().endswith(b"\n")

    write_config()
    readme = ["# 测试数据说明", "", "主造数脚本：题目根目录 `gen.py`。", "stdin 一行整数数组。", "", "| 组 | 说明 |", "|---:|---|"]
    for i, (desc, _) in enumerate(cases, 1):
        readme.append(f"| {i} | {desc} |")
    (DATA / "README.md").write_text("\n".join(readme) + "\n", encoding="utf-8")
    print("P5401 data ok")


if __name__ == "__main__":
    main()
