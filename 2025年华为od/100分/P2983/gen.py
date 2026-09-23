# -*- coding: utf-8 -*-
"""P2983 测试数据。stdin 一行：双引号包裹的括号字符串。"""
import os
import random
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)
from std import Solution

RNG = random.Random(2983001)
LEFT = "([{"
RIGHT = ")]}"
PAIR = {")": "(", "]": "[", "}": "{"}
OPEN_OF = {"(": ")", "[": "]", "{": "}"}


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
    return format_out(Solution().maxBracketDepth(text))


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


def gen_valid(n, max_depth_hint=20):
    """生成大致长度 n 的合法括号串。"""
    stack = []
    out = []
    while len(out) + len(stack) < n:
        can_open = len(stack) < max_depth_hint and len(out) + len(stack) + 2 <= n
        can_close = bool(stack)
        if can_open and (not can_close or RNG.random() < 0.55):
            ch = RNG.choice(LEFT)
            stack.append(ch)
            out.append(ch)
        elif can_close:
            out.append(OPEN_OF[stack.pop()])
        else:
            break
    while stack:
        out.append(OPEN_OF[stack.pop()])
    return "".join(out)


def gen_invalid_mismatch():
    return "([{"


def gen_invalid_cross():
    return "([)]"


def main():
    data_dir = os.path.join(ROOT, "data")
    os.makedirs(data_dir, exist_ok=True)

    mid = gen_valid(2000, 50)
    big = gen_valid(100000, 200)

    generators = [
        ("样例1", lambda: format_in("[]")),
        ("样例2", lambda: format_in("([]{()})")),
        ("样例3", lambda: format_in("(]")),
        ("样例4", lambda: format_in("([)]")),
        ("样例5", lambda: format_in(")(")),
        ("空串", lambda: format_in("")),
        ("深嵌套同种", lambda: format_in("(" * 10 + ")" * 10)),
        ("hack：交叉闭合", lambda: format_in(gen_invalid_cross())),
        ("中等合法 n~2000", lambda: format_in(mid)),
        ("极限合法 n=100000", lambda: format_in(big)),
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
        f.write("# P2983 测试数据\n\n主脚本：题目根 `gen.py`。\n\n")
        f.write("| # | 说明 |\n|---|------|\n")
        for i, (note, _) in enumerate(generators, 1):
            f.write(f"| {i} | {note} |\n")

    print("P2983 data ok")


if __name__ == "__main__":
    main()
