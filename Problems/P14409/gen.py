# -*- coding: utf-8 -*-
"""P14409 测试数据生成。stdin 一行：n,nums。"""
import ast
import os
import random
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)
from std import Solution

RNG = random.Random(14409001)


def format_input(n, nums):
    arr = "[" + ",".join(str(x) for x in nums) + "]"
    return f"{n},{arr}"


def format_output(ans):
    return f"{ans}\n"


def solve_line(line: str) -> str:
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
    nums = ast.literal_eval(parts[1])
    ans = Solution().minimizeRangeSum(n, nums)
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


def gen_random_case(n):
    nums = [RNG.randint(1, 10**9) for _ in range(n)]
    return format_input(n, nums)


def gen_max_stress():
    n = 100000
    nums = [RNG.randint(1, 10**9) for _ in range(n)]
    return format_input(n, nums)


def main():
    data_dir = os.path.join(ROOT, "data")
    os.makedirs(data_dir, exist_ok=True)
    generators = [
        ("样例1：一般划分", lambda: format_input(5, [10, 1, 5, 3, 8])),
        ("样例2：全相等分组", lambda: format_input(5, [1, 1, 9, 1, 9])),
        ("样例3：n=2 边界", lambda: format_input(2, [1, 2])),
        ("边界：全部相同", lambda: format_input(6, [7, 7, 7, 7, 7, 7])),
        ("边界：严格递增", lambda: format_input(8, [1, 2, 3, 4, 5, 6, 7, 8])),
        ("hack：未排序直接枚举", lambda: format_input(6, [100, 1, 50, 2, 49, 3])),
        ("hack：忽略全局 min/max 同组", lambda: format_input(4, [1, 50, 51, 100])),
        ("hack：n=2 特判遗漏", lambda: format_input(2, [1000000000, 1])),
        ("随机中等规模", lambda: gen_random_case(5000)),
        ("极限 n=100000", lambda: gen_max_stress()),
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
        f.write("# P14409 测试数据\n\n主脚本：题目根 `gen.py`。\n\n")
        f.write("| # | 说明 |\n|---|------|\n")
        for i, (note, _) in enumerate(generators, 1):
            f.write(f"| {i} | {note} |\n")
    print("P14409 data ok")


if __name__ == "__main__":
    main()
