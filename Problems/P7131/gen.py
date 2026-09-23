# -*- coding: utf-8 -*-
"""P7131 造数：二叉搜索树第 cnt 大。

stdin：第一行 n cnt；第二行 n 个层序记号（数字或 null）。
输出：第 cnt 大的节点值。
`.in` 最后一行后不留换行；`.out` 末尾恰好一个换行。
"""
from __future__ import annotations

import random
import sys
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
from std import solve  # noqa: E402

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
RNG = random.Random(713120260914)

N_MAX = 10**4
V_LO, V_HI = -(10**9), 10**9


class T:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None


def insert(root, val):
    if root is None:
        return T(val)
    cur = root
    while True:
        if val < cur.val:
            if cur.left is None:
                cur.left = T(val)
                return root
            cur = cur.left
        else:
            if cur.right is None:
                cur.right = T(val)
                return root
            cur = cur.right


def from_sorted_balanced(arr, l, r):
    if l > r:
        return None
    mid = (l + r) // 2
    node = T(arr[mid])
    node.left = from_sorted_balanced(arr, l, mid - 1)
    node.right = from_sorted_balanced(arr, mid + 1, r)
    return node


def serialize(root):
    if root is None:
        return []
    q = [root]
    out = []
    while q:
        node = q.pop(0)
        if node is None:
            out.append("null")
            continue
        out.append(str(node.val))
        q.append(node.left)
        q.append(node.right)
    while out and out[-1] == "null":
        out.pop()
    return out


def naive(tokens, cnt):
    vals = [int(t) for t in tokens if t != "null"]
    vals.sort(reverse=True)
    return vals[cnt - 1]


def case_in_text(cnt, tokens):
    n = len(tokens)
    return f"{n} {cnt}\n" + " ".join(tokens)


def write_case(idx, cnt, tokens):
    n = len(tokens)
    vals = [int(t) for t in tokens if t != "null"]
    m = len(vals)
    assert 1 <= n <= N_MAX
    assert 1 <= cnt <= m
    assert all(V_LO <= v <= V_HI for v in vals)
    assert len(set(vals)) == m
    (DATA / f"{idx}.in").write_bytes(case_in_text(cnt, tokens).encode("utf-8"))
    ans = solve(tokens, cnt)
    expect = naive(tokens, cnt)
    assert ans == expect, (idx, ans, expect)
    with open(DATA / f"{idx}.out", "w", encoding="utf-8", newline="\n") as f:
        f.write(str(ans) + "\n")
    return ans


def bst_from_seq(seq):
    root = None
    for v in seq:
        root = insert(root, v)
    return serialize(root)


