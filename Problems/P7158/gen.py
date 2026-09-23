# -*- coding: utf-8 -*-
"""P7158 造数：从两端拿 k 张牌的最大点数。"""
from __future__ import annotations

import random
import sys
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
from std import solve  # noqa: E402

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
RNG = random.Random(715820260915)

N_MAX = 10**5
V_MAX = 10**4


def brute(cards, k):
    """枚举左边拿 i 张、右边拿 k-i 张。"""
    n = len(cards)
    pref = [0] * (n + 1)
    for i, x in enumerate(cards):
        pref[i + 1] = pref[i] + x
    best = 0
    for left in range(k + 1):
        right = k - left
        s = pref[left] + (pref[n] - pref[n - right])
        if s > best:
            best = s
    return best


def take_k_largest(cards, k):
    """假解：取全局最大的 k 张。"""
    return sum(sorted(cards, reverse=True)[:k])


def only_one_side(cards, k):
    """假解：只从左侧或只从右侧拿。"""
    return max(sum(cards[:k]), sum(cards[-k:]))


def write_case(idx, cards, k):
    n = len(cards)
    assert 1 <= n <= N_MAX
    assert 1 <= k <= n
    for x in cards:
        assert 1 <= x <= V_MAX
    ans = solve(cards, k)
    expect = brute(cards, k)
    assert ans == expect
    inp = f"{n} {k}\n" + " ".join(str(x) for x in cards)
    (DATA / f"{idx}.in").write_bytes(inp.encode("utf-8"))
    with open(DATA / f"{idx}.out", "w", encoding="utf-8", newline="\n") as f:
        f.write(str(ans) + "\n")
    return ans


def main():
    DATA.mkdir(parents=True, exist_ok=True)

    small = [RNG.randint(1, 50) for _ in range(40)]
    big_mid = [1] * N_MAX
    big_mid[N_MAX // 2] = V_MAX
    k9 = 3
    all_take = [RNG.randint(1, 100) for _ in range(N_MAX)]

    plan = [
        ([1, 2, 3, 4, 5, 6, 1], 3,
         "样例 1，从右边拿 $1,6,5$", "$12$",
         "只拿左边得到 $6$"),
        ([2, 2, 2], 2,
         "样例 2，全相同", "$4$",
         "输出 $6$"),
        ([9, 7, 7, 9, 7, 7, 9], 7,
         "样例 3，$k=n$ 全拿走", "$55$",
         "窗口长度写成 $k$ 而不是 $n-k$"),
        ([1, 1000, 1], 1,
         "样例 4，中间大牌拿不到", "$1$",
         "取全局最大的 $k$ 张得到 $1000$"),
        ([1, 79, 80, 1, 1, 1, 200, 1], 3,
         "样例 5，右端 $1+200+1$", "$202$",
         "拿左边 $1+79+80=160$"),
        ([5, 1, 1, 1, 9], 2,
         "两端一大一小", "$14$",
         "只从一侧拿"),
        ([3], 1,
         "$n=k=1$", "$3$",
         "输出 $0$"),
        (small, 7,
         "中等随机 $n=40$", "与枚举左右张数对拍",
         "每次重新求和导致后面 TLE"),
        (big_mid, k9,
         "压满 $n=10^5$，中间有一张 $10^4$", "只能拿两端，$O(n)$",
         "取全局最大 $k$ 张会拿到中间那张"),
        (all_take, N_MAX,
         "压满 $n=k=10^5$ 必须全拿", "总和",
         "leave 窗口没特判 $0$ 越界"),
    ]
    assert len(plan) == 10
    assert take_k_largest([1, 1000, 1], 1) == 1000
    assert only_one_side([1, 2, 3, 4, 5, 6, 1], 3) == 12  # 这组碰巧右侧最优
    assert only_one_side([5, 1, 1, 1, 9], 2) != solve([5, 1, 1, 1, 9], 2)

    answers = []
    metas = []
    for idx, (cards, k, _, _, _) in enumerate(plan, 1):
        metas.append((cards, k))
        answers.append(write_case(idx, cards, k))

    for i, (cards, k) in enumerate(metas, 1):
        ib = (DATA / f"{i}.in").read_bytes()
        ob = (DATA / f"{i}.out").read_bytes()
        assert not ib.endswith(b"\n") and b"\r" not in ib, f"{i}.in"
        assert ob.endswith(b"\n") and not ob.endswith(b"\n\n") and b"\r" not in ob
        expect = f"{len(cards)} {k}\n" + " ".join(str(x) for x in cards)
        assert ib.decode("utf-8") == expect
        assert ob.decode("utf-8")[:-1] == str(answers[i - 1])

    assert answers[0] == 12
    assert answers[1] == 4
    assert answers[2] == 55
    assert answers[3] == 1
    assert answers[4] == 202
    assert answers[6] == 3
    assert answers[9] == sum(metas[9][0])
    assert len(metas[8][0]) == N_MAX and len(metas[9][0]) == N_MAX
    assert take_k_largest(metas[8][0], metas[8][1]) != answers[8]

    rows = []
    for i, (_, _, scale, goal, hack) in enumerate(plan, 1):
        rows.append(f"| {i} | {scale} | {goal} | {hack} |")
    readme = "\n".join([
        "# P7158 测试数据说明",
        "",
        "主造数脚本：题目根目录 `gen.py`。",
        "stdin：第一行 $n$ $k$，第二行 $n$ 个点数。",
        "输出：从两端恰好拿 $k$ 张的最大点数。",
        "",
        r"约束：$1\le k\le n\le 10^5$，$1\le cardPoints_i\le 10^4$。",
        "",
        "| 组别 | 规模/分布 | 目标 | 卡掉的错误解 |",
        "|---|---|---|---|",
        *rows,
        "",
        "`.in` 最后一行后无换行符；`.out` 末尾恰好一个换行符。",
        "",
        "生成后自校验：滑动窗口必须等于枚举左边 $i$ 张、右边 $k-i$ 张。",
        "",
    ])
    (DATA / "README.md").write_text(readme, encoding="utf-8")
    print("generated 10 cases")
    for i, ans in enumerate(answers, 1):
        print(i, ans, "n", len(metas[i - 1][0]), "k", metas[i - 1][1])


if __name__ == "__main__":
    main()
