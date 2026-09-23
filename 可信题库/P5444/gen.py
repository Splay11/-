# -*- coding: utf-8 -*-
"""造数：记分牌订正。

设计要点：
  1-3   题面样例原文。
  4     只有一个元素的正数。
  5     全部为正。
  6     全部为负。
  7     最小项在末尾：只盯着第一项的写法会算错。
  8     最小项恰好是最小负值 -1000000000，答案超过 32 位范围。
  9     中等规模随机（n = 1000，含负数）。
  10    极限规模（n = 100000，元素压满正负 10^9）。
"""
from __future__ import annotations

import sys

sys.dont_write_bytecode = True

import json
import random
import shutil
from pathlib import Path
from typing import List

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
RNG = random.Random(544420260914)
LIMIT = 10 ** 9


def best_total(scores: List[int]) -> int:
    """参考实现：原总分减去 2 倍的最小项。"""
    total = 0
    mn = scores[0]
    for v in scores:
        total += v
        if v < mn:
            mn = v
    return total - 2 * mn


def brute_best(scores: List[int]) -> int:
    """朴素解：枚举每一项当作记反的那一项，取最大值，用于小数据交叉验证。"""
    best = None
    for i in range(len(scores)):
        cur = 0
        for j in range(len(scores)):
            cur += -scores[j] if j == i else scores[j]
        if best is None or cur > best:
            best = cur
    return best


def fmt_arr(a: List[int]) -> str:
    # 小样例用题面同款风格；大数据用紧凑写法，避免文件里出现多余空格
    if len(a) <= 20:
        return "[" + ", ".join(str(x) for x in a) + "]"
    return json.dumps(a, separators=(",", ":"))


def write_case(idx: int, scores: List[int]) -> None:
    assert 1 <= len(scores) <= 10 ** 5
    for x in scores:
        assert -LIMIT <= x <= LIMIT
    (DATA / f"{idx}.in").write_bytes(fmt_arr(scores).encode("utf-8"))
    with open(DATA / f"{idx}.out", "w", encoding="utf-8", newline="\n") as f:
        f.write(str(best_total(scores)) + "\n")


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    cases: List[tuple] = []

    # 1-3 题面样例原文
    cases.append(("样例1：[3, -5, 4]", [3, -5, 4]))
    cases.append(("样例2：[2, 2]", [2, 2]))
    cases.append(("样例3：[-1]", [-1]))

    # 4 只有一个元素的正数
    cases.append(("只有一个元素的正数 [5]", [5]))

    # 5 全部为正
    cases.append(("全部为正 [1, 2, 3]", [1, 2, 3]))

    # 6 全部为负
    cases.append(("全部为负 [-1, -2, -3]", [-1, -2, -3]))

    # 7 最小项在末尾：只检查第一项的写法会错
    cases.append(("最小项在末尾 [4, 9, 2, 7, -5]", [4, 9, 2, 7, -5]))

    # 8 最小项恰为最小负值，答案超过 32 位范围
    cases.append((
        "最小负值 -1000000000 夹在正数中，答案超 32 位",
        [1000000000, -1000000000, 999999999, 500000000],
    ))

    # 9 中等规模随机，含负数
    cases.append((
        "中等随机 n=1000，含负数",
        [RNG.randint(-LIMIT, LIMIT) for _ in range(1000)],
    ))

    # 10 极限规模，压满取值范围
    cases.append((
        "极限 n=100000，元素在 ±10^9 之间",
        [RNG.randint(-LIMIT, LIMIT) for _ in range(100000)],
    ))

    assert len(cases) == 10

    # 题面样例逐字核对
    assert best_total([3, -5, 4]) == 12
    assert best_total([2, 2]) == 0
    assert best_total([-1]) == 1

    # 小数据用朴素枚举交叉验证
    for _, scores in cases[:8]:
        assert best_total(scores) == brute_best(scores), scores

    for i, (_, scores) in enumerate(cases, 1):
        write_case(i, scores)

    # 用 std.py 重算，与 .out 逐字节比对，并检查换行约定
    import importlib.util

    spec = importlib.util.spec_from_file_location("std_mod", ROOT / "std.py")
    std_mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(std_mod)
    sol = std_mod.Solution()

    for i in range(1, 11):
        raw = (DATA / f"{i}.in").read_bytes()
        assert not raw.endswith(b"\n"), i
        scores = json.loads(raw.decode("utf-8"))
        got = (str(sol.bestCorrectedTotal(scores)) + "\n").encode("utf-8")
        outb = (DATA / f"{i}.out").read_bytes()
        assert outb == got, (i, got, outb)
        assert outb.endswith(b"\n") and not outb.endswith(b"\n\n"), i
        assert outb.decode("utf-8").count("\n") == 1, i

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
        "stdin 一行整型数组，形如 `[3, -5, 4]`，与题面样例同形。",
        "",
        "| 组 | 说明 |",
        "|---:|---|",
    ]
    for i, (desc, _) in enumerate(cases, 1):
        readme.append(f"| {i} | {desc} |")
    (DATA / "README.md").write_text("\n".join(readme) + "\n", encoding="utf-8")

    shutil.copyfile(Path(r"d:\机考出题\problem-maker\compile.sh"), DATA / "compile.sh")
    shutil.copyfile(
        Path(r"d:\机考出题\problem-maker\核心代码模式模板\execute.sh"),
        DATA / "execute.sh",
    )
    print("OK")


if __name__ == "__main__":
    main()
