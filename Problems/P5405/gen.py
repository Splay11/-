# -*- coding: utf-8 -*-
"""P5405 叉车装车优惠：10 组测例。

分层目标（每组 10 分，合计 100）：
- 1～7：无剪枝回溯约 2^n 可通过（70%）
- 8～10：n 大且容量紧，只有 O(nW) DP 能满过（100%）
其中第 3、4 组答案为 0。
"""
from __future__ import annotations

import random
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
RNG = random.Random(540520260909)
NEG = -1
UNPRUNED_OK = 5_000_000  # 无剪枝可接受：n=21 全装约 2^22 结点，Python/C++ 1s 内可过
PRUNED_OK = 3_000_000  # 有剪枝可接受的搜索结点数
PRUNED_ABORT = 8_000_000


def max_value(n, W, T, v, w):
    dp = [[NEG, NEG] for _ in range(W + 1)]
    dp[0][0] = 0
    for i in range(n):
        new_dp = [row[:] for row in dp]
        for vol in range(W + 1):
            for trig in (0, 1):
                if dp[vol][trig] < 0:
                    continue
                cost = v[i] // 2 if trig else v[i]
                nvol = vol + cost
                if nvol > W:
                    continue
                ntrig = 1 if (trig or nvol >= T) else 0
                val = dp[vol][trig] + w[i]
                if val > new_dp[nvol][ntrig]:
                    new_dp[nvol][ntrig] = val
        dp = new_dp
    ans = 0
    for vol in range(W + 1):
        for trig in (0, 1):
            if dp[vol][trig] > ans:
                ans = dp[vol][trig]
    return ans


def unpruned_nodes(n, W, T, v, w, limit):
    """不带剪枝的回溯，只统计结点数（合法才递归装入）。"""
    nodes = [0]

    def dfs(i, vol, trig):
        nodes[0] += 1
        if nodes[0] > limit:
            return
        if i == n:
            return
        dfs(i + 1, vol, trig)
        if nodes[0] > limit:
            return
        cost = v[i] // 2 if trig else v[i]
        nvol = vol + cost
        if nvol <= W:
            ntrig = 1 if (trig or nvol >= T) else 0
            dfs(i + 1, nvol, ntrig)

    dfs(0, 0, 0)
    return nodes[0]


def pruned_nodes(n, W, T, v, w, limit):
    """先尝试装入、再用剩余货值上界剪枝。"""
    suffix = [0] * (n + 1)
    for i in range(n - 1, -1, -1):
        suffix[i] = suffix[i + 1] + w[i]
    nodes = [0]
    ans = [0]

    def dfs(i, vol, trig, cur):
        nodes[0] += 1
        if nodes[0] > limit:
            return
        if cur + suffix[i] <= ans[0]:
            return
        if i == n:
            if cur > ans[0]:
                ans[0] = cur
            return
        # 先装
        cost = v[i] // 2 if trig else v[i]
        nvol = vol + cost
        if nvol <= W:
            ntrig = 1 if (trig or nvol >= T) else 0
            dfs(i + 1, nvol, ntrig, cur + w[i])
            if nodes[0] > limit:
                return
        # 再跳过
        dfs(i + 1, vol, trig, cur)

    dfs(0, 0, 0, 0)
    return nodes[0]


def write_in(path: Path, n, W, T, items):
    lines = [f"{n} {W} {T}"]
    for vi, wi in items:
        lines.append(f"{vi} {wi}")
    # 输入末尾不要换行
    path.write_bytes("\n".join(lines).encode("utf-8"))


def write_out(path: Path, ans: int):
    path.write_bytes((str(ans) + "\n").encode("utf-8"))


