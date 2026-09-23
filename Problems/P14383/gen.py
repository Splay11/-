# -*- coding: utf-8 -*-
"""P14383 测试数据生成。stdin 一行 [..],minInterval。"""
import os
import random
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)
from std import Solution

RNG = random.Random(14383001)


def format_in(ts, k):
    return "[" + ",".join(str(x) for x in ts) + "]," + str(k)


def solve_line(line: str) -> str:
    line = line.strip("\r\n")
    d = 0
    end = -1
    for i, c in enumerate(line):
        if c == "[":
            d += 1
        elif c == "]":
            d -= 1
            if d == 0:
                end = i
                break
    arr_s = line[: end + 1]
    k = int(line[end + 1 :].strip()[1:])
    ts = [int(x.strip()) for x in arr_s[1:-1].split(",") if x.strip() != ""]
    if arr_s == "[]":
        ts = []
    ans = Solution().countValidPlans(ts, k)
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


def gen_random(n, k):
    used = set()
    ts = []
    while len(ts) < n:
        v = RNG.randint(0, 10**6)
        if v not in used:
            used.add(v)
            ts.append(v)
    return format_in(ts, k)


def main():
    data_dir = os.path.join(ROOT, "data")
    os.makedirs(data_dir, exist_ok=True)
    generators = [
        ("样例1", lambda: format_in([1, 2, 4], 2)),
        ("样例2 单点", lambda: format_in([10], 5)),
        ("n=1", lambda: format_in([0], 1)),
        ("全间隔够大", lambda: format_in([0, 100, 200], 50)),
        ("hack：相邻差1", lambda: format_in([1, 2, 3, 4], 2)),
        ("乱序输入", lambda: format_in([9, 1, 5, 3], 2)),
        ("minInterval 大", lambda: format_in([1, 2, 3], 100)),
        ("n=15 边界", lambda: format_in(list(range(0, 30, 2)), 2)),
        ("随机 n=12", lambda: gen_random(12, RNG.randint(2, 20))),
        ("随机 n=15 满", lambda: gen_random(15, RNG.randint(1, 5))),
    ]
    for i, (_, gen) in enumerate(generators, start=1):
        inp = gen()
        write_in(os.path.join(data_dir, f"{i}.in"), inp)
        write_out(os.path.join(data_dir, f"{i}.out"), solve_line(inp))
    write_config_yaml(data_dir)
    for i in range(1, 11):
        with open(os.path.join(data_dir, f"{i}.in"), "rb") as f:
            if f.read().endswith(b"\n"):
                raise SystemExit(f"{i}.in newline")
        with open(os.path.join(data_dir, f"{i}.out"), "rb") as f:
            raw = f.read()
            if not raw.endswith(b"\n") or raw.endswith(b"\n\n"):
                raise SystemExit(f"{i}.out newline")
        with open(os.path.join(data_dir, f"{i}.in"), encoding="utf-8") as f:
            if solve_line(f.read()) != open(os.path.join(data_dir, f"{i}.out"), encoding="utf-8").read():
                raise SystemExit(f"group {i} mismatch")
    with open(os.path.join(data_dir, "README.md"), "w", encoding="utf-8", newline="\n") as f:
        f.write("# P14383 测试数据\n\n主脚本：`gen.py`。\n")
    print("P14383 data ok")


if __name__ == "__main__":
    main()
