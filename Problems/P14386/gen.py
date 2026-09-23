# -*- coding: utf-8 -*-
"""P14386 测试数据生成。stdin 一行 [t0,t1,...]。"""
import os
import random
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)
from std import Solution

RNG = random.Random(14386001)


def format_in(arr):
    return "[" + ",".join(str(x) for x in arr) + "]"


def solve_line(line: str) -> str:
    arr = __import__("ast").literal_eval(line.strip("\r\n"))
    ans = Solution().longestValidSkillChain(arr)
    return str(ans) + "\n"


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


def gen_random(n, allow012=True):
    if allow012:
        return [RNG.randint(0, 2) for _ in range(n)]
    return [RNG.randint(0, 1) for _ in range(n)]


def gen_alternating01(m):
    return [i % 2 for i in range(m)]


def main():
    data_dir = os.path.join(ROOT, "data")
    os.makedirs(data_dir, exist_ok=True)
    generators = [
        ("样例1 全0", lambda: format_in([0, 0, 0])),
        ("样例2 0-1交替", lambda: format_in([0, 1, 0, 1])),
        ("样例3 首2", lambda: format_in([2, 0, 0])),
        ("样例4 含高级", lambda: format_in([0, 1, 0, 0, 2])),
        ("空数组", lambda: format_in([])),
        ("单元素非法", lambda: format_in([1])),
        ("hack：两扩展夹基础", lambda: format_in([0, 1, 1, 0])),
        ("hack：0-2-0 非法高级", lambda: format_in([0, 2, 0])),
        ("随机 n=500", lambda: format_in(gen_random(500))),
        ("极限 n=2000", lambda: format_in(gen_random(2000))),
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
        f.write("# P14386 测试数据\n\n主脚本：题目根 `gen.py`。\n\n")
        f.write("| # | 说明 |\n|---|------|\n")
        for i, (note, _) in enumerate(generators, 1):
            f.write(f"| {i} | {note} |\n")
    print("P14386 data ok")


if __name__ == "__main__":
    main()
