# -*- coding: utf-8 -*-
"""P2981 测试数据生成。stdin 一行：[h1,h2,...]。"""
import os
import random
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)
from std import Solution

RNG = random.Random(2981001)


def format_in(heights):
    return "[" + ",".join(str(x) for x in heights) + "]"


def format_out(ans):
    return str(ans) + "\n"


def solve_line(line):
    heights = eval(line.strip())
    return format_out(Solution().maxSolarPanelArea(heights))


def write_in(path, text):
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text.rstrip("\n"))


def write_out(path, text):
    if not text.endswith("\n"):
        text += "\n"
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)


def write_config_yaml(data_dir):
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


def main():
    data_dir = os.path.join(ROOT, "data")
    os.makedirs(data_dir, exist_ok=True)

    h9 = [RNG.randint(1, 1000) for _ in range(2000)]
    h10 = [RNG.randint(1, 10**9) for _ in range(10000)]

    generators = [
        ("样例1", lambda: format_in([10, 9, 8, 7, 6, 5, 4, 3, 2, 1])),
        ("基础：仅两根", lambda: format_in([3, 7])),
        ("递增序列", lambda: format_in([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])),
        ("全等高", lambda: format_in([5, 5, 5, 5, 5])),
        ("两端最高", lambda: format_in([100, 1, 1, 1, 100])),
        ("hack：中间局部最优", lambda: format_in([1, 8, 6, 2, 5, 4, 8, 3, 7])),
        ("短数组随机", lambda: format_in([RNG.randint(1, 100) for _ in range(8)])),
        ("单峰值", lambda: format_in([1, 3, 5, 9, 7, 4, 2])),
        ("中等 n=2000", lambda: format_in(h9)),
        ("极限 n=10000", lambda: format_in(h10)),
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
        f.write("# P2981 测试数据\n\n主脚本：题目根 `gen.py`。\n\n")
        f.write("| # | 说明 |\n|---|------|\n")
        for i, (note, _) in enumerate(generators, 1):
            f.write(f"| {i} | {note} |\n")

    print("P2981 data ok")


if __name__ == "__main__":
    main()
