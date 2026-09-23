# -*- coding: utf-8 -*-
"""P14396 测试数据生成。stdin 一行：n,duration,deadline,profit。"""
import ast
import os
import random
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)
from std import Solution

RNG = random.Random(14396001)


def format_in(n, duration, deadline, profit):
    def arr(a):
        return "[" + ",".join(str(x) for x in a) + "]"

    return f"{n},{arr(duration)},{arr(deadline)},{arr(profit)}"


def format_out(value: int) -> str:
    return f"{value}\n"


def _split_top_level_commas(s: str):
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


def _parse_line(line: str):
    line = line.strip("\r\n")
    parts = _split_top_level_commas(line)
    duration = ast.literal_eval(parts[1])
    deadline = ast.literal_eval(parts[2])
    profit = ast.literal_eval(parts[3])
    return duration, deadline, profit


def solve_line(line: str) -> str:
    duration, deadline, profit = _parse_line(line)
    ans = Solution().maximumProfit(duration, deadline, profit)
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


def gen_random(n, max_val=1000):
    duration = [RNG.randint(1, max_val) for _ in range(n)]
    deadline = [RNG.randint(1, max_val) for _ in range(n)]
    profit = [RNG.randint(1, max_val) for _ in range(n)]
    return format_in(n, duration, deadline, profit)


def gen_greedy_deadline_trap():
    """hack：仅按截止时间贪心，先做长任务会错过高收益短截止任务。"""
    return format_in(2, [3, 1], [100, 2], [10, 100])


def gen_greedy_profit_trap():
    """hack：仅按收益贪心，长高收益任务挤掉多个中等收益任务。"""
    return format_in(3, [5, 2, 2], [10, 4, 6], [50, 40, 45])


def gen_all_impossible_except_one():
    n = 5
    duration = [10] * n
    deadline = [5] * n
    profit = [100] * n
    duration[-1] = 3
    deadline[-1] = 100
    profit[-1] = 999
    return format_in(n, duration, deadline, profit)


def gen_max_n():
    n = 20
    duration = [RNG.randint(1, 1000) for _ in range(n)]
    deadline = [RNG.randint(1, 1000) for _ in range(n)]
    profit = [RNG.randint(1, 1000) for _ in range(n)]
    return format_in(n, duration, deadline, profit)


def main():
    data_dir = os.path.join(ROOT, "data")
    os.makedirs(data_dir, exist_ok=True)
    generators = [
        ("样例1", lambda: "3,[2,1,3],[3,2,5],[10,20,30]"),
        ("样例2", lambda: "4,[1,2,3,4],[1,3,6,10],[100,200,300,400]"),
        ("样例3", lambda: "2,[5,5],[4,10],[100,200]"),
        ("n=1 可完成", lambda: format_in(1, [2], [5], [88])),
        ("n=1 必超时", lambda: format_in(1, [10], [3], [500])),
        ("hack：截止时间贪心", gen_greedy_deadline_trap),
        ("hack：收益贪心", gen_greedy_profit_trap),
        ("随机 n=8", lambda: gen_random(8, 200)),
        ("仅一任务有收益", gen_all_impossible_except_one),
        ("极限 n=20", gen_max_n),
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
        f.write("# P14396 测试数据\n\n主脚本：题目根 `gen.py`。\n\n")
        f.write("| # | 说明 |\n|---|------|\n")
        for i, (note, _) in enumerate(generators, 1):
            f.write(f"| {i} | {note} |\n")
    print("P14396 data ok")


if __name__ == "__main__":
    main()