def write_config():
    cases = "\n".join(
        f"      - input: {i}.in\n        output: {i}.out" for i in range(1, 11)
    )
    config = f"""type: default
time: 1s
memory: 256m
subtasks:
  - score: 100
    if: []
    id: 1
    type: sum
    cases:
{cases}
langs:
  - c
  - cc.cc14o2
  - cc
  - java
  - py.py3
  - py
  - js
  - go
"""
    (DATA / "config.yaml").write_bytes(config.encode("utf-8"))


def rand_item(vmax, wmax):
    return (RNG.randint(1, vmax), RNG.randint(1, wmax))


def build_cases():
    cases = []

    # 1 样例1
    cases.append((3, 10, 5, [(6, 10), (4, 9), (5, 8)], "样例1：三件都装，触发优惠后折半"))

    # 2 样例2
    cases.append((3, 8, 4, [(5, 1), (4, 100), (4, 100)], "样例2：必须跳过第一件"))

    # 3 答案 0：全部体积大于 W，无法装任何一件
    items = [(11 + i, 100 + i * 10) for i in range(8)]
    cases.append((8, 10, 5, items, "答案为 0：所有 v_i > W"))

    # 4 答案 0：n 拉到无剪枝上限附近，仍全部装不下
    items = [(RNG.randint(5, 20), RNG.randint(1, 1000)) for _ in range(16)]
    cases.append((16, 4, 3, items, "答案为 0：W 极小，全部 v_i >= 5"))

    # 5 小随机：无剪枝可过，含触发优惠与跳过
    n, W, T = 14, 40, 12
    items = [rand_item(18, 50) for _ in range(n)]
    items[0] = (15, 1)
    items[1] = (10, 80)
    items[2] = (10, 80)
    cases.append((n, W, T, items, "小随机：类似样例2的跳过决策 + 其余随机"))

    # 6 全都能装下，n=20：无剪枝 2^20 可通过（累计 60%）
    n, W, T = 20, 5000, 10
    items = [(1, RNG.randint(1, 100)) for _ in range(n)]
    cases.append((n, W, T, items, "中等：全部 v_i=1 都能装下，无剪枝回溯可过"))

    # 7 全都能装下，n=21，带优惠触发：无剪枝仍可过（累计 70%）
    n, W, T = 21, 5000, 8
    items = [(2, RNG.randint(10, 200)) for _ in range(n)]
    cases.append((n, W, T, items, "中等：全部能装下且会触发优惠，无剪枝回溯可过"))

    # 8 中等 n、容量紧，跳过低货值大体积；剪枝上界松，只有 DP 稳过
    n, W, T = 42, 80, 25
    items = [(30, 5)] + [(RNG.randint(8, 18), RNG.randint(40, 90)) for _ in range(n - 1)]
    cases.append((n, W, T, items, "构造：第一件低货值大体积，容量紧，卡剪枝暴力"))

    # 9 上限规模随机
    n, W, T = 100, 5000, 2000
    items = [(RNG.randint(30, 180), RNG.randint(1, 10**6)) for _ in range(n)]
    cases.append((n, W, T, items, "最大规模随机：n=100,W=5000，只有 DP"))

    # 10 上限 + 必须跳过前若干件才能触发后半高货值
    n, W, T = 100, 5000, 400
    items = [(800, 1), (800, 1), (800, 1)]
    for i in range(3, n):
        items.append((RNG.randint(40, 120), RNG.randint(10**5, 10**6)))
    cases.append((n, W, T, items, "最大规模构造：前三件低货值占体积，卡贪心先装"))

    return cases


