# -*- coding: utf-8 -*-
"""P2984 测试数据。stdin 一行："A","B"。"""
import os
import random
import re
import string
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)
from std import Solution

RNG = random.Random(2984001)


def format_in(a, b):
    return f'"{a}","{b}"'


def format_out(ans):
    return str(ans) + "\n"


def solve_line(line):
    line = line.strip("\r\n")
    m = re.fullmatch(r'"(.*)"\s*,\s*"(.*)"', line)
    if not m:
        raise SystemExit(f"bad line: {line!r}")
    return format_out(Solution().countFormableGroups(m.group(1), m.group(2)))


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


def rand_unique_b(n):
    letters = list(string.ascii_lowercase)
    RNG.shuffle(letters)
    return "".join(letters[:n])


def rand_a(n):
    return "".join(RNG.choice(string.ascii_lowercase) for _ in range(n))


def main():
    data_dir = os.path.join(ROOT, "data")
    os.makedirs(data_dir, exist_ok=True)

    b9 = rand_unique_b(5)
    a9 = rand_a(80)
    b10 = rand_unique_b(9)
    a10 = rand_a(99)

    generators = [
        ("样例1", lambda: format_in("badc", "bac")),
        ("样例2", lambda: format_in("badc", "abc")),
        ("样例3", lambda: format_in("aabbcxd", "abcd")),
        ("样例4", lambda: format_in("ababcecfdc", "abc")),
        ("样例5", lambda: format_in("aaa", "a")),
        ("B 单字母多次", lambda: format_in("ababab", "ab")),
        ("无法形成", lambda: format_in("cba", "abc")),
        ("A 几乎全用完", lambda: format_in("abcabcabc", "abc")),
        ("随机中等", lambda: format_in(a9, b9)),
        ("接近上限", lambda: format_in(a10, b10)),
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
        f.write("# P2984 测试数据\n\n主脚本：题目根 `gen.py`。\n\n")
        f.write("| # | 说明 |\n|---|------|\n")
        for i, (note, _) in enumerate(generators, 1):
            f.write(f"| {i} | {note} |\n")

    print("P2984 data ok")


if __name__ == "__main__":
    main()
