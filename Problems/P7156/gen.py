# -*- coding: utf-8 -*-
"""P7156 造数：环形加油站（有解时起点唯一）。

stdin：第一行 n，第二行 n 个 gas，第三行 n 个 cost。
输出：可行起点编号（从 0 开始），否则 -1。
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
RNG = random.Random(715620260915)

N_MAX = 10**5
V_MAX = 10**4


def can_from(gas, cost, s):
    tank = 0
    n = len(gas)
    for k in range(n):
        i = (s + k) % n
        tank += gas[i] - cost[i]
        if tank < 0:
            return False
    return True


def brute(gas, cost):
    """小数据：枚举每个起点，并检查有解时恰好一个。"""
    hits = [s for s in range(len(gas)) if can_from(gas, cost, s)]
    if not hits:
        return -1
    assert len(hits) == 1, hits
    return hits[0]


def count_starts(gas, cost):
    """O(n) 统计合法起点，用来校验大数据的唯一性。"""
    n = len(gas)
    p = [0] * (n + 1)
    for i in range(n):
        p[i + 1] = p[i] + gas[i] - cost[i]
    total = p[n]
    pref_min = [0] * (n + 1)
    pref_min[0] = p[0]
    for i in range(1, n + 1):
        pref_min[i] = min(pref_min[i - 1], p[i])
    suff_min = [0] * (n + 1)
    suff_min[n] = p[n]
    for i in range(n - 1, -1, -1):
        suff_min[i] = min(p[i], suff_min[i + 1])
    hits = []
    for i in range(n):
        ok = suff_min[i + 1] >= p[i] and total + pref_min[i] >= p[i]
        if ok:
            hits.append(i)
    return hits


def apply_offset(gas, cost):
    """净油量不变，给每站同时加减油，避免全是 0/1。"""
    n = len(gas)
    g = gas[:]
    c = cost[:]
    for i in range(n):
        room = min(V_MAX - g[i], V_MAX - c[i])
        if room > 0:
            add = RNG.randint(0, room)
            g[i] += add
            c[i] += add
    return g, c


def unique_start(n, s):
    """net[s]=+1, net[s-1]=-1, 其余 0：从 s 出发最后才把多出来的 1 填进坑。"""
    assert n >= 2
    assert 0 <= s < n
    gas = [0] * n
    cost = [0] * n
    prev = (s - 1) % n
    gas[s] = 1
    cost[s] = 0
    gas[prev] = 0
    cost[prev] = 1
    return apply_offset(gas, cost)


def max_net_wrong(n=4):
    """净油最大的站不是合法起点。"""
    # net = [2, 100, -101, -1]，唯一起点 0，argmax 是 1
    gas = [2, 100, 0, 0]
    cost = [0, 0, 101, 1]
    return apply_offset(gas, cost)


def impossible(n, vmax=V_MAX):
    gas = [RNG.randint(0, vmax) for _ in range(n)]
    cost = [RNG.randint(0, vmax) for _ in range(n)]
    sg, sc = sum(gas), sum(cost)
    if sg < sc:
        return gas, cost
    # 把总油压到比总耗油少 1
    need = sg - sc + 1
    i = 0
    while need > 0 and i < n:
        cut = min(need, gas[i])
        gas[i] -= cut
        need -= cut
        i += 1
    if sum(gas) >= sum(cost):
        gas = [0] * n
        cost = [1] * n
    return gas, cost


def write_case(idx, gas, cost):
    n = len(gas)
    assert 1 <= n <= N_MAX
    assert len(cost) == n
    for x in gas + cost:
        assert 0 <= x <= V_MAX
    ans = solve(gas, cost)
    hits = count_starts(gas, cost)
    if ans == -1:
        assert hits == []
    else:
        assert hits == [ans], (idx, hits, ans)
    if n <= 400:
        assert brute(gas, cost) == ans
    inp = f"{n}\n" + " ".join(str(x) for x in gas) + "\n" + " ".join(str(x) for x in cost)
    (DATA / f"{idx}.in").write_bytes(inp.encode("utf-8"))
    with open(DATA / f"{idx}.out", "w", encoding="utf-8", newline="\n") as f:
        f.write(str(ans) + "\n")
    return ans


def main():
    DATA.mkdir(parents=True, exist_ok=True)

    g8, c8 = unique_start(80, 17)
    g9, c9 = unique_start(N_MAX, N_MAX - 1)
    g10, c10 = impossible(N_MAX, vmax=20)

    plan = [
        ([1, 2, 3, 4, 5], [3, 4, 5, 1, 2],
         "样例 1，$n=5$，起点 $3$", "$3$",
         "从 $0$ 模拟或按 $1$ 编号输出 $4$"),
        ([2, 3, 4], [3, 4, 3],
         "样例 2，总量不够", "$-1$",
         "不判断总量仍返回某个下标"),
        ([5], [4],
         "$n=1$ 且油够", "$0$",
         "输出 $-1$"),
        ([1], [2],
         "$n=1$ 且油不够", "$-1$",
         "输出 $0$"),
        (*unique_start(6, 0),
         "唯一起点在 $0$", "$0$",
         "总量够就随便输出非 $0$"),
        (*max_net_wrong(),
         "净油最大的站不是起点", "唯一合法起点 $0$",
         "选 $gas-cost$ 最大的下标"),
        (*unique_start(9, 5),
         "小环形、起点不在两端", "起点 $5$",
         "取第一个 $gas\\ge cost$ 的站"),
        (g8, c8,
         "中等 $n=80$，构造唯一起点", "DP/贪心与枚举对拍",
         "从每个起点模拟在后面大数据超时"),
        (g9, c9,
         "压满 $n=10^5$，起点在最后一站", "$O(n)$ 贪心",
         "$O(n^2)$ 每个起点绕圈 TLE"),
        (g10, c10,
         "压满 $n=10^5$，总量不够", "$-1$",
         "不判断总量返回 $0$ 或 $n$"),
    ]
    assert len(plan) == 10

    answers = []
    metas = []
    for idx, (gas, cost, _, _, _) in enumerate(plan, 1):
        metas.append((gas, cost))
        answers.append(write_case(idx, gas, cost))

    for i, (gas, cost) in enumerate(metas, 1):
        ib = (DATA / f"{i}.in").read_bytes()
        ob = (DATA / f"{i}.out").read_bytes()
        assert not ib.endswith(b"\n") and b"\r" not in ib, f"{i}.in"
        assert ob.endswith(b"\n") and not ob.endswith(b"\n\n") and b"\r" not in ob
        expect_in = (
            f"{len(gas)}\n"
            + " ".join(str(x) for x in gas)
            + "\n"
            + " ".join(str(x) for x in cost)
        )
        assert ib.decode("utf-8") == expect_in
        got = ob.decode("utf-8")[:-1]
        assert got == str(answers[i - 1])

    assert answers[0] == 3
    assert answers[1] == -1
    assert answers[2] == 0
    assert answers[3] == -1
    assert answers[4] == 0
    assert answers[5] == 0
    assert answers[6] == 5
    assert answers[8] == N_MAX - 1
    assert answers[9] == -1
    assert len(metas[8][0]) == N_MAX and len(metas[9][0]) == N_MAX
    # 第 6 组：净油最大不是 0
    g, c = metas[5]
    nets = [g[i] - c[i] for i in range(len(g))]
    assert max(range(len(nets)), key=lambda i: nets[i]) != 0

    rows = []
    for i, (_, _, scale, goal, hack) in enumerate(plan, 1):
        rows.append(f"| {i} | {scale} | {goal} | {hack} |")

    readme = "\n".join([
        "# P7156 测试数据说明",
        "",
        "主造数脚本：题目根目录 `gen.py`。",
        "stdin：第一行 $n$，第二行 $n$ 个 $gas$，第三行 $n$ 个 $cost$。",
        "输出：绕圈可行的唯一起点（从 $0$ 编号），否则 $-1$。",
        "",
        r"约束：$1\le n\le 10^5$，$0\le gas_i,cost_i\le 10^4$，有解时起点唯一。",
        "",
        "| 组别 | 规模/分布 | 目标 | 卡掉的错误解 |",
        "|---|---|---|---|",
        *rows,
        "",
        "`.in` 最后一行后无换行符；`.out` 末尾恰好一个换行符。",
        "",
        "生成后自校验：贪心结果必须与前缀最小值判定的合法起点集合一致；",
        "$n\\le 400$ 时再与逐起点模拟对拍。有解时集合大小必须为 $1$。",
        "",
    ])
    (DATA / "README.md").write_text(readme, encoding="utf-8")
    print("generated 10 cases")
    for i, ans in enumerate(answers, 1):
        print(i, ans, "n", len(metas[i - 1][0]))


if __name__ == "__main__":
    main()
