# -*- coding: utf-8 -*-
"""P7157 造数：删除最少区间使剩余互不重叠（端点相碰不算重叠）。"""
from __future__ import annotations

import random
import sys
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
from std import solve  # noqa: E402

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
RNG = random.Random(715720260915)

N_MAX = 10**5
LO, HI = -5 * 10**4, 5 * 10**4


def brute(intervals):
    """O(n^2)：按左端点排序后 DP 求最多互不重叠个数。"""
    iv = sorted(intervals)
    n = len(iv)
    dp = [1] * n
    for i in range(n):
        for j in range(i):
            if iv[j][1] <= iv[i][0]:
                dp[i] = max(dp[i], dp[j] + 1)
    return n - max(dp)


def greedy_by_start(intervals):
    """假解：按左端点排序再贪心。"""
    iv = sorted(intervals, key=lambda x: x[0])
    keep = 0
    last = -10**9
    for s, e in iv:
        if s >= last:
            keep += 1
            last = e
    return len(iv) - keep


def treat_touch_overlap(intervals):
    """假解：端点相碰也当成重叠。"""
    iv = sorted(intervals, key=lambda x: x[1])
    keep = 0
    last = -10**9
    for s, e in iv:
        if s > last:
            keep += 1
            last = e
    return len(iv) - keep


def rand_interval():
    a = RNG.randint(LO, HI - 1)
    b = RNG.randint(a + 1, HI)
    return a, b


def write_case(idx, intervals):
    n = len(intervals)
    assert 1 <= n <= N_MAX
    for s, e in intervals:
        assert LO <= s < e <= HI
    ans = solve(list(intervals))
    if n <= 300:
        assert brute(intervals) == ans
    inp = f"{n}\n" + "\n".join(f"{s} {e}" for s, e in intervals)
    (DATA / f"{idx}.in").write_bytes(inp.encode("utf-8"))
    with open(DATA / f"{idx}.out", "w", encoding="utf-8", newline="\n") as f:
        f.write(str(ans) + "\n")
    return ans


def main():
    DATA.mkdir(parents=True, exist_ok=True)

    chain = [(-50000 + i, -49999 + i) for i in range(N_MAX)]
    same_big = [(0, 1)] * N_MAX
    small_rand = [rand_interval() for _ in range(60)]
    start_hack = [(1, 10), (2, 3), (3, 4), (4, 5)]

    plan = [
        ([(1, 2), (2, 3), (3, 4), (1, 3)],
         "样例 1，删掉覆盖三段的长区间", "$1$",
         "按左端点贪心可能多删"),
        ([(1, 2), (1, 2), (1, 2)],
         "样例 2，三个完全相同", "$2$",
         "相同区间只删 $1$ 个"),
        ([(1, 2), (2, 3)],
         "样例 3，端点相碰", "$0$",
         "把相碰当成重叠输出 $1$"),
        ([(-5, 0)],
         "$n=1$ 负数端点", "$0$",
         "输出 $1$"),
        ([(-10, 10), (-5, 0), (0, 5)],
         "大区间包住两段相碰的短区间", "删 $1$ 个",
         "按左端点先留下大区间"),
        (start_hack,
         "长区间左端更靠前", "删 $1$ 留三段短的",
         "按左端点排序贪心"),
        ([(-20, -10), (-10, 0), (5, 8)],
         "两段相碰再加一段分离", "$0$",
         "负数没处理"),
        (small_rand,
         "中等随机 $n=60$", "与 $O(n^2)$ DP 对拍",
         "区间 DP TLE 在后面大数据"),
        (chain,
         "压满 $n=10^5$ 单位区间首尾相接", "$0$",
         "相碰当重叠会删很多；$O(n^2)$ TLE"),
        (same_big,
         "压满 $n=10^5$ 完全相同", "$n-1$",
         "只删 $1$ 个或输出 $0$"),
    ]
    assert len(plan) == 10
    assert greedy_by_start(start_hack) != solve(list(start_hack))
    assert treat_touch_overlap([(1, 2), (2, 3)]) == 1

    answers = []
    metas = []
    for idx, (iv, _, _, _) in enumerate(plan, 1):
        metas.append(iv)
        answers.append(write_case(idx, iv))

    for i, iv in enumerate(metas, 1):
        ib = (DATA / f"{i}.in").read_bytes()
        ob = (DATA / f"{i}.out").read_bytes()
        assert not ib.endswith(b"\n") and b"\r" not in ib, f"{i}.in"
        assert ob.endswith(b"\n") and not ob.endswith(b"\n\n") and b"\r" not in ob
        expect = f"{len(iv)}\n" + "\n".join(f"{s} {e}" for s, e in iv)
        assert ib.decode("utf-8") == expect
        assert ob.decode("utf-8")[:-1] == str(answers[i - 1])

    assert answers[0] == 1
    assert answers[1] == 2
    assert answers[2] == 0
    assert answers[3] == 0
    assert answers[8] == 0
    assert answers[9] == N_MAX - 1
    assert len(metas[8]) == N_MAX and len(metas[9]) == N_MAX

    rows = []
    for i, (_, scale, goal, hack) in enumerate(plan, 1):
        rows.append(f"| {i} | {scale} | {goal} | {hack} |")
    readme = "\n".join([
        "# P7157 测试数据说明",
        "",
        "主造数脚本：题目根目录 `gen.py`。",
        "stdin：第一行 $n$，随后 $n$ 行 $start$ $end$。",
        "输出：最少删除区间数。端点相碰不算重叠。",
        "",
        r"约束：$1\le n\le 10^5$，$-5\times 10^4\le start<end\le 5\times 10^4$。",
        "",
        "| 组别 | 规模/分布 | 目标 | 卡掉的错误解 |",
        "|---|---|---|---|",
        *rows,
        "",
        "`.in` 最后一行后无换行符；`.out` 末尾恰好一个换行符。",
        "",
        "生成后自校验：$n\\le 300$ 时贪心必须等于 $O(n^2)$ DP。",
        "",
    ])
    (DATA / "README.md").write_text(readme, encoding="utf-8")
    print("generated 10 cases")
    for i, ans in enumerate(answers, 1):
        print(i, ans, "n", len(metas[i - 1]))


if __name__ == "__main__":
    main()
