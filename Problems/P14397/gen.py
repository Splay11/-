# -*- coding: utf-8 -*-
"""P14397 测试数据生成。stdin 一行双引号包裹的字符串字面量。"""
import os
import random
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)
from std import Solution

RNG = random.Random(14397001)
LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
DIGITS = "0123456789"


def format_in(s: str) -> str:
    return f'"{s}"'


def format_out(s: str) -> str:
    return f'"{s}"\n'


def solve_raw(s: str) -> str:
    return Solution().processString(s)


def solve_line(line: str) -> str:
    s = line.strip()
    if s.startswith('"') and s.endswith('"'):
        s = s[1:-1]
    return format_out(solve_raw(s))


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


def gen_only_letters(n):
    return "".join(RNG.choice(LETTERS) for _ in range(n))


def gen_only_digits(n):
    return "".join(RNG.choice(DIGITS) for _ in range(n))


def gen_mixed(n):
    chars = []
    for _ in range(n):
        if RNG.random() < 0.45:
            chars.append(RNG.choice(DIGITS))
        else:
            chars.append(RNG.choice(LETTERS))
    if not any(c.isdigit() for c in chars):
        chars[RNG.randrange(n)] = RNG.choice(DIGITS)
    if not any(c.isalpha() for c in chars):
        chars[RNG.randrange(n)] = RNG.choice(LETTERS)
    return "".join(chars)


def gen_max_stress():
    parts = []
    for i in range(25):
        parts.append(LETTERS[i % 26])
        parts.append("9")
    while len("".join(parts)) < 100:
        parts.append(RNG.choice(LETTERS))
        if len("".join(parts)) < 100:
            parts.append(str(RNG.randint(0, 9)))
    s = "".join(parts)[:100]
    if not any(c.isdigit() for c in s):
        s = s[:-1] + "9"
    if not any(c.isalpha() for c in s):
        s = "A" + s[1:]
    return s


def main():
    data_dir = os.path.join(ROOT, "data")
    os.makedirs(data_dir, exist_ok=True)
    generators = [
        ("样例1", lambda: format_in("A1B2C3")),
        ("样例2", lambda: format_in("ABC0123")),
        ("样例3", lambda: format_in("B")),
        ("只含数字", lambda: format_in("90531")),
        ("hack：数字为 0 不输出字母", lambda: format_in("A0B1C2")),
        ("hack：数字侧余下拼接", lambda: format_in("XY012")),
        ("hack：字母侧余下拼接", lambda: format_in("A1B2C")),
        ("hack：误把 0 当重复 1 次", lambda: format_in("Z0W1")),
        ("随机混合 50", lambda: format_in(gen_mixed(50))),
        ("极限长度 100 高重复", lambda: format_in(gen_max_stress())),
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
        f.write("# P14397 测试数据\n\n主脚本：题目根 `gen.py`。\n\n")
        f.write("| # | 说明 |\n|---|------|\n")
        for i, (note, _) in enumerate(generators, 1):
            f.write(f"| {i} | {note} |\n")
    print("P14397 data ok")


if __name__ == "__main__":
    main()
