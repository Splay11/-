# -*- coding: utf-8 -*-
"""P14393 测试数据生成。stdin 一行 resourceCount,conflicts0,conflicts1,..."""
import ast
import os
import random
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)
from std import Solution

RNG = random.Random(14393001)


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


def parse_line(line: str):
    line = line.strip("\r\n")
    parts = split_top_level_commas(line)
    resource_count = ast.literal_eval(parts[0])
    conflicts = [ast.literal_eval(p) if p else [] for p in parts[1:]]
    normalized = []
    for group in conflicts:
        normalized.append([[int(a), int(b)] for a, b in group])
    return resource_count, normalized


def format_in(resource_count, conflicts):
    parts = ["[" + ",".join(str(x) for x in resource_count) + "]"]
    for group in conflicts:
        if not group:
            parts.append("[]")
        else:
            inner = ",".join(f"({a},{b})" for a, b in group)
            parts.append(f"[{inner}]")
    return ",".join(parts)


def format_out(values):
    return "[" + ",".join(str(x) for x in values) + "]\n"


def solve_line(line: str) -> str:
    rc, conflicts = parse_line(line)
    ans = Solution().canIsolateWithTwoPools(rc, conflicts)
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


def gen_bipartite_edges(n, m):
    left = list(range(1, n // 2 + 1))
    right = list(range(n // 2 + 1, n + 1))
    if not left or not right:
        left = [1]
        right = [2] if n >= 2 else []
    edges = []
    seen = set()
    tries = 0
    while len(edges) < m and tries < m * 20:
        tries += 1
        u = RNG.choice(left)
        v = RNG.choice(right) if right else RNG.randint(1, n)
        if u == v:
            continue
        key = (min(u, v), max(u, v))
        if key in seen:
            continue
        seen.add(key)
        edges.append([u, v])
    return edges


def gen_odd_cycle(n):
    n = max(3, n)
    edges = [[i, i % n + 1] for i in range(1, n + 1)]
    return edges


def gen_random_case(groups, max_n=500, max_edges_per_group=2000):
    rc = [RNG.randint(2, max_n) for _ in range(groups)]
    conflicts = []
    for n in rc:
        if RNG.random() < 0.15:
            u = RNG.randint(1, n)
            conflicts.append([[u, u]])
        elif RNG.random() < 0.25:
            k = min(n, RNG.randint(3, 7))
            conflicts.append(gen_odd_cycle(k))
        else:
            m = RNG.randint(0, min(max_edges_per_group, n * 3))
            conflicts.append(gen_bipartite_edges(n, m))
    return rc, conflicts


def gen_max_case():
    groups = 100
    rc = []
    conflicts = []
    total_v = 0
    total_e = 0
    for _ in range(groups):
        remain_v = 100000 - total_v
        remain_e = 200000 - total_e
        if remain_v <= 0 or remain_e <= 0:
            break
        n = min(1000, remain_v // max(1, groups - len(rc)))
        n = max(2, n)
        m = min(2000, remain_e // max(1, groups - len(conflicts)), n * 4)
        rc.append(n)
        conflicts.append(gen_bipartite_edges(n, m))
        total_v += n
        total_e += len(conflicts[-1])
    while len(rc) < groups and total_v < 100000:
        n = min(10000, 100000 - total_v)
        rc.append(max(2, n))
        m = min(2000, 200000 - total_e, rc[-1] * 4)
        conflicts.append(gen_bipartite_edges(rc[-1], m))
        total_v += rc[-1]
        total_e += len(conflicts[-1])
    return rc, conflicts


def main():
    data_dir = os.path.join(ROOT, "data")
    os.makedirs(data_dir, exist_ok=True)
    generators = [
        ("样例1", lambda: format_in(*parse_line("[4,3,5],[(1,2),(1,3),(2,4)],[(1,2),(2,3),(1,3)],[(1,2),(3,4)]"))),
        ("样例2", lambda: format_in(*parse_line("[2,2,4],[(1,2)],[],[(1,2),(2,3),(3,4),(4,1)]"))),
        ("样例3", lambda: format_in(*parse_line("[3,4],[(1,1)],[(1,2),(2,3),(3,1)]"))),
        ("单组无边", lambda: format_in([5], [[]])),
        ("单组一条边", lambda: format_in([2], [[(1, 2)]])),
        ("hack：自环", lambda: format_in([4], [[(2, 2), (1, 3)]])),
        ("hack：三角形奇环", lambda: format_in([3], [[(1, 2), (2, 3), (3, 1)]])),
        ("hack：偶数环", lambda: format_in([4], [[(1, 2), (2, 3), (3, 4), (4, 1)]])),
        ("随机 20 组", lambda: format_in(*gen_random_case(20, max_n=200, max_edges_per_group=500))),
        ("极限规模", lambda: format_in(*gen_max_case())),
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
        f.write("# P14393 测试数据\n\n主脚本：题目根 `gen.py`。\n\n")
        f.write("| # | 说明 |\n|---|------|\n")
        for i, (note, _) in enumerate(generators, 1):
            f.write(f"| {i} | {note} |\n")
    print("P14393 data ok")


if __name__ == "__main__":
    main()