def main():
    DATA.mkdir(parents=True, exist_ok=True)

    sample1 = ["7", "3", "9", "1", "5"]
    sample2 = ["10", "5", "15", "2", "7", "null", "20", "1", "null", "6", "8"]

    chain_left = bst_from_seq(list(range(12, 0, -1)))
    chain_right = bst_from_seq(list(range(1, 13)))

    mixed_vals = [-9, -4, 0, 3, 8]
    mixed_tokens = serialize(from_sorted_balanced(mixed_vals, 0, len(mixed_vals) - 1))

    rand_vals = RNG.sample(range(-500, 501), 40)
    rand_tokens = bst_from_seq(rand_vals)
    rand_m = sum(t != "null" for t in rand_tokens)
    rand_cnt = 1 + RNG.randrange(rand_m)

    big_m = 8191
    big_vals = list(range(1, big_m + 1))
    big_tokens = serialize(from_sorted_balanced(big_vals, 0, big_m - 1))
    assert len(big_tokens) <= N_MAX

    chain_m = 5000
    chain_tokens = bst_from_seq(list(range(1, chain_m + 1)))
    assert len(chain_tokens) <= N_MAX

    plan = [
        (2, sample1,
         "样例 1", "第 $2$ 大是 $7$",
         "求成第 $2$ 小会得到 $3$"),
        (4, sample2,
         "样例 2，层序含 $null$", "第 $4$ 大是 $8$",
         "建树时左右孩子对调，或把 $null$ 当数字"),
        (1, ["42"],
         "单节点，$cnt=1$", "答案就是 $42$",
         "去读不存在的左右孩子"),
        (1, ["5", "3", "7", "1", "4", "6", "9"],
         "满二叉树，$cnt=1$ 取最大", "答案 $9$",
         "走成左-根-右，得到最小值 $1$"),
        (7, ["5", "3", "7", "1", "4", "6", "9"],
         "满二叉树，$cnt=m$ 取最小", "答案 $1$",
         "下标写成 $cnt$ 而不是 $m-cnt$"),
        (3, chain_left,
         "左偏链 $m=12$", "从大到小第 $3$ 个",
         "递归深链爆栈；或只看根"),
        (12, chain_right,
         "右偏链，$cnt=m$ 取最小", "答案 $1$",
         "只沿着右孩子走，漏掉没有的左子树"),
        (2, mixed_tokens,
         "含负数与 $0$", "第 $2$ 大是 $3$",
         "把负数当更小关键字排反"),
        (2, big_tokens,
         "压满平衡树 $m=8191$", "第 $2$ 大是 $8190$",
         "层序解析错位导致整棵树烂掉"),
        (chain_m // 2, chain_tokens,
         "压满右链 $m=5000$，层序约 $10^4$", "第 $2500$ 大",
         "真递归中序在链上爆栈或 TLE"),
    ]
    assert len(plan) == 10

    answers = []
    for idx, (cnt, tokens, _, _, _) in enumerate(plan, 1):
        answers.append(write_case(idx, cnt, tokens))

    for i, (cnt, tokens, _, _, _) in enumerate(plan, 1):
        ib = (DATA / f"{i}.in").read_bytes()
        ob = (DATA / f"{i}.out").read_bytes()
        assert not ib.endswith(b"\n") and b"\r" not in ib, f"{i}.in"
        assert ob.endswith(b"\n") and not ob.endswith(b"\n\n") and b"\r" not in ob
        text = ib.decode("utf-8")
        lines = text.split("\n")
        hn, hc = map(int, lines[0].split())
        got_tok = lines[1].split()
        assert hn == len(tokens) == len(got_tok) and hc == cnt
        assert got_tok == tokens
        got = int(ob.decode("utf-8").strip())
        assert got == answers[i - 1] == naive(tokens, cnt)

    assert answers[0] == 7
    assert answers[1] == 8
    assert answers[2] == 42
    assert answers[3] == 9
    assert answers[4] == 1
    assert answers[8] == 8190

    rows = []
    for i, (_, _, scale, goal, hack) in enumerate(plan, 1):
        rows.append(f"| {i} | {scale} | {goal} | {hack} |")

    readme = "\n".join([
        "# P7131 测试数据说明",
        "",
        "主造数脚本：题目根目录 `gen.py`。",
        "stdin：第一行 `n cnt`；第二行 $n$ 个层序记号（整数或 `null`）。",
        "输出：BST 中第 $cnt$ 大的节点值。",
        "",
        r"题面未写 $n$ 与值域。本套按 $1\le n\le 10^4$，$-10^9\le a_i\le 10^9$，节点值互异，$1\le cnt\le m$。",
        "",
        "| 组别 | 规模/分布 | 目标 | 卡掉的错误解 |",
        "|---|---|---|---|",
        *rows,
        "",
        "`.in` 最后一行后无换行符；`.out` 末尾恰好一个换行符。",
        "",
        "生成后自校验：树求解必须等于把非空节点值降序排序后的第 $cnt$ 个。",
        "",
    ])
    (DATA / "README.md").write_text(readme, encoding="utf-8")
    print("generated 10 cases")
    for i, ans in enumerate(answers, 1):
        print(i, "ans", ans)


if __name__ == "__main__":
    main()
