# -*- coding: utf-8 -*-
"""P14398 测试数据生成。stdin 一行：[整数数组],base"""
import ast
import os
import random
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)
from std import Solution

RNG = random.Random(14398001)


def format_in(nums, base):
    return "[" + ",".join(str(x) for x in nums) + "]," + str(base)


def format_out(values):
    return "[" + ",".join(f'"{x}"' for x in values) + "]\n"


def solve_line(line: str) -> str:
    parts = []
    start = 0
    depth = 0
    s = line.strip()
    for i, c in enumerate(s):
        if c == "[":
            depth += 1
        elif c == "]":
            depth -= 1
        elif c == "," and depth == 0:
            parts.append(s[start:i])
            start = i + 1
    parts.append(s[start:])
    nums = ast.literal_eval(parts[0])
    base = int(parts[1].strip())
    ans = Solution().sortConvertedNums(nums, base)
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


def gen_random(n, base, lo=0, hi=10**6):
    return [RNG.randint(lo, hi) for _ in range(n)]


def gen_max_stress():
    base = 16
    nums = [RNG.randint(0, 10**6) for _ in range(100)]
    nums[RNG.randrange(100)] = 10**6
    nums[RNG.randrange(100)] = 0
    return nums, base


def main():
    data_dir = os.path.join(ROOT, "data")
    os.makedirs(data_dir, exist_ok=True)
    generators = [
        ("样例1", lambda: format_in([10, 25, 3, 15, 8], 16)),
        ("样例2", lambda: format_in([16, 256, 0, 16], 2)),
        ("单元素 0", lambda: format_in([0], 10)),
        ("全相同数值", lambda: format_in([7, 7, 7], 8)),
        ("hack：字典序≠数值序", lambda: format_in([100, 255], 16)),
        ("hack：升序误排", lambda: format_in([1, 1000, 50], 10)),
        ("hack：多个 0", lambda: format_in([0, 0, 1, 0], 8)),
        ("hack：二进制长串", lambda: format_in([524288, 1, 262144], 2)),
        ("随机中等 30", lambda: format_in(gen_random(30, 12), 12)),
        ("极限 n=100 base=16", lambda: (lambda t: format_in(t[0], t[1]))(gen_max_stress())),
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
        f.write("# P14398 测试数据\n\n主脚本：题目根 `gen.py`。\n\n")
        f.write("| # | 说明 |\n|---|------|\n")
        for i, (note, _) in enumerate(generators, 1):
            f.write(f"| {i} | {note} |\n")
    print("P14398 data ok")


if __name__ == "__main__":
    main()
