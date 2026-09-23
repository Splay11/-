# -*- coding: utf-8 -*-
"""P14405 测试数据生成。stdin 一行：[nums],k"""
import ast
import os
import random
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)
from std import Solution

RNG = random.Random(14405001)


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


def format_nums(nums):
    return "[" + ", ".join(str(x) for x in nums) + "]"


def format_in(nums, k):
    return format_nums(nums) + "," + str(k)


def format_out(val: int) -> str:
    return str(val) + "\n"


def solve_line(line: str) -> str:
    parts = split_top_level_commas(line.strip())
    nums = ast.literal_eval(parts[0])
    k = int(parts[1].strip())
    ans = Solution().minimumLatency(nums, k)
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


def gen_random_case(n, k):
    nums = [RNG.randint(0, 10**6) for _ in range(n)]
    k = min(k, n)
    k = max(1, k)
    return nums, k


def gen_max_stress():
    n = 1000
    nums = [10**6] * n
    return nums, 500


def main():
    data_dir = os.path.join(ROOT, "data")
    os.makedirs(data_dir, exist_ok=True)
    generators = [
        ("样例1：两通道最优18", lambda: format_in([7, 2, 5, 10, 8], 2)),
        ("样例2：划分为[1,2,3]与[4,5]", lambda: format_in([1, 2, 3, 4, 5], 2)),
        ("样例3：每包一通道", lambda: format_in([1, 4, 4], 3)),
        ("边界：k=1整段传输", lambda: format_in([7, 2, 5, 10, 8], 1)),
        ("边界：k=n单包通道", lambda: format_in([7, 2, 5, 10, 8], 5)),
        ("全零数组", lambda: format_in([0, 0, 0, 0], 2)),
        ("hack：误用段数==k而非<=k", lambda: format_in([10, 20, 30, 40], 3)),
        ("单元素", lambda: format_in([999999], 1)),
        ("随机中等规模", lambda: format_in(*gen_random_case(80, 15))),
        ("极限1000元素k=500", lambda: format_in(*gen_max_stress())),
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
        f.write("# P14405 测试数据\n\n主脚本：题目根 `gen.py`。\n\n")
        f.write("| # | 说明 |\n|---|------|\n")
        for i, (note, _) in enumerate(generators, 1):
            f.write(f"| {i} | {note} |\n")
    print("P14405 data ok")


if __name__ == "__main__":
    main()
