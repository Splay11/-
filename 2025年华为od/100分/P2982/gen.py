# -*- coding: utf-8 -*-
"""P2982 测试数据。stdin 一行：双引号包裹的空格分词字符串。"""
import os
import random
import string
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)
from std import Solution

RNG = random.Random(2982001)


def format_in(text):
    return '"' + text + '"'


def format_out(ans):
    return str(ans) + "\n"


def solve_line(line):
    line = line.strip("\r\n")
    if len(line) >= 2 and line[0] == '"' and line[-1] == '"':
        text = line[1:-1]
    else:
        text = line
    return format_out(Solution().countOpenSyllables(text))


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


def rand_word(n, pure=True):
    if pure:
        return "".join(RNG.choice(string.ascii_lowercase) for _ in range(n))
    chars = string.ascii_lowercase + "0123456789!"
    return "".join(RNG.choice(chars) for _ in range(n))


def main():
    data_dir = os.path.join(ROOT, "data")
    os.makedirs(data_dir, exist_ok=True)

    mid = " ".join(rand_word(RNG.randint(3, 8), RNG.random() < 0.7) for _ in range(80))
    big = " ".join(rand_word(RNG.randint(4, 12), RNG.random() < 0.75) for _ in range(400))

    generators = [
        ("样例1", lambda: format_in("ekam a ekac")),
        ("样例2", lambda: format_in("!ekam a ekekac")),
        ("基础：单单词 make", lambda: format_in("ekam")),
        ("无相对开音节", lambda: format_in("abc xyz")),
        ("含数字不反转", lambda: format_in("cake1 ekac")),
        ("hack：第三位为 r 不计入", lambda: format_in("erab")),
        ("重叠子串 keke", lambda: format_in("ekek")),
        ("多单词含 cake", lambda: format_in("a bike ekac")),
        ("中等随机", lambda: format_in(mid)),
        ("较大随机", lambda: format_in(big)),
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
        f.write("# P2982 测试数据\n\n主脚本：题目根 `gen.py`。\n\n")
        f.write("| # | 说明 |\n|---|------|\n")
        for i, (note, _) in enumerate(generators, 1):
            f.write(f"| {i} | {note} |\n")

    print("P2982 data ok")


if __name__ == "__main__":
    main()
