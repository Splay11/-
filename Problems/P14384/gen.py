# -*- coding: utf-8 -*-
"""P14384 测试数据生成。stdin 一行 N,M,[[AT,CT,WT],...]。"""
import os
import random
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)
from std import Solution

RNG = random.Random(14384001)


def format_in(n, cars):
    inner = "[" + ",".join("[" + ",".join(str(x) for x in c) + "]" for c in cars) + "]"
    return f"{n},{len(cars)},{inner}"


def parse_line(line: str):
    line = line.strip("\r\n")
    p1 = line.index(",")
    p2 = line.index(",", p1 + 1)
    n = int(line[:p1])
    cars = __import__("ast").literal_eval(line[p2 + 1 :])
    return n, cars


def solve_line(line: str) -> str:
    n, cars = parse_line(line)
    ans = Solution().countFailedCharging(n, cars)
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


def gen_random_cars(m, at_max=10000):
    cars = []
    for _ in range(m):
        at = RNG.randint(1, at_max)
        ct = RNG.randint(1, min(10000, 500))
        wt = RNG.randint(0, 10000)
        cars.append([at, ct, wt])
    return cars


def main():
    data_dir = os.path.join(ROOT, "data")
    os.makedirs(data_dir, exist_ok=True)
    generators = [
        ("样例1 五车同到", lambda: format_in(3, [[10, 1, 0]] * 5)),
        ("样例2 等待超时", lambda: format_in(2, [[1, 10, 0], [2, 2, 1], [3, 1, 0], [4, 1, 0]])),
        ("单桩单车", lambda: format_in(1, [[1, 5, 0]])),
        ("单桩三车 WT=0", lambda: format_in(1, [[1, 2, 0], [1, 2, 0], [1, 2, 0]])),
        ("可等待成功", lambda: format_in(1, [[1, 5, 0], [6, 1, 10]])),
        ("hack：忽略 FCFS 顺序", lambda: format_in(2, [[1, 3, 0], [1, 3, 0], [4, 1, 0], [4, 1, 0]])),
        ("长充电占桩", lambda: format_in(2, [[1, 100, 0], [2, 1, 50], [50, 1, 0]])),
        ("WT 极大链式等待", lambda: format_in(1, [[i, 1, 10000] for i in range(1, 21)])),
        ("随机 M=200", lambda: format_in(RNG.randint(5, 50), gen_random_cars(200, 5000))),
        ("极限 N=100 M=1000", lambda: format_in(100, gen_random_cars(1000, 10000))),
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
        f.write("# P14384 测试数据\n\n主脚本：题目根 `gen.py`。\n\n")
        f.write("| # | 说明 |\n|---|------|\n")
        for i, (note, _) in enumerate(generators, 1):
            f.write(f"| {i} | {note} |\n")
    print("P14384 data ok")


if __name__ == "__main__":
    main()
