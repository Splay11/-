# -*- coding: utf-8 -*-
"""P14406 测试数据生成。stdin 一行：[profiles],diff"""
import ast
import os
import random
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)
from std import Solution

RNG = random.Random(14406001)


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


def format_profiles(profiles):
    return "[" + ", ".join(str(x) for x in profiles) + "]"


def format_in(profiles, diff):
    return format_profiles(profiles) + "," + str(diff)


def format_out(val: int) -> str:
    return str(val) + "\n"


def solve_line(line: str) -> str:
    parts = split_top_level_commas(line.strip())
    profiles = ast.literal_eval(parts[0])
    diff = int(parts[1].strip())
    ans = Solution().countProfilePairs(profiles, diff)
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


def gen_arithmetic_chain(n, step):
    start = RNG.randint(-1000, 1000)
    return [start + i * step for i in range(n)]


def gen_random_case(n, diff):
    base = [RNG.randint(-10**6, 10**6) for _ in range(n)]
    if diff == 0:
        dup = RNG.choice(base)
        base.append(dup)
        RNG.shuffle(base)
        return base, 0
    uniq = set(base)
    while len(uniq) < min(n, max(2, n // 3)):
        x = RNG.randint(-10**6, 10**6)
        base.append(x)
        uniq.add(x)
    return base, diff


def gen_max_stress():
    n = 100000
    profiles = list(range(0, n))
    return profiles, 1


def main():
    data_dir = os.path.join(ROOT, "data")
    os.makedirs(data_dir, exist_ok=True)
    generators = [
        ("样例1：差为2的三组", lambda: format_in([1, 5, 3, 4, 2], 2)),
        ("样例2：diff=0重复档位", lambda: format_in([8, 8, 8, 10, 10, 12], 0)),
        ("样例3：负数等差链", lambda: format_in([-5, -3, -1, 1], 2)),
        ("边界：单元素diff>0", lambda: format_in([42], 5)),
        ("边界：全唯一diff=0", lambda: format_in([1, 2, 3, 4], 0)),
        ("hack：按下标配对会多计", lambda: format_in([1, 1, 3, 3], 2)),
        ("hack：diff=0只出现一次", lambda: format_in([5, 5, 7], 0)),
        ("负数与大diff", lambda: format_in([-2147483648, -2147483646, 0], 2)),
        ("随机中等规模", lambda: format_in(*gen_random_case(500, RNG.randint(1, 100)))),
        ("极限10万元素diff=1", lambda: format_in(*gen_max_stress())),
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
        f.write("# P14406 测试数据\n\n主脚本：题目根 `gen.py`。\n\n")
        f.write("| # | 说明 |\n|---|------|\n")
        for i, (note, _) in enumerate(generators, 1):
            f.write(f"| {i} | {note} |\n")
    print("P14406 data ok")


if __name__ == "__main__":
    main()
