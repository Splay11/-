#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P5223 数据生成器
输入为一行一个整数 m (1 ≤ m ≤ 12)
"""

import os
import sys
import subprocess

# 确保可以 import std 和 testlib
sys.path.insert(0, os.path.dirname(__file__))
os.chdir(os.path.dirname(__file__))

from std import solve  # type: ignore

# ---------- 大数据 / 小数据 分界 ----------
LARGE_GROUP_COUNT = 2   # 后 2 组为大
SMALL_GROUP_COUNT = 8   # 前 8 组为小

def group_name(idx: int) -> str:
    return f"g{idx + 1:02d}"

# ---------- 测试点清单 ----------
ALL_MS = [2, 3, 1, 4, 5, 6, 7, 8, 10, 12]
assert len(ALL_MS) == SMALL_GROUP_COUNT + LARGE_GROUP_COUNT

TESTS = []
for g_idx, m_val in enumerate(ALL_MS):
    desc_map = {
        2: "sample1-m=2",
        3: "sample2-m=3",
        1: "boundary-min-m=1",
        4: "small-m=4",
        5: "small-m=5",
        6: "small-m=6",
        7: "small-m=7",
        8: "small-m=8",
        10: "large-m=10",
        12: "max-boundary-m=12",
    }
    TESTS.append((group_name(g_idx), m_val, desc_map.get(m_val, f"m={m_val}")))
    assert g_idx == len(TESTS) - 1

DATA_DIR = "data"

def gen():
    os.makedirs(DATA_DIR, exist_ok=True)
    small, large = [], []

    for g_idx, (g_name, m_val, desc) in enumerate(TESTS):
        basename = f"testcase{group_name(g_idx)}"
        in_path = os.path.join(DATA_DIR, f"{basename}.in")
        out_path = os.path.join(DATA_DIR, f"{basename}.out")
        ans = solve(m_val)

        # 写入 .in（无末尾空行，末尾恰好一个换行）
        with open(in_path, "w", newline="\n") as f:
            f.write(f"{m_val}\n")

        # 写入 .out（以换行结尾）
        with open(out_path, "w", newline="\n") as f:
            f.write(f"{ans}\n")

        print(f"[{desc}] {in_path}  ans={ans}")
        if g_idx < SMALL_GROUP_COUNT:
            small.append(basename)
        else:
            large.append(basename)

    # ---------- 写 config.yaml ----------
    lines = [
        "testcases:",
    ]

    if small:
        lines.append("  small:")
        for b in small:
            lines.append(f'    - "data/{b}"')
    else:
        lines.append("  small: []")

    if large:
        lines.append("  large:")
        for b in large:
            lines.append(f'    - "data/{b}"')
    else:
        lines.append("  large: []")

    lines.append("")

    with open("config.yaml", "w", newline="\n") as f:
        f.write("\n".join(lines))

    print("config.yaml generated.")

    # ---------- 写 data/README.md ----------
    readme_lines = [
        "# P5223 数据说明",
        "",
        "共 10 个测试点。前 8 个为小数据，后 2 个为大数据（m 较大、答案需取模）。",
        "",
        "| 编号 | 组名 | m | 说明 |",
        "|------|------|---|------|",
    ]
    for g_idx, (g_name, m_val, desc) in enumerate(TESTS):
        readme_lines.append(f"| {g_idx + 1} | {g_name} | {m_val} | {desc} |")

    readme_lines += [
        "",
        "## 预计易错",
        "",
        "- 忘记对 998244353 取模",
        "- 直接计算 `2**(2**m - 1)` 导致溢出",
        "- C++ 中用 `int`/`unsigned int` 计算指数时溢出（`1<<12=4096` 在 int 内安全，但指数 `(1<<12)-1=4095` 作为幂次传给倍增运算时，迭代次数需要 `long long` 来计数——不过 4095 次循环即使暴力也能过，但 `1<<m` 在 m=12 时对 int 是安全的，对 long long 封装依然安全。）",
        "",
        "## 对拍方式",
        "",
        "```bash",
        "# 生成数据",
        "python gen.py",
        "# C++ 标程验证",
        "g++ std.cpp -o std.exe -O2 -std=c++17",
        "for f in data/testcaseg*.in; do ./std.exe < $f | diff - ${f%.in}.out; done",
        "# Java 标程验证",
        "javac Main.java",
        "for f in data/testcaseg*.in; do java Main < $f | diff - ${f%.in}.out; done",
        "```",
    ]

    with open(os.path.join(DATA_DIR, "README.md"), "w", newline="\n") as f:
        f.write("\n".join(readme_lines))

    print("data/README.md generated.")


if __name__ == "__main__":
    gen()
