# -*- coding: utf-8 -*-
"""P5108 测试数据生成。stdin 单行：n,[temperatures],k,t"""
import ast
import os
import random
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)
from std import Solution

RNG = random.Random(5108001)


def format_in(temperatures, k, t):
    n = len(temperatures)
    arr = "[" + ",".join(str(x) for x in temperatures) + "]"
    return f"{n},{arr},{k},{t}"


def format_out(values):
    return "[" + ",".join(str(x) for x in values) + "]\n"


def split_top_level_commas(s: str):
    parts = []
    start = 0
    depth = 0
    for i, c in enumerate(s):
        if c == "[":
            depth += 1
        elif c == "]":
            depth -= 1
        elif c == "," and depth == 0:
            parts.append(s[start:i])
            start = i + 1
    parts.append(s[start:])
    return parts


def parse_line(line: str):
    line = line.strip("\r\n")
    parts = split_top_level_commas(line)
    temperatures = ast.literal_eval(parts[1].strip())
    k = int(parts[2].strip())
    t = int(parts[3].strip())
    return temperatures, k, t


def solve_line(line: str) -> str:
    temperatures, k, t = parse_line(line)
    ans = Solution().analyzeTemperatureData(temperatures, k, t)
    return format_out(ans)


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


def gen_strict_rise_segment(start, step, k):
    return [start + i * step for i in range(k)]


def gen_large_array(n=10000):
    arr = []
    i = 0
    while len(arr) < n:
        block = RNG.randint(80, 220)
        if block <= 0:
            block = 100
        step = RNG.randint(1, 3)
        seg = gen_strict_rise_segment(RNG.randint(-50, 50), step, 3)
        if len(arr) + len(seg) <= n:
            arr.extend(seg)
        else:
            break
        tail = RNG.randint(1, 5)
        for _ in range(tail):
            if len(arr) >= n:
                break
            arr.append(arr[-1] + RNG.randint(-8, -1))
    while len(arr) < n:
        arr.append(RNG.randint(-100, 100))
    return arr[:n]


def main():
    data_dir = os.path.join(ROOT, "data")
    os.makedirs(data_dir, exist_ok=True)
    generators = [
        ("样例1", lambda: format_in([20, 25, 30, 28, 35, 40, 42, 25], 3, 10)),
        ("样例2", lambda: format_in([10, 15, 20], 3, 30)),
        ("样例3（数组含空格）", lambda: "6,[1, 3, 6, 2, 4, 7],3,5"),
        (
            "最高温首次出现下标",
            lambda: format_in([10, 20, 20, 15, 25], 2, 5),
        ),
        (
            "单调但升幅不足",
            lambda: format_in([0, 1, 2, 3, 4], 3, 10),
        ),
        (
            "单段危险窗口",
            lambda: format_in([5, 10, 20, 1, 2], 3, 12),
        ),
        (
            "hack：相邻相等非严格递增",
            lambda: format_in([1, 2, 2, 3, 4, 5], 3, 2),
        ),
        (
            "hack：最大升幅平局取最早起点",
            lambda: format_in([0, 2, 4, 10, 12, 14], 3, 4),
        ),
        (
            "负温度与边界阈值",
            lambda: format_in([-20, -10, 0, -5, 0, 5], 3, 10),
        ),
        ("极限 n=10000", lambda: format_in(gen_large_array(10000), 3, 10)),
    ]
    for i, (_, gen) in enumerate(generators, start=1):
        inp = gen()
        write_in(os.path.join(data_dir, f"{i}.in"), inp)
        write_out(os.path.join(data_dir, f"{i}.out"), solve_line(inp))
    write_config_yaml(data_dir)
    for i in range(1, 11):
        with open(os.path.join(data_dir, f"{i}.in"), "rb") as f:
            if f.read().endswith(b"\n"):
                raise SystemExit(f"{i}.in must not end with newline")
        with open(os.path.join(data_dir, f"{i}.out"), "rb") as f:
            raw = f.read()
            if not raw.endswith(b"\n") or raw.endswith(b"\n\n"):
                raise SystemExit(f"{i}.out newline rule")
        with open(os.path.join(data_dir, f"{i}.in"), encoding="utf-8") as f:
            if solve_line(f.read()) != open(
                os.path.join(data_dir, f"{i}.out"), encoding="utf-8"
            ).read():
                raise SystemExit(f"group {i} mismatch")
    with open(os.path.join(data_dir, "README.md"), "w", encoding="utf-8", newline="\n") as f:
        f.write("# P5108 测试数据\n\n主脚本：题目根 `gen.py`。\n\n")
        f.write("| # | 说明 |\n|---|------|\n")
        for i, (note, _) in enumerate(generators, 1):
            f.write(f"| {i} | {note} |\n")
    print("P5108 data ok")


if __name__ == "__main__":
    main()
