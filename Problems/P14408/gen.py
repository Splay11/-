# -*- coding: utf-8 -*-
"""P14408 测试数据生成。stdin 一行：n,k,weights,conflicts。"""
import ast
import os
import random
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)
from std import Solution

RNG = random.Random(14408001)


def format_input(n, k, weights, conflicts):
    w = "[" + ",".join(str(x) for x in weights) + "]"
    if conflicts:
        c = "[" + ",".join("[" + ",".join(str(x) for x in pair) + "]" for pair in conflicts) + "]"
    else:
        c = "[]"
    return f"{n},{k},{w},{c}"


def format_output(ans):
    if not ans:
        return "[]\n"
    inner = []
    for combo in ans:
        inner.append("[" + ",".join(str(x) for x in combo) + "]")
    return "[" + ",".join(inner) + "]\n"


def solve_line(line: str) -> str:
    parts = []
    start = 0
    depth = 0
    for i, c in enumerate(line):
        if c == "[":
            depth += 1
        elif c == "]":
            depth -= 1
        elif c == "," and depth == 0:
            parts.append(line[start:i])
            start = i + 1
    parts.append(line[start:])
    n = int(parts[0].strip())
    k = int(parts[1].strip())
    weights = ast.literal_eval(parts[2])
    conflicts = ast.literal_eval(parts[3])
    ans = Solution().selectMaxWeightPolicies(n, k, weights, conflicts)
    return format_output(ans)


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


def gen_random_case(n, k):
    weights = [RNG.randint(1, 1000) for _ in range(n)]
    edges = set()
    m = RNG.randint(0, min(n * (n - 1) // 2, n * 2))
    while len(edges) < m:
        a = RNG.randint(1, n)
        b = RNG.randint(1, n)
        if a == b:
            continue
        if a > b:
            a, b = b, a
        edges.add((a, b))
    conflicts = [[a, b] for a, b in sorted(edges)]
    return format_input(n, k, weights, conflicts)


def gen_max_stress():
    n = 25
    k = 12
    weights = [RNG.randint(800, 1000) for _ in range(n)]
    conflicts = []
    for i in range(1, n, 2):
        if i + 1 <= n:
            conflicts.append([i, i + 1])
    return format_input(n, k, weights, conflicts)


def main():
    data_dir = os.path.join(ROOT, "data")
    os.makedirs(data_dir, exist_ok=True)
    generators = [
        ("样例1：单最优组合", lambda: format_input(4, 2, [5, 1, 3, 4], [[1, 2], [2, 3]])),
        ("样例2：多最优组合字典序", lambda: format_input(5, 3, [3, 4, 3, 4, 3], [[1, 3], [2, 4], [3, 5]])),
        ("样例3：完全图无合法解", lambda: format_input(3, 2, [10, 10, 10], [[1, 2], [1, 3], [2, 3]])),
        ("边界：k=0 空组合", lambda: format_input(4, 0, [5, 1, 3, 4], [[1, 2], [2, 3]])),
        ("边界：无互斥边", lambda: format_input(4, 2, [1, 100, 2, 99], [])),
        ("hack：忽略互斥关系", lambda: format_input(4, 2, [5, 1, 3, 4], [[1, 2], [2, 3], [1, 3]])),
        ("hack：只输出一个最优解", lambda: format_input(6, 2, [5, 5, 5, 5, 5, 5], [[1, 2], [3, 4], [5, 6]])),
        ("多解同权字典序", lambda: format_input(5, 2, [10, 10, 10, 10, 10], [[1, 2], [3, 4]])),
        ("随机中等规模", lambda: gen_random_case(15, 7)),
        ("极限 n=25 k=12", lambda: gen_max_stress()),
    ]
    for i, (_, gen) in enumerate(generators, start=1):
        inp = gen()
        write_in(os.path.join(data_dir, f"{i}.in"), inp)
        write_out(os.path.join(data_dir, f"{i}.out"), solve_line(inp))
    write_config_yaml(data_dir)
    repo_compile = os.path.normpath(os.path.join(ROOT, "..", "..", "compile.sh"))
    if not os.path.isfile(repo_compile):
        raise SystemExit(f"missing compile.sh: {repo_compile}")
    with open(repo_compile, "rb") as src, open(os.path.join(data_dir, "compile.sh"), "wb") as dst:
        dst.write(src.read())
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
        f.write("# P14408 测试数据\n\n主脚本：题目根 `gen.py`。\n\n")
        f.write("| # | 说明 |\n|---|------|\n")
        for i, (note, _) in enumerate(generators, 1):
            f.write(f"| {i} | {note} |\n")
    print("P14408 data ok")


if __name__ == "__main__":
    main()
