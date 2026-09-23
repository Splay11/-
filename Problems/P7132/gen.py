# -*- coding: utf-8 -*-
"""P7132 造数：根到叶子路径和等于 targetSum。

stdin：第一行 n targetSum；n>0 时第二行 n 个层序记号；n=0 时第二行省略。
输出：第一行 k，随后 k 行路径；无路径只输出 0。
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
RNG = random.Random(713220260914)

M_MAX = 5000
V_LO, V_HI = -1000, 1000
T_LO, T_HI = -1000, 1000


class T:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None


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


def complete_from(vals):
    if not vals:
        return []
    nodes = [T(v) for v in vals]
    for i, node in enumerate(nodes):
        l, r = 2 * i + 1, 2 * i + 2
        if l < len(nodes):
            node.left = nodes[l]
        if r < len(nodes):
            node.right = nodes[r]
    return serialize(nodes[0])


def chain_left(vals):
    root = T(vals[0])
    cur = root
    for v in vals[1:]:
        cur.left = T(v)
        cur = cur.left
    return serialize(root)


def naive(tokens, target):
    """按同样层序建树后 DFS，用于对拍。"""
    if not tokens or tokens[0] == "null":
        return []
    vals = []
    nodes = []
    root_v = int(tokens[0])
    class N:
        def __init__(self, v):
            self.val = v
            self.left = None
            self.right = None
    root = N(root_v)
    q = [root]
    i = 1
    idx = 0
    while idx < len(q) and i < len(tokens):
        cur = q[idx]
        idx += 1
        if i < len(tokens):
            if tokens[i] != "null":
                cur.left = N(int(tokens[i]))
                q.append(cur.left)
            i += 1
        if i < len(tokens):
            if tokens[i] != "null":
                cur.right = N(int(tokens[i]))
                q.append(cur.right)
            i += 1
    ans = []
    path = []

    def dfs(node, remain):
        if node is None:
            return
        path.append(node.val)
        remain -= node.val
        if node.left is None and node.right is None:
            if remain == 0:
                ans.append(list(path))
        else:
            dfs(node.left, remain)
            dfs(node.right, remain)
        path.pop()

    dfs(root, target)
    return ans


def nonempty_count(tokens):
    return sum(t != "null" for t in tokens)


def case_in_text(n, target, tokens):
    if n == 0:
        return f"{n} {target}"
    return f"{n} {target}\n" + " ".join(tokens)


def format_out(paths):
    lines = [str(len(paths))]
    for p in paths:
        lines.append(" ".join(map(str, p)))
    return "\n".join(lines) + "\n"


def write_case(idx, target, tokens):
    n = len(tokens)
    m = nonempty_count(tokens)
    assert 0 <= m <= M_MAX
    assert T_LO <= target <= T_HI
    for t in tokens:
        if t != "null":
            v = int(t)
            assert V_LO <= v <= V_HI
    (DATA / f"{idx}.in").write_bytes(case_in_text(n, target, tokens).encode("utf-8"))
    ans = solve(tokens, target)
    expect = naive(tokens, target)
    assert ans == expect, (idx, ans[:3], expect[:3])
    with open(DATA / f"{idx}.out", "w", encoding="utf-8", newline="\n") as f:
        f.write(format_out(ans))
    return ans


def main():
    DATA.mkdir(parents=True, exist_ok=True)

    sample1 = "5 4 8 11 null 13 4 7 2 null null 5 1".split()
    sample2 = ["1", "2", "3"]
    sample3 = ["1", "2"]

    two_paths = ["1", "2", "3", "4", "5", "null", "0"]
    # 1-2-4=7, 1-2-5=8, 1-3-0=4；target 7 只有左路一条；改 target 让两条都中
    # 用 1, 2, 2, 3, 3 满三层：1-2-3 和 1-2-3 两条相同值，顺序仍先左后右
    twin = ["5", "3", "3", "1", "1", "1", "1"]
    # 5-3-1=9 四条叶子都是 9

    neg = ["1", "-2", "3", "-3", "4"]
    # 1-(-2)-(-3)=-4；1-(-2)-4=3；1-3=4（3 是叶子? 3 有没有孩子：层序 1 -2 3 -3 4
    #   1
    # -2   3
    # -3 4
    # 3 是叶子。路径：1-2? 1,-2,-3 和 1,-2,4 和 1,3

    chain = chain_left([10, -3, 2, -1, 5])
    # 10-3+2-1+5=13

    small_rand = complete_from([RNG.randint(-20, 20) for _ in range(15)])

    big_miss = complete_from([1] * 4095)
    # 路径长 12，和恒为 12，target 0 一条都没有

    big_hit_vals = [RNG.randint(-10, 10) for _ in range(5000)]
    big_hit = complete_from(big_hit_vals)
    # 选一条真实叶子路径的和当代 target，保证至少有解
    probe = solve(big_hit, 10**9)  # 极大目标和，通常 0 条
    # 自己走一条最左路径求和
    def leftmost_sum(vals):
        s = 0
        i = 0
        while i < len(vals):
            s += vals[i]
            i = 2 * i + 1
        return s
    big_target = leftmost_sum(big_hit_vals)
    big_target = max(T_LO, min(T_HI, big_target))

    plan = [
        (22, sample1,
         "样例 1", "两条路径 $5\\ 4\\ 11\\ 2$ 与 $5\\ 8\\ 4\\ 5$",
         "先右后左会把顺序写反；漏掉 $5\\ 8\\ 4\\ 5$"),
        (5, sample2,
         "样例 2，两条叶子都不匹配", "只输出 $0$",
         "把 $1\\ 2$ 或 $1\\ 3$ 硬输出"),
        (0, sample3,
         "样例 3，$targetSum=0$ 但路径和为 $3$", "只输出 $0$",
         "把根当成叶子，输出 $1$ 和 $1$"),
        (0, [],
         "空树 $n=0$，无第二行", "只输出 $0$",
         "去读第二行导致 RE"),
        (7, ["7"],
         "单节点且值等于目标", "一条路径就是 $7$",
         "单节点不当成叶子"),
        (-4, neg,
         "含负数，目标为负", "路径 $1\\ -2\\ -3$",
         "当前和已超就剪枝，负数分支被砍掉"),
        (9, twin,
         "四条叶子路径和都是 $9$", "按从左到右输出四条 $5\\ 3\\ 1$ / $5\\ 3\\ 1$ / $5\\ 3\\ 1$ / $5\\ 3\\ 1$",
         "去重后只留一条"),
        (13, chain,
         "左偏小链，唯一路径命中", "整条链 $10\\ -3\\ 2\\ -1\\ 5$",
         "链上中途节点也当叶子输出前缀"),
        (0, big_miss,
         "压满完全树 $m=4095$，全部为 $1$，目标和 $0$", "无路径",
         "层序建树错位，或把非叶子当叶子扫出大量假路径"),
        (big_target, big_hit,
         "压满 $m=5000$ 随机值，目标和取最左路径和", "至少包含最左根到叶",
         "递归过深（本组是完全树，高约 $12$）；I/O 超时"),
    ]
    assert len(plan) == 10
    # 丢掉未使用变量，避免误导
    _ = (two_paths, small_rand, probe)

    answers = []
    for idx, (target, tokens, _, _, _) in enumerate(plan, 1):
        answers.append(write_case(idx, target, tokens))

    for i, (target, tokens, _, _, _) in enumerate(plan, 1):
        ib = (DATA / f"{i}.in").read_bytes()
        ob = (DATA / f"{i}.out").read_bytes()
        assert not ib.endswith(b"\n") and b"\r" not in ib, f"{i}.in"
        assert ob.endswith(b"\n") and not ob.endswith(b"\n\n") and b"\r" not in ob
        text = ib.decode("utf-8")
        lines = text.split("\n")
        hn, ht = map(int, lines[0].split())
        assert hn == len(tokens) and ht == target
        if hn == 0:
            assert len(lines) == 1
            assert ob == b"0\n"
        else:
            assert lines[1].split() == tokens
            got_lines = ob.decode("utf-8").strip("\n").split("\n")
            k = int(got_lines[0])
            assert k == len(answers[i - 1])
            got_paths = [list(map(int, s.split())) for s in got_lines[1:]]
            assert got_paths == answers[i - 1] == naive(tokens, target)

    assert answers[0] == [[5, 4, 11, 2], [5, 8, 4, 5]]
    assert answers[1] == []
    assert answers[2] == []
    assert answers[3] == []
    assert answers[4] == [[7]]
    assert answers[5] == [[1, -2, -3]]
    assert len(answers[6]) == 4
    assert answers[7] == [[10, -3, 2, -1, 5]]
    assert answers[8] == []
    assert answers[9], "case 10 should hit at least one path"

    rows = []
    for i, (_, _, scale, goal, hack) in enumerate(plan, 1):
        rows.append(f"| {i} | {scale} | {goal} | {hack} |")

    readme = "\n".join([
        "# P7132 测试数据说明",
        "",
        "主造数脚本：题目根目录 `gen.py`。",
        "stdin：第一行 `n targetSum`；$n>0$ 时第二行 $n$ 个层序记号；$n=0$ 时没有第二行。",
        "输出：第一行路径条数 $k$，随后 $k$ 行路径；没有路径时只输出 $0$。",
        "",
        r"约束：非空节点个数 $\le 5000$，$-1000\le Node.val,targetSum\le 1000$。",
        "",
        "| 组别 | 规模/分布 | 目标 | 卡掉的错误解 |",
        "|---|---|---|---|",
        *rows,
        "",
        "`.in` 最后一行后无换行符；`.out` 末尾恰好一个换行符。",
        "",
        "生成后自校验：标程 DFS 结果必须等于独立实现的根到叶路径过滤。",
        "",
    ])
    (DATA / "README.md").write_text(readme, encoding="utf-8")
    print("generated 10 cases")
    for i, ans in enumerate(answers, 1):
        print(i, "k", len(ans), "first", ans[0] if ans else [])


if __name__ == "__main__":
    main()
