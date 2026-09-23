# -*- coding: utf-8 -*-
"""P7133 造数：员工重要度总和（自己 + 所有下属）。

stdin：第一行 n qid；随后 n 行 id importance m [subs...]。
`.in` 最后一行后不留换行；`.out` 末尾恰好一个换行。
"""
from __future__ import annotations

import random
import sys
from collections import deque
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
from std import solve_from_employees  # noqa: E402

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
RNG = random.Random(713320260914)

N_MAX = 2000
ID_LO, ID_HI = 1, 2000
IMP_LO, IMP_HI = -100, 100


def naive(employees, qid):
    importance = {}
    children = {}
    for eid, imp, subs in employees:
        importance[eid] = imp
        children[eid] = list(subs)
    total = 0
    q = deque([qid])
    while q:
        u = q.popleft()
        total += importance[u]
        q.extend(children[u])
    return total


def case_in_text(qid, employees):
    n = len(employees)
    lines = [f"{n} {qid}"]
    for eid, imp, subs in employees:
        m = len(subs)
        if m == 0:
            lines.append(f"{eid} {imp} {m}")
        else:
            lines.append(f"{eid} {imp} {m} " + " ".join(map(str, subs)))
    return "\n".join(lines)


def write_case(idx, qid, employees):
    n = len(employees)
    ids = [e[0] for e in employees]
    assert 1 <= n <= N_MAX
    assert len(set(ids)) == n
    assert all(ID_LO <= e <= ID_HI for e in ids)
    assert ID_LO <= qid <= ID_HI and qid in set(ids)
    assert all(IMP_LO <= imp <= IMP_HI for _, imp, _ in employees)
    sub_set = set(ids)
    for eid, _, subs in employees:
        assert all(s in sub_set and s != eid for s in subs)
    (DATA / f"{idx}.in").write_bytes(case_in_text(qid, employees).encode("utf-8"))
    ans = solve_from_employees(employees, qid)
    expect = naive(employees, qid)
    assert ans == expect, (idx, ans, expect)
    with open(DATA / f"{idx}.out", "w", encoding="utf-8", newline="\n") as f:
        f.write(str(ans) + "\n")
    return ans


def chain(n, imp_fn, qid=1):
    emps = []
    for i in range(1, n + 1):
        subs = [i + 1] if i < n else []
        emps.append((i, imp_fn(i), subs))
    return qid, emps


def star(n, root_imp, leaf_imp, qid):
    emps = [(1, root_imp, list(range(2, n + 1)))]
    for i in range(2, n + 1):
        emps.append((i, leaf_imp, []))
    return qid, emps


def random_tree(n, id_start=1):
    ids = list(range(id_start, id_start + n))
    RNG.shuffle(ids)
    parent = {ids[0]: None}
    children = {i: [] for i in ids}
    for i in range(1, n):
        p = ids[RNG.randrange(0, i)]
        parent[ids[i]] = p
        children[p].append(ids[i])
    emps = []
    for eid in ids:
        emps.append((eid, RNG.randint(IMP_LO, IMP_HI), children[eid]))
    qid = ids[RNG.randrange(0, n)]
    return qid, emps


