# -*- coding: utf-8 -*-
import math
import random
from pathlib import Path

from std import max_depth

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
DATA.mkdir(exist_ok=True)
rng = random.Random(5363)


def dump(idx, t, note):
    ans = max_depth(t)
    (DATA / f"{idx}.in").write_bytes(t.encode("utf-8"))
    (DATA / f"{idx}.out").write_bytes((str(ans) + "\n").encode("utf-8"))
    print(f"case {idx}: len={len(t)} ans={ans} note={note}")


def chain_left(n):
    parts = ["1"]
    for i in range(2, n + 1):
        parts.append(str(i))
        parts.append("#")
    return "{" + ",".join(parts) + "}"


def chain_right(n):
    parts = ["1"]
    for i in range(2, n + 1):
        parts.append("#")
        parts.append(str(i))
    return "{" + ",".join(parts) + "}"


def complete(n):
    parts = [str(i) for i in range(1, n + 1)]
    return "{" + ",".join(parts) + "}"


class Node:
    def __init__(self, v):
        self.v = v
        self.l = None
        self.r = None


def serialize(root):
    if root is None:
        return "{}"
    from collections import deque
    q = deque([root])
    out = []
    while q:
        x = q.popleft()
        if x is None:
            out.append("#")
        else:
            out.append(str(x.v))
            q.append(x.l)
            q.append(x.r)
    while out and out[-1] == "#":
        out.pop()
    return "{" + ",".join(out) + "}"


def random_tree(n):
    nodes = [Node(rng.randint(1, 10**9)) for _ in range(n)]
    slots = [0]
    for i in range(1, n):
        p = slots[rng.randrange(len(slots))]
        if nodes[p].l is None and nodes[p].r is None:
            if rng.random() < 0.5:
                nodes[p].l = nodes[i]
            else:
                nodes[p].r = nodes[i]
        elif nodes[p].l is None:
            nodes[p].l = nodes[i]
            slots.remove(p)
        else:
            nodes[p].r = nodes[i]
            slots.remove(p)
        slots.append(i)
    return serialize(nodes[0])


dump(1, "{5,#,8,6}", "样例1")
dump(2, "{9}", "样例2")
dump(3, "{}", "样例3 空树")
dump(4, "{7,2,4}", "满两层")
dump(5, "{8,3,1,#,#,9}", "原题形态换值")
dump(6, chain_left(20), "左链 20")
dump(7, chain_right(15), "右链 15")
dump(8, random_tree(80), "随机 80")
dump(9, complete(100000), "完全树 1e5")
dump(10, chain_left(100000), "左链 1e5 卡递归")

assert max_depth("{1,2,3,#,#,4}") == 3
assert max_depth("{}") == 0
assert max_depth(complete(100000)) == int(math.floor(math.log2(100000))) + 1

for i in range(1, 11):
    t = (DATA / f"{i}.in").read_bytes().decode("utf-8")
    got = str(max_depth(t)) + "\n"
    exp = (DATA / f"{i}.out").read_bytes().decode("utf-8")
    assert got == exp, i
    inn = (DATA / f"{i}.in").read_bytes()
    assert not inn.endswith(b"\n"), i
    out = (DATA / f"{i}.out").read_bytes()
    assert out.endswith(b"\n") and not out.endswith(b"\n\n"), i

print("gen ok")
