# -*- coding: utf-8 -*-
"""P5109 测试数据生成。stdin 单行："resA","resB" """
import ast
import os
import random
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)
from std import Solution

RNG = random.Random(5109001)


def format_in(resA, resB):
    return f'"{resA}","{resB}"'


def format_out(value):
    return f"{value}\n"


def parse_line(line):
    line = line.strip("\r\n")
    resA, resB = ast.literal_eval("[" + line + "]")
    return resA, resB


def solve_line(line):
    resA, resB = parse_line(line)
    ans = Solution().minDistinctAfterSwap(resA, resB)
    return format_out(ans)


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


def gen_large(n=100000):
    half = n // 2
    resA = "a" * half + "b" * (n - half)
    resB = "c" * half + "d" * (n - half)
    return resA, resB


def gen_random(nA, nB):
    pool = "abcdefghijklmnopqrstuvwxyz"
    return (
        "".join(RNG.choice(pool) for _ in range(nA)),
        "".join(RNG.choice(pool) for _ in range(nB)),
    )


def main():
    data_dir = os.path.join(ROOT, "data")
    os.makedirs(data_dir, exist_ok=True)
    generators = [
        ("样例1：无解", lambda: format_in("ac", "b")),
        ("样例2：最优为 2", lambda: format_in("abcc", "aab")),
        ("样例3：字符集不交", lambda: format_in("abcde", "fghij")),
        ("单字符交换可达 1", lambda: format_in("a", "b")),
        ("同字符交换 dA==dB", lambda: format_in("aaa", "aaa")),
        ("多种合法取最小为 1", lambda: format_in("ab", "ba")),
        (
            "hack：误用 countB 判断 A 侧新增",
            lambda: format_in("ab", "cd"),
        ),
        (
            "hack：初始 dA==dB 仍需枚举交换",
            lambda: format_in("aab", "bbc"),
        ),
        ("中等随机", lambda: format_in(*gen_random(5000, 5000))),
        ("极限 n=100000", lambda: format_in(*gen_large(100000))),
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
        f.write("# P5109 测试数据\n\n主脚本：题目根 `gen.py`。\n\n")
        f.write("| # | 说明 |\n|---|------|\n")
        for i, (note, _) in enumerate(generators, 1):
            f.write(f"| {i} | {note} |\n")
    print("P5109 data ok")


if __name__ == "__main__":
    main()
