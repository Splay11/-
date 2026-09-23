# -*- coding: utf-8 -*-
"""P7134 造数：终止进程及其整棵子树，ID 升序输出。

stdin：第一行 n kill；第二行 n 个 pid；第三行 n 个 ppid。
`.in` 最后一行后不留换行；`.out` 末尾恰好一个换行。
"""
from __future__ import annotations

import random
import sys
from collections import deque
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
from std import solve  # noqa: E402

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
RNG = random.Random(713420260914)

N_MAX = 5 * 10**4
ID_HI = 5 * 10**4


def naive(pids, ppids, kill):
    children = {p: [] for p in pids}
    for child, parent in zip(pids, ppids):
        if parent != 0:
            children[parent].append(child)
    killed = []
    q = deque([kill])
    while q:
        u = q.popleft()
        killed.append(u)
        q.extend(children[u])
    killed.sort()
    return killed


def shuffle_arrays(parent_of):
    pids = list(parent_of.keys())
    RNG.shuffle(pids)
    ppids = [parent_of[p] for p in pids]
    return pids, ppids


def chain_parent(n):
    # 1 为根，1->2->...->n
    return {i: (0 if i == 1 else i - 1) for i in range(1, n + 1)}


def star_parent(n):
    return {i: (0 if i == 1 else 1) for i in range(1, n + 1)}


def random_tree_parent(n):
    parent_of = {1: 0}
    for i in range(2, n + 1):
        parent_of[i] = RNG.randint(1, i - 1)
    return parent_of


def case_in_text(kill, pids, ppids):
    n = len(pids)
    return f"{n} {kill}\n" + " ".join(map(str, pids)) + "\n" + " ".join(map(str, ppids))


def write_case(idx, kill, pids, ppids):
    n = len(pids)
    assert 1 <= n <= N_MAX
    assert len(ppids) == n
    assert len(set(pids)) == n
    assert all(1 <= p <= ID_HI for p in pids)
    assert all(0 <= p <= ID_HI for p in ppids)
    assert ppids.count(0) == 1
    assert kill in set(pids)
    (DATA / f"{idx}.in").write_bytes(case_in_text(kill, pids, ppids).encode("utf-8"))
    ans = solve(pids, ppids, kill)
    expect = naive(pids, ppids, kill)
    assert ans == expect, (idx, ans[:8], expect[:8])
    with open(DATA / f"{idx}.out", "w", encoding="utf-8", newline="\n") as f:
        f.write(" ".join(map(str, ans)) + "\n")
    return ans


