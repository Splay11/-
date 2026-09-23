# -*- coding: utf-8 -*-
"""P14410 测试数据生成。stdin 一行：intervals 二维数组。"""
import ast
import os
import random
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)
from std import Solution

RNG = random.Random(14410001)


def format_input(intervals):
    inner = []
    for s, e in intervals:
        inner.append("[" + ",".join(str(x) for x in (s, e)) + "]")
    return "[" + ",".join(inner) + "]"


def format_output(ans):
    return f"{ans}\n"


def solve_line(line: str) -> str:
    intervals = ast.literal_eval(line.strip())
    ans = Solution().countIsolatedIntervals(intervals)
    return format_output(ans)


def write_in(path: str, text: str):
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text.rstrip("\n"))


def write_out(path: str, text: str):
    if not text.endswith("\n"):
        text += "\n"
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)


def write_config_yaml(data_dir: str):
    lines = [
        "type: default\n",
        "user_extra_files:\n",
        "  - template.py\n",
        "  - template.java\n",
        "  - template.cc\n",
        "  - compile.sh\n",
        "  - config.yaml\n",
        "  - user.cc\n",
        "  - user.java\n",
        "  - user.py\n",
        "subtasks:\n",
        "  - score: 100\n",
        "    if: []\n",
        "    id: 1\n",
        "    type: sum\n",
        "    cases:\n",
    ]
    for i in range(1, 11):
        lines.append(f"      - input: {i}.in\n")
        lines.append(f"        output: {i}.out\n")
    lines += ["langs:\n", "  - py.py3\n", "  - java\n", "  - cc.cc14o2\n", "  - py\n", "  - cc\n"]
    with open(os.path.join(data_dir, "config.yaml"), "w", encoding="utf-8", newline="\n") as f:
        f.writelines(lines)


def gen_disjoint_chain(k):
    intervals = [[i * 2, i * 2 + 1] for i in range(k)]
    return format_input(intervals)


def gen_touching_chain(k):
    intervals = [[i, i + 1] for i in range(k)]
    return format_input(intervals)


def gen_random(n):
    intervals = []
    for _ in range(n):
        s = RNG.randint(0, 9990)
        e = s + RNG.randint(0, 10)
        intervals.append([s, e])
    return format_input(intervals)


def gen_max_stress():
    n = 10000
    intervals = []
    for i in range(n):
        intervals.append([i * 2, i * 2 + 1])
    return format_input(intervals)


def main():
    data_dir = os.path.join(ROOT, "data")
    os.makedirs(data_dir, exist_ok=True)
    generators = [
        ("样例1：部分独立", lambda: format_input([[8, 10], [1, 4], [2, 6], [15, 18]])),
        ("样例2：端点相接全重叠", lambda: format_input([[2, 4], [4, 6]])),
        ("样例3：n=1", lambda: format_input([[0, 1]])),
        ("边界：全部互不重叠", lambda: gen_disjoint_chain(8)),
        ("边界：端点链全重叠", lambda: gen_touching_chain(6)),
        ("hack：排序后只查相邻", lambda: format_input([[0, 100], [50, 60], [101, 200]])),
        ("hack：端点相接不算重叠", lambda: format_input([[0, 1], [1, 2], [5, 6]])),
        ("hack：大区间吞小区间", lambda: format_input([[0, 50], [10, 20], [60, 70]])),
        ("随机中等规模", lambda: gen_random(800)),
        ("极限 n=10000 互不重叠", lambda: gen_max_stress()),
    ]
    for i, (_, gen) in enumerate(generators, start=1):
        inp = gen()
        write_in(os.path.join(data_dir, f"{i}.in"), inp)
        write_out(os.path.join(data_dir, f"{i}.out"), solve_line(inp))
    write_config_yaml(data_dir)
    repo_compile = os.path.normpath(os.path.join(ROOT, "..", "..", "compile.sh"))
    if not os.path.isfile(repo_compile):
        raise SystemExit(f"missing compile.sh: {repo_compile}")
    with open(repo_compile, "rb") as src, open(os.path.join(data_dir, "compile.sh"), "wb") as dst:
        dst.write(src.read())
    for i in range(1, 11):
        with open(os.path.join(data_dir, f"{i}.in"), "rb") as f:
            if f.read().endswith(b"\n"):
                raise SystemExit(f"{i}.in must not end with newline")
        with open(os.path.join(data_dir, f"{i}.out"), "rb") as f:
            raw = f.read()
            if not raw.endswith(b"\n") or raw.endswith(b"\n\n"):
                raise SystemExit(f"{i}.out newline rule")
        with open(os.path.join(data_dir, f"{i}.in"), encoding="utf-8") as f:
            if solve_line(f.read()) != open(os.path.join(data_dir, f"{i}.out"), encoding="utf-8").read():
                raise SystemExit(f"group {i} mismatch")
    with open(os.path.join(data_dir, "README.md"), "w", encoding="utf-8", newline="\n") as f:
        f.write("# P14410 测试数据\n\n主脚本：题目根 `gen.py`。\n\n")
        f.write("| # | 说明 |\n|---|------|\n")
        for i, (note, _) in enumerate(generators, 1):
            f.write(f"| {i} | {note} |\n")
    print("P14410 data ok")


if __name__ == "__main__":
    main()
