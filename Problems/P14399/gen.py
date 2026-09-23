# -*- coding: utf-8 -*-
"""P14399 测试数据生成。stdin 一行：[loads],[[edges]]"""
import ast
import os
import random
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)
from std import Solution

RNG = random.Random(14399001)


def format_in(loads, edges):
    loads_s = "[" + ",".join(str(x) for x in loads) + "]"
    if not edges:
        edges_s = "[]"
    else:
        edges_s = "[" + ",".join("[" + ",".join(str(x) for x in e) + "]" for e in edges) + "]"
    return loads_s + "," + edges_s


def format_out(val: int) -> str:
    return str(val) + "\n"


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


def solve_line(line: str) -> str:
    parts = split_top_level_commas(line.strip())
    loads = ast.literal_eval(parts[0])
    edges = ast.literal_eval(parts[1])
    ans = Solution().maxZoneImbalance(loads, edges)
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


def gen_chain_edges(n):
    return [[i, i + 1] for i in range(n - 1)]


def gen_random_graph(n, m):
    edges = set()
    while len(edges) < m:
        u = RNG.randrange(n)
        v = RNG.randrange(n)
        if u == v:
            continue
        a, b = (u, v) if u < v else (v, u)
        edges.add((a, b))
    return [[a, b] for a, b in sorted(edges)]


def gen_max_stress():
    n = 100
    loads = [RNG.randint(0, 10000) for _ in range(n)]
    loads[0] = 0
    loads[99] = 10000
    edges = gen_chain_edges(n)
    extra = min(n * (n - 1) // 2 - (n - 1), 200)
    for u, v in gen_random_graph(n, extra):
        edges.append([u, v])
    return loads, edges


def main():
    data_dir = os.path.join(ROOT, "data")
    os.makedirs(data_dir, exist_ok=True)
    generators = [
        ("样例1", lambda: format_in([100, 200, 150, 50, 300], [[0, 1], [1, 2], [3, 4]])),
        ("样例2", lambda: format_in([80, 90, 80, 90], [[0, 1], [1, 2], [2, 3]])),
        ("样例3", lambda: format_in([100, 200, 300], [])),
        ("两节点相同负载", lambda: format_in([5000, 5000], [[0, 1]])),
        ("hack：全局最值误用", lambda: format_in([0, 100, 50, 10000], [[0, 1], [2, 3]])),
        ("hack：忘记乘节点数", lambda: format_in([0, 10000], [[0, 1]])),
        ("hack：M=0 无有效区", lambda: format_in([1, 2, 3, 4], [])),
        ("hack：大区负载全相同", lambda: format_in([5, 5, 5, 5], [[0, 1], [1, 2], [2, 3]])),
        ("随机中等 n=30", lambda: (lambda t: format_in(t[0], t[1]))(
            ([RNG.randint(0, 10000) for _ in range(30)], gen_random_graph(30, 40))
        )),
        ("极限 n=100 满负载差", lambda: (lambda t: format_in(t[0], t[1]))(gen_max_stress())),
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
        f.write("# P14399 测试数据\n\n主脚本：题目根 `gen.py`。\n\n")
        f.write("| # | 说明 |\n|---|------|\n")
        for i, (note, _) in enumerate(generators, 1):
            f.write(f"| {i} | {note} |\n")
    print("P14399 data ok")


if __name__ == "__main__":
    main()