def classify(n, W, T, items, ans):
    v = [a[0] for a in items]
    w = [a[1] for a in items]
    # 全都能装下时，无剪枝结点数就是 2^{n+1}-1，不必真搜
    all_fit = True
    vol = 0
    trig = 0
    for i in range(n):
        cost = v[i] // 2 if trig else v[i]
        if vol + cost > W:
            all_fit = False
            break
        vol += cost
        if vol >= T:
            trig = 1
    if all_fit:
        un = (1 << (n + 1)) - 1
    elif n <= 20:
        un = unpruned_nodes(n, W, T, v, w, UNPRUNED_OK + 1)
    else:
        un = UNPRUNED_OK + 1
    if n <= 22 and not all_fit:
        pr = pruned_nodes(n, W, T, v, w, PRUNED_ABORT)
    elif all_fit:
        # 先装后剪枝，最优是全装，搜索接近线性
        pr = 2 * n + 5
    else:
        pr = pruned_nodes(n, W, T, v, w, PRUNED_ABORT)
    u_ok = un <= UNPRUNED_OK
    p_ok = pr <= PRUNED_OK
    return un, pr, u_ok, p_ok, ans


def main():
    DATA.mkdir(parents=True, exist_ok=True)
    cases = build_cases()
    notes = []
    zero_ids = []
    for idx, (n, W, T, items, desc) in enumerate(cases, 1):
        assert 1 <= n <= 100
        assert 1 <= W <= 5000 and 1 <= T <= 5000
        assert len(items) == n
        for vi, wi in items:
            assert 1 <= vi <= 5000 and 1 <= wi <= 10**6
        v = [a[0] for a in items]
        w = [a[1] for a in items]
        ans = max_value(n, W, T, v, w)
        write_in(DATA / f"{idx}.in", n, W, T, items)
        write_out(DATA / f"{idx}.out", ans)
        # 回读校验
        raw = (DATA / f"{idx}.in").read_text(encoding="utf-8")
        assert not raw.endswith("\n")
        out_raw = (DATA / f"{idx}.out").read_bytes()
        assert out_raw.endswith(b"\n") and out_raw.count(b"\n") == 1
        un, pr, u_ok, p_ok, _ = classify(n, W, T, items, ans)
        if ans == 0:
            zero_ids.append(idx)
        band = "无剪枝可过" if u_ok else ("剪枝可过" if p_ok else "仅 DP")
        notes.append(
            f"- {idx}.in：{desc}；n={n}, W={W}, T={T}, ans={ans}；"
            f"无剪枝结点约 {un}，剪枝结点约 {pr} → {band}"
        )
        print(f"case {idx}: n={n} ans={ans} un={un} pr={pr} {band}")

    assert len(cases) == 10
    assert zero_ids == [3, 4], zero_ids
    write_config()

    readme = """# P5405 测试数据说明

每组 10 分，共 10 组。

| 组别 | 分值 | 规模/分布 | 目标 | 卡掉的错误解 |
|---|---:|---|---|---|
| 1 | 10 | 样例1 | 展示触发优惠后折半仍能装满 | 忽略优惠或顺序约束 |
| 2 | 10 | 样例2 | 展示必须跳过前件 | 贪心先装低货值 |
| 3 | 10 | 小 n，全部装不下 | 答案为 0 | 漏处理「一件都不装」 |
| 4 | 10 | n=16，W 极小，答案为 0 | 无剪枝也能过的零解 | 输出非 0 |
| 5 | 10 | n=14 小随机 | 无剪枝回溯可通过 | 转移写错 |
| 6 | 10 | n=20，全部能装下 | 无剪枝可通过（累计 60%） | 转移写错 |
| 7 | 10 | n=21，全部能装下 | 无剪枝可通过（累计 70%） | 转移写错 |
| 8 | 10 | n=42，容量紧 | 剪枝上界松，TLE | 回溯暴力 |
| 9 | 10 | n=100,W=5000 随机 | 压测 DP | 一切指数搜索 |
| 10 | 10 | n=100 构造跳过前件 | 卡先装贪心与搜索 | 贪心 / 剪枝 DFS |

生成器固定种子 `540520260909`。输入文件最后一行后无换行；输出恰好一个换行。
"""
    readme += "\n".join(notes) + "\n"
    (DATA / "README.md").write_bytes(readme.encode("utf-8"))
    print("zero cases", zero_ids)
    print("done")


if __name__ == "__main__":
    main()
