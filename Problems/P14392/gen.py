# -*- coding: utf-8 -*-
"""P14392 测试数据生成。stdin 一行 fileIds,parentIds,targetId。"""
import ast
import os
import random
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)
from std import Solution

RNG = random.Random(14392001)


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
    file_ids = ast.literal_eval(parts[0])
    parent_ids = ast.literal_eval(parts[1])
    target_id = int(parts[2].strip())
    return file_ids, parent_ids, target_id


def format_in(file_ids, parent_ids, target_id):
    f = "[" + ",".join(str(x) for x in file_ids) + "]"
    p = "[" + ",".join(str(x) for x in parent_ids) + "]"
    return f"{f},{p},{target_id}"


def format_out(values):
    return "[" + ",".join(str(x) for x in values) + "]\n"


def solve_line(line: str) -> str:
    file_ids, parent_ids, target_id = parse_line(line)
    ans = Solution().getLoadedFileIds(file_ids, parent_ids, target_id)
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


def build_tree(n, shape="random"):
    """返回 fileIds, parentIds（1..n 或指定 id 集合）。"""
    if shape == "chain":
        file_ids = list(range(1, n + 1))
        parent_ids = [0] + file_ids[:-1]
        return file_ids, parent_ids
    if shape == "star":
        file_ids = list(range(2, n + 2))
        parent_ids = [1] * (n - 1) + [0]
        file_ids = [1] + file_ids
        parent_ids = [0] + [1] * (len(file_ids) - 1)
        return file_ids, parent_ids
    # random: 按 BFS 顺序挂到已有节点
    file_ids = []
    parent_ids = []
    nodes = [0]
    next_id = 1
    while len(file_ids) < n:
        parent = RNG.choice(nodes)
        file_ids.append(next_id)
        parent_ids.append(parent)
        nodes.append(next_id)
        next_id += 1
    return file_ids, parent_ids


def collect_subtree(file_ids, parent_ids, target):
    children = {}
    for fid, pid in zip(file_ids, parent_ids):
        children.setdefault(pid, []).append(fid)
    ans = []
    stack = [target]
    while stack:
        u = stack.pop()
        ans.append(u)
        for v in children.get(u, []):
            stack.append(v)
    return sorted(ans)


def gen_random_case(n, shape="random"):
    file_ids, parent_ids = build_tree(n, shape)
    target = RNG.choice(file_ids)
    return file_ids, parent_ids, target


def gen_hack_direct_children_only():
    """卡只取直接子节点：链 1-2-3-4，加载 1 应得四个 ID。"""
    file_ids = [1, 2, 3, 4]
    parent_ids = [0, 1, 2, 3]
    return file_ids, parent_ids, 1


def gen_hack_forget_target():
    """卡漏 target：叶节点 5。"""
    file_ids = [1, 2, 3, 4, 5]
    parent_ids = [0, 1, 1, 2, 2]
    return file_ids, parent_ids, 5


def main():
    data_dir = os.path.join(ROOT, "data")
    os.makedirs(data_dir, exist_ok=True)
    compile_src = os.path.join(ROOT, "..", "..", "核心代码模式模板", "compile.sh")
    compile_dst = os.path.join(data_dir, "compile.sh")
    with open(compile_src, "rb") as fsrc:
        data = fsrc.read()
    with open(compile_dst, "wb") as fdst:
        fdst.write(data)

    generators = [
        ("样例1", lambda: format_in(*parse_line("[1,2,3,4,5,6,7],[0,1,1,2,2,3,0],2"))),
        ("样例2 叶节点", lambda: format_in([1, 2, 3], [0, 1, 1], 3)),
        ("样例3 链式子树", lambda: format_in([1, 2, 3, 4], [0, 1, 2, 3], 1)),
        ("单节点", lambda: format_in([42], [0], 42)),
        ("根下兄弟 加载7", lambda: format_in([1, 2, 3, 4, 5, 6, 7], [0, 1, 1, 2, 2, 3, 0], 7)),
        ("hack 链式全后代", lambda: format_in(*gen_hack_direct_children_only())),
        ("hack 叶仅自身", lambda: format_in(*gen_hack_forget_target())),
        ("随机树 n=120", lambda: format_in(*gen_random_case(120))),
        ("随机树 n=500", lambda: format_in(*gen_random_case(500, "star"))),
        ("极限 n=1000 链", lambda: format_in(*build_tree(1000, "chain") + (500,))),
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
            if not raw.endswith(b"\n") or raw.count(b"\n") != 1:
                raise SystemExit(f"{i}.out must end with exactly one newline")
        with open(os.path.join(data_dir, f"{i}.in"), encoding="utf-8") as f:
            got = solve_line(f.read())
        with open(os.path.join(data_dir, f"{i}.out"), encoding="utf-8") as f:
            exp = f.read()
        if got != exp:
            raise SystemExit(f"group {i} mismatch: {got!r} vs {exp!r}")
    with open(os.path.join(data_dir, "README.md"), "w", encoding="utf-8", newline="\n") as f:
        f.write("# P14392 测试数据\n\n主脚本：题目根 `gen.py`。\n\n")
        f.write("| # | 说明 |\n|---|------|\n")
        for i, (note, _) in enumerate(generators, 1):
            f.write(f"| {i} | {note} |\n")
    print("P14392 data ok")


if __name__ == "__main__":
    main()
