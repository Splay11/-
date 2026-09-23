# -*- coding: utf-8 -*-
"""P14404 测试数据生成。stdin 一行：[[max,min,base],...],station_capacity"""
import ast
import os
import random
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)
from std import Solution

RNG = random.Random(14404001)


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


def format_sub_arrays(rows):
    inner = []
    for row in rows:
        inner.append("[" + ",".join(str(x) for x in row) + "]")
    return "[" + ",".join(inner) + "]"


def format_in(sub_arrays, station_capacity):
    return format_sub_arrays(sub_arrays) + "," + str(station_capacity)


def format_out(values):
    return "[" + ",".join(str(x) for x in values) + "]\n"


def solve_line(line: str) -> str:
    parts = split_top_level_commas(line.strip())
    sub_arrays = ast.literal_eval(parts[0])
    station_capacity = int(parts[1].strip())
    ans = Solution().predictGeneration(sub_arrays, station_capacity)
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


def gen_random_case(n, cap_scale):
    rows = []
    for _ in range(n):
        mn = RNG.randint(100, 5000)
        mx = mn + RNG.randint(100, 50000)
        base = RNG.randint(mn, mx)
        rows.append([mx, mn, base])
    total = sum(r[2] for r in rows)
    station = max(1, int(total * RNG.uniform(0.7, 1.3)))
    return rows, station


def gen_max_stress():
    rows = []
    for i in range(1000):
        mn = 1000000 + (i % 1000)
        mx = mn + 500000
        base = mn + (i * 37) % (mx - mn + 1)
        rows.append([mx, mn, base])
    total = sum(r[2] for r in rows)
    station = total - 100000000
    return rows, station


def main():
    data_dir = os.path.join(ROOT, "data")
    os.makedirs(data_dir, exist_ok=True)
    generators = [
        ("样例1：无需调整", lambda: format_in(
            [[1000, 800, 900], [1200, 900, 1100], [800, 600, 700]], 2800
        )),
        ("样例2：基准等于总下限", lambda: format_in(
            [[1000, 800, 800], [1200, 900, 900], [800, 600, 600]], 2600
        )),
        ("样例3：按比例缩减", lambda: format_in(
            [[1000, 800, 900], [1200, 900, 1100], [800, 600, 700]], 2500
        )),
        ("样例4：无法缩减返回全0", lambda: format_in(
            [[100, 80, 80], [100, 80, 80]], 150
        )),
        ("放大场景", lambda: format_in(
            [[1000, 800, 700], [1200, 900, 800]], 3000
        )),
        ("hack：单个子阵缩减", lambda: format_in([[1000, 200, 900]], 700)),
        ("hack：误用 floor 而非 ceil", lambda: format_in(
            [[100, 10, 50], [100, 10, 50]], 80
        )),
        ("边界：单元素无需调整", lambda: format_in([[1000, 500, 800]], 900)),
        ("随机中等规模", lambda: format_in(*gen_random_case(50, 1))),
        ("极限1000子阵大容量缩减", lambda: format_in(*gen_max_stress())),
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
        f.write("# P14404 测试数据\n\n主脚本：题目根 `gen.py`。\n\n")
        f.write("| # | 说明 |\n|---|------|\n")
        for i, (note, _) in enumerate(generators, 1):
            f.write(f"| {i} | {note} |\n")
    print("P14404 data ok")


if __name__ == "__main__":
    main()
