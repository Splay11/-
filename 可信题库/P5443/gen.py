# -*- coding: utf-8 -*-
"""造数：烤盘份数最接近。"""
import sys

sys.dont_write_bytecode = True

import importlib.util
import json
import random
import shutil
from pathlib import Path
from typing import List, Tuple

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
RNG = random.Random(544320260914)
LIMIT = 10**9


def fmt_arr(a: List[int]) -> str:
    """整型数组写在一行，形如题面样例 [4, 9, 6, 6, 12]。"""
    return "[" + ", ".join(str(x) for x in a) + "]"


def increasing(n: int) -> List[int]:
    """单调递增：每步加上一个正间隔，保证严格上升。"""
    vals = [0]
    for _ in range(n - 1):
        vals.append(vals[-1] + RNG.randint(1000, 5000))
    return vals


def decreasing(n: int) -> List[int]:
    """单调递减：每步减去一个正间隔，减值总量远小于 10^9，不会出现负数。"""
    vals = [LIMIT]
    for _ in range(n - 1):
        vals.append(vals[-1] - RNG.randint(1000, 5000))
    return vals


def mid_hack() -> List[int]:
    """最小差落在数组中间：首尾两对的差都很大，只有中间一对相差 1。"""
    return [1000000000, 500000000, 1000000, 1000001, 700000000, 200000000, 900000000, 300000000]


def medium_random(n: int) -> List[int]:
    return [RNG.randint(0, LIMIT) for _ in range(n)]


def big_random(n: int) -> List[int]:
    """大数组压满范围：显式放入 0 与 10^9。"""
    vals = [RNG.randint(0, LIMIT) for _ in range(n)]
    vals[0] = 0
    vals[-1] = LIMIT
    return vals


def write_case(idx: int, a: List[int], sol) -> None:
    n = len(a)
    assert 2 <= n <= 10**5, (idx, n)
    for x in a:
        assert 0 <= x <= LIMIT, (idx, x)
    # .in 一行数组，末尾不带换行
    (DATA / f"{idx}.in").write_bytes(fmt_arr(a).encode("utf-8"))
    with open(DATA / f"{idx}.out", "w", encoding="utf-8", newline="\n") as f:
        f.write(str(sol.minAdjacentGap(a)) + "\n")


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)

    spec = importlib.util.spec_from_file_location("std_mod", ROOT / "std.py")
    std_mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(std_mod)
    sol = std_mod.Solution()

    cases: List[Tuple[str, List[int]]] = []

    # 1-3 题面样例原文
    cases.append(("样例1：第 3、4 盘都是 6，答案 0", [4, 9, 6, 6, 12]))
    cases.append(("样例2：三盘，10 与 8 相差 2 最小", [3, 10, 8]))
    cases.append(("样例3：只有两盘，答案 99", [1, 100]))

    # 4 最短长度且两盘相同
    cases.append(("两盘件数相同 [7, 7]，答案 0", [7, 7]))

    # 5 最短长度且相差拉满
    cases.append(("两盘分别取 0 与 10^9，答案 10^9", [0, 1000000000]))

    # 6 单调递增长数组：最小差 = 最小的那个正间隔
    cases.append(("单调递增 n=100000", increasing(100000)))

    # 7 单调递减长数组
    cases.append(("单调递减 n=100000", decreasing(100000)))

    # 8 最小差出现在中间，首尾两对的差都很大
    cases.append(("最小差在数组中间（首尾差都很大），答案 1", mid_hack()))

    # 9 中等随机
    cases.append(("中等随机 n=1000", medium_random(1000)))

    # 10 大数组压满范围
    cases.append(("大 n=100000，含 0 与 10^9", big_random(100000)))

    assert len(cases) == 10

    # 三组样例的答案先钉死
    assert sol.minAdjacentGap([4, 9, 6, 6, 12]) == 0
    assert sol.minAdjacentGap([3, 10, 8]) == 2
    assert sol.minAdjacentGap([1, 100]) == 99
    # 第 8 组要真的是「最小差在中间」
    assert sol.minAdjacentGap(mid_hack()) == 1

    for i, (_, a) in enumerate(cases, 1):
        write_case(i, a, sol)

    # 1-3 的 .in 必须与题面样例原文逐字节相同
    assert (DATA / "1.in").read_bytes() == b"[4, 9, 6, 6, 12]"
    assert (DATA / "2.in").read_bytes() == b"[3, 10, 8]"
    assert (DATA / "3.in").read_bytes() == b"[1, 100]"

    # 自校验：用 std.py 重算并逐组逐字节比对
    for i in range(1, 11):
        raw = (DATA / f"{i}.in").read_bytes()
        assert not raw.endswith(b"\n"), i
        arr = json.loads(raw.decode("utf-8"))
        assert 2 <= len(arr) <= 10**5, i
        got = str(sol.minAdjacentGap(arr)) + "\n"
        exp = (DATA / f"{i}.out").read_text(encoding="utf-8")
        assert got == exp, (i, got, exp)
        outb = (DATA / f"{i}.out").read_bytes()
        assert outb.endswith(b"\n"), i
        assert outb.count(b"\n") == 1, i

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
        "stdin 一行整型数组（形如 `[4, 9, 6, 6, 12]`，数字之间用 `, ` 分隔），与题面样例同形。",
        "",
        "| 组 | 说明 |",
        "|---:|---|",
    ]
    for i, (desc, _) in enumerate(cases, 1):
        readme.append(f"| {i} | {desc} |")
    (DATA / "README.md").write_text("\n".join(readme) + "\n", encoding="utf-8")

    shutil.copyfile(Path(r"d:\机考出题\problem-maker\compile.sh"), DATA / "compile.sh")
    shutil.copyfile(Path(r"d:\机考出题\problem-maker\核心代码模式模板\execute.sh"), DATA / "execute.sh")

    print("OK")


if __name__ == "__main__":
    main()
