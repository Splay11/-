# -*- coding: utf-8 -*-
import random
import sys
from collections import deque
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from std import TreeNode, solve_line, tree_depth

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
DATA.mkdir(exist_ok=True)
rng = random.Random(5386)


def serialize(root):
    if root is None:
        return "{}"
    q = deque([root])
    toks = []
    while q:
        node = q.popleft()
        if node is None:
            toks.append("#")
        else:
            toks.append(str(node.val))
            q.append(node.left)
            q.append(node.right)
    while toks and toks[-1] == "#":
        toks.pop()
    return "{" + ",".join(toks) + "}"


def dump(idx, line, note):
    ans = solve_line(line)
    (DATA / f"{idx}.in").write_bytes(line.encode("utf-8"))
    (DATA / f"{idx}.out").write_bytes((str(ans) + "\n").encode("utf-8"))
    print(f"case {idx}: ans={ans} toks={line.count(',')+1} note={note}")


def val():
    return rng.randint(-1000, 1000)


def complete(k):
    # k 个结点的完全二叉树
    nodes = [TreeNode(val()) for _ in range(k)]
    for i in range(k):
        li, ri = 2 * i + 1, 2 * i + 2
        if li < k:
            nodes[i].left = nodes[li]
        if ri < k:
            nodes[i].right = nodes[ri]
    return nodes[0]


def left_chain(k):
    nodes = [TreeNode(val()) for _ in range(k)]
    for i in range(k - 1):
        nodes[i].left = nodes[i + 1]
    return nodes[0]


def right_chain(k):
    nodes = [TreeNode(val()) for _ in range(k)]
    for i in range(k - 1):
        nodes[i].right = nodes[i + 1]
    return nodes[0]


def random_tree(k):
    nodes = [TreeNode(val()) for _ in range(k)]
    for i in range(1, k):
        p = rng.randrange(i)
        if nodes[p].left is None and nodes[p].right is None:
            if rng.random() < 0.5:
                nodes[p].left = nodes[i]
            else:
                nodes[p].right = nodes[i]
        elif nodes[p].left is None:
            nodes[p].left = nodes[i]
        elif nodes[p].right is None:
            nodes[p].right = nodes[i]
        else:
            # 找一个还有空位的父亲
            for j in range(i):
                if nodes[j].left is None:
                    nodes[j].left = nodes[i]
                    break
                if nodes[j].right is None:
                    nodes[j].right = nodes[i]
                    break
    return nodes[0]


dump(1, "{8,4,6}", "样例1 两层")
dump(2, "{2,#,8,#,9}", "样例2 右链")
dump(3, "{5}", "样例3 单点")
dump(4, serialize(complete(3)), "三结点完全树")
dump(5, serialize(left_chain(4)), "短左链，卡深度少 1")
dump(6, serialize(random_tree(8)), "小随机，卡把 # 当实灯")
dump(7, "{10,#,11,12}", "左空右再分叉")
dump(8, serialize(complete(15)), "满 4 层")
dump(9, serialize(right_chain(5000)), "n=5000 右链压测")
dump(10, serialize(complete(8191)), "完全树约 10^4 项压测")

ok = True
for i in range(1, 11):
    raw = (DATA / f"{i}.in").read_bytes().decode("utf-8")
    got = solve_line(raw)
    exp = int((DATA / f"{i}.out").read_text(encoding="utf-8").strip())
    ntok = 0 if raw in ("{}",) else raw.count(",") + 1
    if ntok > 10000:
        print("TOO LONG", i, ntok)
        ok = False
    if got != exp:
        print("MISMATCH", i, got, exp)
        ok = False
if not ok:
    raise SystemExit(1)
print("ok")
