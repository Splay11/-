# -*- coding: utf-8 -*-
"""P14400 测试数据生成。stdin 一行：双引号字符串,整数 n。"""
import ast
import os
import random
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)
from std import Solution

RNG = random.Random(14400001)
LETTERS = "abcdefghijklmnopqrstuvwxyz"


def format_in(s: str, n: int) -> str:
    return f'"{s}",{n}'


def format_out(s: str) -> str:
    return f'"{s}"\n'


def solve_raw(s: str, n: int) -> str:
    return Solution().processChunks(s, n)


def solve_line(line: str) -> str:
    line = line.strip()
    s, n = ast.literal_eval("(" + line + ")")
    return format_out(solve_raw(s, n))


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


def gen_random_string(length: int) -> str:
    return "".join(RNG.choice(LETTERS) for _ in range(length))


def gen_max_stress():
    s = "abcdefghijklmnopqrstuvwxyz" * 38 + "abc"
    s = s[:1000]
    return s, 37


def main():
    data_dir = os.path.join(ROOT, "data")
    os.makedirs(data_dir, exist_ok=True)
    generators = [
        ("样例1", lambda: format_in("abaabacbda", 3)),
        ("样例2", lambda: format_in("aaabbb", 2)),
        ("样例3", lambda: format_in("a", 1)),
        ("样例4", lambda: format_in("a", 1000)),
        ("hack：保留首次而非末次", lambda: format_in("aba", 3)),
        ("hack：整串去重而非分块", lambda: format_in("aaabbb", 2)),
        ("hack：n=1 每字符一块", lambda: format_in("aaa", 1)),
        ("hack：末块不足 n", lambda: format_in("abcd", 3)),
        ("随机中等 500", lambda: format_in(gen_random_string(500), RNG.randint(1, 50))),
        ("极限 |s|=1000", lambda: (lambda sn: format_in(sn[0], sn[1]))(gen_max_stress())),
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
        f.write("# P14400 测试数据\n\n主脚本：题目根 `gen.py`。\n\n")
        f.write("| # | 说明 |\n|---|------|\n")
        for i, (note, _) in enumerate(generators, 1):
            f.write(f"| {i} | {note} |\n")
    print("P14400 data ok")


if __name__ == "__main__":
    main()
