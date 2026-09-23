# -*- coding: utf-8 -*-
"""P14411 测试数据生成。stdin 一行：{层次遍历树},threshold。"""
import os
import random
import sys
from collections import deque

ROOT = os.path.dirname(os.path.abspath(__file__))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)
from std import Solution, TreeNode

RNG = random.Random(14411001)
INT_MIN = -2147483648


def format_tree(root):
    if root is None:
        return "{}"
    tokens = []
    q = deque([root])
    while q:
        node = q.popleft()
        if node is None:
            tokens.append("#")
            continue
        tokens.append(str(node.val))
        q.append(node.left)
        q.append(node.right)
    while tokens and tokens[-1] == "#":
        tokens.pop()
    return "{" + ",".join(tokens) + "}"


def format_input(root, threshold):
    return format_tree(root) + "," + str(threshold)


def format_output(ans):
    return "[" + ",".join(str(x) for x in ans) + "]\n"


def solve_line(line: str) -> str:
    line = line.strip("\r\n")
    depth = 0
    end = -1
    for i, ch in enumerate(line):
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                end = i
                break
    tree_str = line[: end + 1]
    threshold = int(line[end + 2 :].strip())

    def build_tree(s):
        s = s.strip()
        if s in ("{}", "{#}"):
            return None
        inner = s[1:-1].strip()
        if inner == "" or inner == "#":
            return None
        toks = [t.strip() for t in inner.split(",")]
        if toks[0] == "#":
            return None
        r = TreeNode(int(toks[0]))
        q = deque([r])
        idx = 1
        while q and idx < len(toks):
            node = q.popleft()
            if idx < len(toks):
                t = toks[idx]
                idx += 1
                if t != "#":
                    node.left = TreeNode(int(t))
                    q.append(node.left)
            if idx < len(toks):
                t = toks[idx]
                idx += 1
                if t != "#":
                    node.right = TreeNode(int(t))
                    q.append(node.right)
        return r

    root = build_tree(tree_str)
    ans = Solution().analyzeSpiritPaths(root, threshold)
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


def make_sample1():
    # 10 / -5,20 / #,8 / -6,15
    root = TreeNode(10)
    root.left = TreeNode(-5)
    root.right = TreeNode(20)
    root.left.right = TreeNode(8)
    root.right.left = TreeNode(-6)
    root.right.right = TreeNode(15)
    return root, 40


def make_sample2():
    root = TreeNode(-5)
    root.left = TreeNode(-3)
    root.left.right = TreeNode(-7)
    return root, -100


def make_sample3():
    root = TreeNode(5)
    root.left = TreeNode(-3)
    root.left.right = TreeNode(8)
    root.left.right.left = TreeNode(-2)
    root.left.right.left.right = TreeNode(10)
    return root, 18


def make_empty():
    return None, 0


def make_single(pos=True):
    v = 7 if pos else -4
    return TreeNode(v), 0


def make_all_invalid_chain():
    root = TreeNode(-1)
    root.left = TreeNode(-2)
    root.left.left = TreeNode(-3)
    return root, -1000


def make_intermittent_neg():
    root = TreeNode(1)
    root.left = TreeNode(-1)
    root.right = TreeNode(2)
    root.left.right = TreeNode(3)
    root.right.right = TreeNode(-1)
    root.right.right.right = TreeNode(4)
    return root, 5


def make_threshold_edge():
    root = TreeNode(10)
    root.left = TreeNode(5)
    root.right = TreeNode(20)
    return root, 15


def make_random(n_nodes):
    if n_nodes <= 0:
        return None
    vals = [RNG.randint(-100, 100) for _ in range(n_nodes)]
    nodes = [TreeNode(v) for v in vals]
    for i in range(n_nodes):
        li = 2 * i + 1
        ri = 2 * i + 2
        if li < n_nodes:
            nodes[i].left = nodes[li]
        if ri < n_nodes:
            nodes[i].right = nodes[ri]
    return nodes[0], RNG.randint(-1000, 1000)


def make_skewed_chain(depth):
    root = cur = TreeNode(RNG.randint(0, 50))
    prev_neg = False
    for _ in range(depth - 1):
        if prev_neg:
            v = RNG.randint(0, 50)
        else:
            v = RNG.choice([RNG.randint(0, 50), RNG.randint(-100, -1)])
        child = TreeNode(v)
        cur.right = child
        cur = child
        prev_neg = v < 0
    return root, 0


def make_large(n):
    vals = [RNG.randint(-100, 100) for _ in range(n)]
    nodes = [TreeNode(v) for v in vals]
    for i in range(n):
        li = 2 * i + 1
        ri = 2 * i + 2
        if li < n:
            nodes[i].left = nodes[li]
        if ri < n:
            nodes[i].right = nodes[ri]
    return nodes[0], 10**9


def main():
    data_dir = os.path.join(ROOT, "data")
    os.makedirs(data_dir, exist_ok=True)
    generators = [
        ("样例1：三路径", lambda: format_input(*make_sample1())),
        ("样例2：连续负全非法", lambda: format_input(*make_sample2())),
        ("样例3：间隔负合法", lambda: format_input(*make_sample3())),
        ("边界：空树", lambda: format_input(*make_empty())),
        ("边界：单结点负", lambda: format_input(*make_single(False))),
        ("hack：链式连续负", lambda: format_input(*make_all_invalid_chain())),
        ("hack：间隔负与多叶", lambda: format_input(*make_intermittent_neg())),
        ("hack：阈值边界", lambda: format_input(*make_threshold_edge())),
        ("随机中等规模", lambda: format_input(*make_random(500))),
        ("极限 n=100000", lambda: format_input(*make_large(100000))),
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
        f.write("# P14411 测试数据\n\n主脚本：题目根 `gen.py`。\n\n")
        f.write("| # | 说明 |\n|---|------|\n")
        for i, (note, _) in enumerate(generators, 1):
            f.write(f"| {i} | {note} |\n")
    print("P14411 data ok")


if __name__ == "__main__":
    main()
