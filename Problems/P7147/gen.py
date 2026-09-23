# -*- coding: utf-8 -*-
"""P7147 造数：小行星碰撞。

stdin：第一行 n，第二行 n 个非零整数。
输出：第一行 m；m>0 时第二行剩余序列；m=0 时只有一行 0。
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
RNG = random.Random(714720260915)

N_MIN, N_MAX = 2, 10**4
V_MAX = 1000


def naive(a):
    """反复消掉相邻的右行-左行对，与栈模拟对拍。"""
    a = list(a)
    i = 0
    while i < len(a) - 1:
        if a[i] > 0 and a[i + 1] < 0:
            if abs(a[i]) > abs(a[i + 1]):
                del a[i + 1]
            elif abs(a[i]) < abs(a[i + 1]):
                del a[i]
                if i:
                    i -= 1
            else:
                del a[i]
                del a[i]
                if i:
                    i -= 1
        else:
            i += 1
    return a


def fmt_out(rest):
    if not rest:
        return "0\n"
    return str(len(rest)) + "\n" + " ".join(str(x) for x in rest) + "\n"


def write_case(idx, a):
    n = len(a)
    assert N_MIN <= n <= N_MAX
    for x in a:
        assert -V_MAX <= x <= V_MAX and x != 0
    ans = solve(a)
    expect = naive(a)
    assert ans == expect, (idx, ans, expect)
    inp = str(n) + "\n" + " ".join(str(x) for x in a)
    (DATA / f"{idx}.in").write_bytes(inp.encode("utf-8"))
    with open(DATA / f"{idx}.out", "w", encoding="utf-8", newline="\n") as f:
        f.write(fmt_out(ans))
    return ans


def rand_val():
    x = RNG.randint(1, V_MAX)
    return x if RNG.random() < 0.5 else -x


def main():
    DATA.mkdir(parents=True, exist_ok=True)

    p8 = [rand_val() for _ in range(20)]
    p9 = [rand_val() for _ in range(N_MAX)]
    # 一长串向右再一颗很大的向左，强迫连锁碰撞
    p10 = [RNG.randint(1, 50) for _ in range(N_MAX - 1)] + [-1000]

    plan = [
        ([5, 10, -5],
         "样例 1", "$5$ 与 $10$ 同向保留",
         "把 $10$ 也炸掉"),
        ([8, -8],
         "样例 2，大小相等", "全部爆炸，只输出 $0$",
         "输出空行或 $8$ $-8$"),
        ([10, 2, -5],
         "样例 3，连锁碰撞", "只剩 $10$",
         "只撞一次得到 $10$ $-5$"),
        ([3, 5, -6, 2, -1, 4],
         "样例 4，先清左边再处理右边", "$-6$ $2$ $4$",
         "让 $-6$ 去撞右边的 $2$"),
        ([-2, 1],
         "背向飞走", "两颗都留",
         "误判为相向碰撞"),
        ([1, 2, 3, 4],
         "全部向右", "原序列",
         "同向也互相抵消"),
        ([-4, -3, -2, -1],
         "全部向左", "原序列",
         "同向也互相抵消"),
        (p8,
         "小随机正负交错", "栈模拟与相邻消除对拍",
         "只比较符号不比绝对值"),
        (p9,
         "压满 $10^4$ 随机", "线性栈",
         "$O(n^2)$ 每次从头扫描可能 TLE"),
        (p10,
         "压满 $10^4$，右侧大质量向左清场", "连锁弹栈",
         "不循环碰撞导致大量右行残留"),
    ]
    assert len(plan) == 10

    answers = []
    arrays = []
    for idx, (a, _, _, _) in enumerate(plan, 1):
        arrays.append(a)
        answers.append(write_case(idx, a))

    for i, a in enumerate(arrays, 1):
        ib = (DATA / f"{i}.in").read_bytes()
        ob = (DATA / f"{i}.out").read_bytes()
        assert not ib.endswith(b"\n") and b"\r" not in ib, f"{i}.in"
        assert ob.endswith(b"\n") and not ob.endswith(b"\n\n") and b"\r" not in ob
        expect_in = str(len(a)) + "\n" + " ".join(str(x) for x in a)
        assert ib.decode("utf-8") == expect_in
        got = ob.decode("utf-8")
        assert got == fmt_out(answers[i - 1])
        assert answers[i - 1] == naive(a)

    assert answers[0] == [5, 10]
    assert answers[1] == []
    assert answers[2] == [10]
    assert answers[3] == [-6, 2, 4]
    assert answers[4] == [-2, 1]
    assert answers[5] == [1, 2, 3, 4]
    assert answers[6] == [-4, -3, -2, -1]
    assert len(arrays[8]) == N_MAX and len(arrays[9]) == N_MAX

    rows = []
    for i, (_, scale, goal, hack) in enumerate(plan, 1):
        rows.append(f"| {i} | {scale} | {goal} | {hack} |")

    readme = "\n".join([
        "# P7147 测试数据说明",
        "",
        "主造数脚本：题目根目录 `gen.py`。",
        "stdin：第一行 $n$，第二行 $n$ 个非零整数。",
        "输出：第一行剩余数量 $m$；$m>0$ 时第二行剩余序列；$m=0$ 时只有一行 $0$。",
        "",
        r"约束：$2\le n\le 10^4$，$-1000\le asteroids_i\le 1000$ 且不为 $0$。",
        "",
        "| 组别 | 规模/分布 | 目标 | 卡掉的错误解 |",
        "|---|---|---|---|",
        *rows,
        "",
        "`.in` 最后一行后无换行符；`.out` 末尾恰好一个换行符。",
        "",
        "生成后自校验：栈模拟必须等于反复消除相邻相向对。",
        "",
    ])
    (DATA / "README.md").write_text(readme, encoding="utf-8")
    print("generated 10 cases")
    for i, ans in enumerate(answers, 1):
        print(i, ans[:8], "n", len(arrays[i - 1]), "m", len(ans))


if __name__ == "__main__":
    main()
