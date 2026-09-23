# -*- coding: utf-8 -*-
"""P7127 造数：双向循环链表头插。

stdin：第一行 n x，第二行 n 个整数。
输出：x 接在原序列前面，共 n+1 个数。
`.in` 最后一行后不留换行；`.out` 末尾恰好一个换行。
"""
from __future__ import annotations

import random
import sys
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
from std import insert_and_list  # noqa: E402

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
RNG = random.Random(712720260914)

N_MAX = 10**4
V_LO, V_HI = -10**9, 10**9


def naive(vals, x):
    return [x] + list(vals)


def case_in_text(n, x, vals):
    return f"{n} {x}\n" + " ".join(map(str, vals))


def write_case(idx, x, vals):
    n = len(vals)
    assert 1 <= n <= N_MAX
    assert V_LO <= x <= V_HI
    assert all(V_LO <= v <= V_HI for v in vals)
    (DATA / f"{idx}.in").write_bytes(case_in_text(n, x, vals).encode("utf-8"))
    ans = insert_and_list(vals, x)
    expect = naive(vals, x)
    assert ans == expect, (idx, ans[:5], expect[:5])
    with open(DATA / f"{idx}.out", "w", encoding="utf-8", newline="\n") as f:
        f.write(" ".join(map(str, ans)) + "\n")
    return ans


def main():
    DATA.mkdir(parents=True, exist_ok=True)

    rand8 = [RNG.randint(V_LO, V_HI) for _ in range(12)]
    x8 = RNG.randint(V_LO, V_HI)
    big9 = list(range(N_MAX))
    big10 = [RNG.randint(V_LO, V_HI) for _ in range(N_MAX)]
    x10 = -10**9

    plan = [
        (10, [1, 2, 3, 4],
         "样例 1", "输出 $10\\ 1\\ 2\\ 3\\ 4$",
         "把 $x$ 接到末尾，或漏掉原序列"),
        (5, [7, 8, 9],
         "样例 2", "输出 $5\\ 7\\ 8\\ 9$",
         "只输出原序列"),
        (100, [5],
         "最小规模 $n=1$", "输出 $100\\ 5$，单节点自环后头插",
         "单节点时 $prev/next$ 没接成环，插入后死循环或崩溃"),
        (-1, [-2, -3, -4],
         "全负数", "输出 $-1\\ -2\\ -3\\ -4$",
         "按无符号输出"),
        (2, [2, 2, 2],
         "$x$ 与原值相同", "输出四个 $2$",
         "去重或跳过相同值"),
        (-10**9, [10**9, 0, -10**9],
         "值域两端", "新头是 $-10^9$",
         "32 位不够"),
        (0, [9, 8, 7, 6, 5],
         "逆序原链", "新头 $0$ 后保持逆序",
         "插入时把链表方向接反"),
        (x8, rand8,
         "小随机 $n=12$", "链表遍历与直接拼接应对上",
         "遍历多走或少走一圈"),
        (123, big9,
         "压满 $n=10^4$，值为 $0..n-1$",
         "输出 $123$ 再接 $0$ 到 $9999$",
         "建表 $O(n^2)$ 或遍历不终止"),
        (x10, big10,
         "压满 $n=10^4$，随机含负数",
         "新头为 $-10^9$",
         "读入/输出超时或断环"),
    ]
    assert len(plan) == 10

    answers = []
    for idx, (x, vals, _, _, _) in enumerate(plan, 1):
        answers.append(write_case(idx, x, vals))

    for i, (x, vals, _, _, _) in enumerate(plan, 1):
        ib = (DATA / f"{i}.in").read_bytes()
        ob = (DATA / f"{i}.out").read_bytes()
        assert not ib.endswith(b"\n") and b"\r" not in ib, f"{i}.in"
        assert ob.endswith(b"\n") and not ob.endswith(b"\n\n") and b"\r" not in ob
        lines = ib.decode("utf-8").split("\n")
        hn, hx = map(int, lines[0].split())
        arr = list(map(int, lines[1].split()))
        assert hn == len(vals) == len(arr) and hx == x and arr == vals
        got = list(map(int, ob.decode("utf-8").split()))
        assert got == answers[i - 1] == [x] + vals

    assert answers[0] == [10, 1, 2, 3, 4]
    assert answers[1] == [5, 7, 8, 9]
    assert answers[2] == [100, 5]

    rows = []
    for i, (_, _, scale, goal, hack) in enumerate(plan, 1):
        rows.append(f"| {i} | {scale} | {goal} | {hack} |")

    readme = "\n".join([
        "# P7127 测试数据说明",
        "",
        "主造数脚本：题目根目录 `gen.py`。",
        "stdin：第一行 `n x`，第二行 $n$ 个整数（原链表从头沿后继的值）。",
        "输出：$n+1$ 个数，值为 $x$ 的新头接在原序列前面。",
        "",
        r"约束：$1 \le n \le 10^4$，$-10^9 \le a_i,x \le 10^9$。",
        "",
        "| 组别 | 规模/分布 | 目标 | 卡掉的错误解 |",
        "|---|---|---|---|",
        *rows,
        "",
        "`.in` 最后一行后无换行符；`.out` 末尾恰好一个换行符。",
        "",
        "生成后自校验：真实双向循环链表头插遍历的结果，必须等于把 $x$ 直接拼在序列前面。",
        "",
    ])
    (DATA / "README.md").write_text(readme, encoding="utf-8")
    print("generated 10 cases")
    for i, ans in enumerate(answers, 1):
        print(i, "len", len(ans), "head", ans[0])


if __name__ == "__main__":
    main()