def main():
    DATA.mkdir(parents=True, exist_ok=True)

    sample1 = (1, [(1, 5, [2, 3]), (2, 3, []), (3, 3, [])])
    sample2 = (5, [(1, 2, [5]), (5, -3, [])])
    single = (7, [(7, 10, [])])
    leaf_q = (3, [(1, 1, [2]), (2, 2, [3]), (3, 4, [])])
    mid_q = (2, [(1, 5, [2]), (2, 6, [3]), (3, 7, [])])
    forest = (3, [
        (1, 10, [2]),
        (2, 1, []),
        (3, 8, [4]),
        (4, 2, []),
    ])
    neg_star = star(6, -5, -2, 1)
    chain8 = chain(8, lambda i: i, 1)

    q9, emps9 = chain(N_MAX, lambda i: 1 if i % 2 == 0 else -1, 1)
    q10, emps10 = random_tree(N_MAX)

    plan = [
        (sample1[0], sample1[1],
         "样例 1", "根 $1$ 加两名下属得 $11$",
         "只加直属忘了加自己，得到 $6$"),
        (sample2[0], sample2[1],
         "样例 2，查询叶子且重要度为负", "答案 $-3$",
         "把上级 $1$ 也加进来得到 $-1$"),
        (single[0], single[1],
         "只有一人", "答案就是自己的 $10$",
         "去读不存在的下属"),
        (leaf_q[0], leaf_q[1],
         "查询链底叶子", "只有 $4$",
         "把整条链 $1+2+4$ 都加上"),
        (mid_q[0], mid_q[1],
         "查询链中间节点", "$6+7=13$",
         "漏掉间接下属 $3$，只输出 $6$"),
        (forest[0], forest[1],
         "两棵树的森林，查询其中一棵", "$8+2=10$，不含另一棵",
         "把所有员工重要度加总"),
        (neg_star[0], neg_star[1],
         "星形，根和叶子都是负数", "根加 $5$ 个叶子",
         "重要度当无符号数"),
        (chain8[0], chain8[1],
         "短链查询根", "$1+\\cdots+8=36$",
         "只走一层"),
        (q9, emps9,
         "压满链 $n=2000$，查询根", "正负交替求和",
         "递归 DFS 在链上爆栈"),
        (q10, emps10,
         "压满 $n=2000$ 随机树，查询随机节点", "只累加该节点子树",
         "I/O 按行读错，或 ID 不从 $1$ 连续时数组越界"),
    ]
    assert len(plan) == 10

    answers = []
    for idx, (qid, emps, _, _, _) in enumerate(plan, 1):
        answers.append(write_case(idx, qid, emps))

    for i, (qid, emps, _, _, _) in enumerate(plan, 1):
        ib = (DATA / f"{i}.in").read_bytes()
        ob = (DATA / f"{i}.out").read_bytes()
        assert not ib.endswith(b"\n") and b"\r" not in ib, f"{i}.in"
        assert ob.endswith(b"\n") and not ob.endswith(b"\n\n") and b"\r" not in ob
        text = ib.decode("utf-8")
        lines = text.split("\n")
        hn, hq = map(int, lines[0].split())
        assert hn == len(emps) and hq == qid
        parsed = []
        for line in lines[1:]:
            parts = list(map(int, line.split()))
            parsed.append((parts[0], parts[1], parts[3:3 + parts[2]]))
        assert [(a, b, list(c)) for a, b, c in parsed] == [(a, b, list(c)) for a, b, c in emps]
        got = int(ob.decode("utf-8").strip())
        assert got == answers[i - 1] == naive(emps, qid)

    assert answers[0] == 11
    assert answers[1] == -3
    assert answers[2] == 10
    assert answers[3] == 4
    assert answers[4] == 13
    assert answers[5] == 10
    assert answers[7] == 36

    rows = []
    for i, (_, _, scale, goal, hack) in enumerate(plan, 1):
        rows.append(f"| {i} | {scale} | {goal} | {hack} |")

    readme = "\n".join([
        "# P7133 测试数据说明",
        "",
        "主造数脚本：题目根目录 `gen.py`。",
        "stdin：第一行 `n qid`；随后 $n$ 行 `id importance m [subs...]`，$m=0$ 时没有下属。",
        "输出：查询员工及其所有下属的重要度之和。",
        "",
        r"约束：$1\le n\le 2000$，$1\le id_i\le 2000$ 互异，$-100\le importance_i\le 100$。",
        "",
        "| 组别 | 规模/分布 | 目标 | 卡掉的错误解 |",
        "|---|---|---|---|",
        *rows,
        "",
        "`.in` 最后一行后无换行符；`.out` 末尾恰好一个换行符。",
        "",
        "生成后自校验：栈 DFS 必须等于队列 BFS 的子树重要度之和。",
        "",
    ])
    (DATA / "README.md").write_text(readme, encoding="utf-8")
    print("generated 10 cases")
    for i, ans in enumerate(answers, 1):
        print(i, "ans", ans)


if __name__ == "__main__":
    main()
