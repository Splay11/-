# -*- coding: utf-8 -*-
"""P14402 测试数据生成。stdin 一行：[data],[[ops]]"""
import ast
import os
import random
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)
from std import Solution

RNG = random.Random(14402001)


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


def format_in(data, operations):
    d = "[" + ",".join(str(x) for x in data) + "]"
    if not operations:
        o = "[]"
    else:
        rows = ["[" + ",".join(str(x) for x in row) + "]" for row in operations]
        o = "[" + ",".join(rows) + "]"
    return d + "," + o


def format_out(values):
    return "[" + ",".join(str(x) for x in values) + "]\n"


def solve_line(line: str) -> str:
    parts = split_top_level_commas(line.strip())
    data = ast.literal_eval(parts[0])
    operations = ast.literal_eval(parts[1])
    ans = Solution().processDataArray(data, operations)
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


def gen_random_data(n):
    pool = [0, 1, -1, 2, 3, 7, 15, 127, 128, 255, 1024, -128, -2147483648, 2147483647]
    data = [RNG.choice(pool) if RNG.random() < 0.4 else RNG.randint(-1000, 1000) for _ in range(n)]
    return data


def gen_random_ops(data_len, k):
    ops = []
    for _ in range(k):
        i = RNG.randrange(data_len) if data_len else 0
        j = RNG.randrange(data_len) if data_len else 0
        ops.append([i, j])
    return ops


def gen_max_stress():
    data = []
    for p in range(30):
        data.append(1 << p)
    data.extend([0, -1, -2147483648, 2147483647])
    while len(data) < 100:
        data.append(RNG.randint(-(1 << 20), (1 << 20) - 1))
    data = data[:100]
    ops = []
    cur = len(data)
    for _ in range(10):
        if cur <= 0:
            break
        i = RNG.randrange(cur)
        j = RNG.randrange(cur)
        ops.append([i, j])
        cur = cur - (1 if i == j else 2) + 1
    return data, ops


def main():
    data_dir = os.path.join(ROOT, "data")
    os.makedirs(data_dir, exist_ok=True)
    generators = [
        ("样例1", lambda: format_in([3, 2, 1], [[0, 1]])),
        ("样例2", lambda: format_in(
            [1024, 512, 256, 128, 64, 32, 16, 8, 4, 2, 1, 0, -1],
            [[0, 1], [0, 1], [0, 1], [1, 2]],
        )),
        ("样例3", lambda: format_in([2147483647, -2147483648, -1, 0], [[1, 2], [2, 2]])),
        ("空数组无操作", lambda: format_in([], [])),
        ("仅排序无操作", lambda: format_in([3, 1, 2], [])),
        ("hack：同下标只删一个", lambda: format_in([1, 2, 4], [[1, 1]])),
        ("hack：负数须按32位计1", lambda: format_in([-1, 0, 1], [[0, 2]])),
        ("hack：popcount相同按值升序", lambda: format_in([3, 1, 5, 2], [[0, 1]])),
        ("随机中等规模", lambda: format_in(gen_random_data(40), gen_random_ops(40, 5))),
        ("极限100元素10次操作", lambda: format_in(*gen_max_stress())),
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
        f.write("# P14402 测试数据\n\n主脚本：题目根 `gen.py`。\n\n")
        f.write("| # | 说明 |\n|---|------|\n")
        for i, (note, _) in enumerate(generators, 1):
            f.write(f"| {i} | {note} |\n")
    print("P14402 data ok")


if __name__ == "__main__":
    main()