def main():
    DATA.mkdir(parents=True, exist_ok=True)

    s1_pid = [1, 3, 10, 5]
    s1_ppid = [3, 0, 5, 3]
    s2_pid = [1]
    s2_ppid = [0]

    # 小树：4 为根，孩子 2、6；2 的孩子 1、3
    small_p = {4: 0, 2: 4, 6: 4, 1: 2, 3: 2}
    small_pid, small_ppid = shuffle_arrays(small_p)

    star_pid, star_ppid = shuffle_arrays(star_parent(8))
    chain_pid, chain_ppid = shuffle_arrays(chain_parent(12))
    rnd_pid, rnd_ppid = shuffle_arrays(random_tree_parent(20))
    rnd_kill = rnd_pid[RNG.randrange(0, len(rnd_pid))]

    big_chain_pid, big_chain_ppid = shuffle_arrays(chain_parent(N_MAX))
    big_tree_p = random_tree_parent(N_MAX)
    big_tree_pid, big_tree_ppid = shuffle_arrays(big_tree_p)
    # 杀掉编号偏大的节点，子树不会是整棵树，也避免只杀叶子
    big_kill = N_MAX // 3

    plan = [
        (5, s1_pid, s1_ppid,
         "样例 1", "杀掉 $5$ 及其孩子 $10$",
         "输出没排序；或把根 $3$ 也杀掉"),
        (1, s2_pid, s2_ppid,
         "样例 2，单进程", "只有 $1$",
         "输出空行"),
        (4, small_pid, small_ppid,
         "杀掉整棵树的根", "五个进程全输出",
         "只输出根自己"),
        (6, small_pid, small_ppid,
         "杀掉叶子", "只有 $6$",
         "把兄弟 $2$ 的子树也杀掉"),
        (2, small_pid, small_ppid,
         "杀掉中间节点", "$1\\ 2\\ 3$（已排序）",
         "输出顺序仍是 DFS 序 $2\\ 1\\ 3$"),
        (1, star_pid, star_ppid,
         "星形，杀掉中心", "全部 $1\\cdots 8$",
         "只杀中心不杀叶子"),
        (7, chain_pid, chain_ppid,
         "短链从中间杀掉", "$7\\cdots 12$",
         "递归还没爆，但只走了一层"),
        (rnd_kill, rnd_pid, rnd_ppid,
         "小随机树", "子树 ID 排序后与 BFS 对拍",
         "邻接表建成无向图，把父亲也杀了"),
        (1, big_chain_pid, big_chain_ppid,
         "压满链 $n=5\\times 10^4$，杀掉根", "输出 $1\\cdots 50000$",
         "递归 DFS 爆栈；或没排序"),
        (big_kill, big_tree_pid, big_tree_ppid,
         "压满随机树 $n=5\\times 10^4$，杀掉 $n/3$", "只输出该节点子树",
         "I/O 超时；或 ID 当下标越界"),
    ]
    assert len(plan) == 10

    answers = []
    for idx, (kill, pids, ppids, _, _, _) in enumerate(plan, 1):
        answers.append(write_case(idx, kill, pids, ppids))

    for i, (kill, pids, ppids, _, _, _) in enumerate(plan, 1):
        ib = (DATA / f"{i}.in").read_bytes()
        ob = (DATA / f"{i}.out").read_bytes()
        assert not ib.endswith(b"\n") and b"\r" not in ib, f"{i}.in"
        assert ob.endswith(b"\n") and not ob.endswith(b"\n\n") and b"\r" not in ob
        text = ib.decode("utf-8")
        lines = text.split("\n")
        hn, hk = map(int, lines[0].split())
        gp = list(map(int, lines[1].split()))
        gpp = list(map(int, lines[2].split()))
        assert hn == len(pids) == len(gp) and hk == kill
        assert gp == pids and gpp == ppids
        got = list(map(int, ob.decode("utf-8").split()))
        assert got == answers[i - 1] == naive(pids, ppids, kill)
        assert got == sorted(got)

    assert answers[0] == [5, 10]
    assert answers[1] == [1]
    assert answers[2] == [1, 2, 3, 4, 6]
    assert answers[3] == [6]
    assert answers[4] == [1, 2, 3]
    assert answers[8] == list(range(1, N_MAX + 1))

    rows = []
    for i, (_, _, _, scale, goal, hack) in enumerate(plan, 1):
        rows.append(f"| {i} | {scale} | {goal} | {hack} |")

    readme = "\n".join([
        "# P7134 测试数据说明",
        "",
        "主造数脚本：题目根目录 `gen.py`。",
        "stdin：第一行 `n kill`；第二行 $n$ 个 $pid$；第三行 $n$ 个 $ppid$。",
        "输出：被终止进程 $ID$，升序，空格分隔。",
        "",
        r"约束：$1\le n\le 5\times 10^4$，$1\le pid_i\le 5\times 10^4$ 互异，恰好一个 $ppid=0$。",
        "",
        "| 组别 | 规模/分布 | 目标 | 卡掉的错误解 |",
        "|---|---|---|---|",
        *rows,
        "",
        "`.in` 最后一行后无换行符；`.out` 末尾恰好一个换行符。",
        "",
        "生成后自校验：栈 DFS 收集再排序，必须等于队列 BFS 再排序。",
        "",
    ])
    (DATA / "README.md").write_text(readme, encoding="utf-8")
    print("generated 10 cases")
    for i, ans in enumerate(answers, 1):
        print(i, "k", len(ans), "head", ans[:5])


if __name__ == "__main__":
    main()
