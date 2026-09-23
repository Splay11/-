# -*- coding: utf-8 -*-
"""P14401 测试数据生成。stdin 一行：n,w,[scores...]。"""
import os
import random
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)
from std import Solution

RNG = random.Random(14401001)


def format_in(n: int, w: int, scores: list) -> str:
    return f"{n},{w},[{','.join(str(x) for x in scores)}]"


def format_out(ans: list) -> str:
    return "[" + ",".join(str(x) for x in ans) + "]\n"


def solve_raw(n: int, w: int, scores: list) -> list:
    return Solution().findMaintenanceWindow(n, w, scores)


def solve_line(line: str) -> str:
    line = line.strip("\r\n")
    parts = []
    start = 0
    depth = 0
    for i, c in enumerate(line):
        if c == "[":
            depth += 1
        elif c == "]":
            depth -= 1
        elif c == "," and depth == 0:
            parts.append(line[start:i])
            start = i + 1
    parts.append(line[start:])
    n = int(parts[0].strip())
    w = int(parts[1].strip())
    scores = eval(parts[2].strip())
    return format_out(solve_raw(n, w, scores))


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


def gen_scores(n: int, zero_prob: float) -> list:
    scores = []
    for _ in range(n):
        if RNG.random() < zero_prob:
            scores.append(0)
        else:
            scores.append(RNG.randint(1, 1000))
    return scores


def gen_all_valid_block(n: int, w: int) -> list:
    scores = [0] * n
    start = RNG.randint(0, max(0, n - w))
    for i in range(start, start + w):
        scores[i] = RNG.randint(1, 1000)
    for i in range(n):
        if scores[i] == 0 and RNG.random() < 0.35:
            scores[i] = RNG.randint(1, 1000)
    return scores


def gen_max_stress():
    n = 100000
    w = 10000
    scores = [0] * n
    block_start = RNG.randint(0, n - w)
    for i in range(block_start, block_start + w):
        scores[i] = RNG.randint(1, 1000)
    for i in range(0, n, 17):
        if i < block_start or i >= block_start + w:
            if RNG.random() < 0.2:
                scores[i] = RNG.randint(1, 1000)
    return n, w, scores


def main():
    data_dir = os.path.join(ROOT, "data")
    os.makedirs(data_dir, exist_ok=True)

    s1 = [10, 5, 20, 10, 5, 15, 10, 5, 25]
    s2 = [0, 5, 0, 8, 12]
    s3 = [10, 2, 1, 0, 15, 0, 8, 3, 6, 12, 6, 9]
    tie = [5, 10, 5, 10, 5, 10]
    w1 = [7, 0, 9]

    n9, w9 = 5000, 500
    scores9 = gen_all_valid_block(n9, w9)

    generators = [
        ("样例1", lambda: format_in(9, 2, s1)),
        ("样例2", lambda: format_in(5, 3, s2)),
        ("样例3", lambda: format_in(12, 4, s3)),
        ("基础：单元素窗口", lambda: format_in(3, 1, w1)),
        ("hack：同和取最早起始", lambda: format_in(6, 2, tie)),
        ("hack：零过多无合法窗口", lambda: format_in(8, 4, [0, 0, 1, 0, 0, 2, 0, 0])),
        ("hack：整段窗口", lambda: format_in(5, 5, [3, 7, 2, 9, 1])),
        ("hack：忽略 0 仍计入窗口", lambda: format_in(4, 2, [8, 0, 6, 4])),
        ("随机中等规模", lambda: format_in(n9, w9, scores9)),
        ("极限 n=100000 w=10000", lambda: format_in(*gen_max_stress())),
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
            if solve_line(f.read()) != open(os.path.join(data_dir, f"{i}.out"), encoding="utf-8").read():
                raise SystemExit(f"group {i} mismatch")

    with open(os.path.join(data_dir, "README.md"), "w", encoding="utf-8", newline="\n") as f:
        f.write("# P14401 测试数据\n\n主脚本：题目根 `gen.py`。\n\n")
        f.write("| # | 说明 |\n|---|------|\n")
        for i, (note, _) in enumerate(generators, 1):
            f.write(f"| {i} | {note} |\n")

    print("P14401 data ok")


if __name__ == "__main__":
    main()
