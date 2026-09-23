# -*- coding: utf-8 -*-
"""P7130 造数：双向循环链表头插（允许空表）。

stdin：第一行 n x；n>0 时第二行 n 个整数；n=0 时第二行省略。
输出：新头沿后继走一圈的节点值。
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
RNG = random.Random(713020260914)

N_MAX = 10**4
V_LO, V_HI = -(10**9), 10**9


def naive(vals, x):
    return [x] + list(vals)


def case_in_text(n, x, vals):
    if n == 0:
        return f"{n} {x}"
    return f"{n} {x}\n" + " ".join(map(str, vals))


def write_case(idx, x, vals):
    n = len(vals)
    assert 0 <= n <= N_MAX
    assert V_LO <= x <= V_HI
    assert all(V_LO <= v <= V_HI for v in vals)
    (DATA / f"{idx}.in").write_bytes(case_in_text(n, x, vals).encode("utf-8"))
    ans = insert_and_list(vals, x)
    expect = naive(vals, x)
    assert ans == expect, (idx, ans[:8], expect[:8])
    with open(DATA / f"{idx}.out", "w", encoding="utf-8", newline="\n") as f:
        f.write(" ".join(map(str, ans)) + "\n")
    return ans


def main():
    DATA.mkdir(parents=True, exist_ok=True)

    rand8 = [RNG.randint(-100, 100) for _ in range(15)]
    x8 = RNG.randint(-100, 100)
    big9 = [(i % 2000000001) - 1000000000 for i in range(N_MAX)]
    assert len(big9) == N_MAX
    big10 = [RNG.randint(V_LO, V_HI) for _ in range(N_MAX)]
    x10 = RNG.choice([V_LO, V_HI, 0])

    plan = [
        (10, [1, 2, 3, 4],
         "样例 1", "头插 $10$ 得到 $10\\ 1\\ 2\\ 3\\ 4$",
         "接到末尾会得到 $1\\ 2\\ 3\\ 4\\ 10$"),
        (7, [5],
         "样例 2，单节点", "得到 $7\\ 5$，两节点成环",
         "单节点没把头尾接成环"),
        (8, [],
         "样例 3，空链表 $n=0$，无第二行", "只输出 $8$",
         "去读第二行导致 RE；或输出空行"),
        (0, [1, 2],
         "头插 $0$，两节点", "得到 $0\\ 1\\ 2$",
         "把 $0$ 当成空表特殊处理"),
        (-1, [-3, -2, -1],
         "全负数", "得到 $-1\\ -3\\ -2\\ -1$",
         "符号弄丢"),
        (5, [5, 5, 5],
         "新值与原节点重复", "得到 $5\\ 5\\ 5\\ 5$",
         "去重后只留一个 $5$"),
        (1000000000, [-(10**9), 10**9],
         "值域边界", "新头 $10^9$，后接极值",
         "int 溢出"),
        (x8, rand8,
         "小随机 $n=15$", "链表头插与 $[x]+vals$ 对拍",
         "遍历没停在 $n+1$ 步，死循环或少输出"),
        (V_LO, big9,
         "压满 $n=10^4$，插入值域下界", "新头接在序列最前",
         "建表断环，或超时"),
        (x10, big10,
         "压满 $n=10^4$，随机值", "线性建表 + 头插",
         "Java 对 $n=0$ 多读一行在大数据上不易暴露，本组压 I/O"),
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
        text = ib.decode("utf-8")
        lines = text.split("\n")
        hn, hx = map(int, lines[0].split())
        assert hn == len(vals) and hx == x
        if hn == 0:
            assert len(lines) == 1
            assert ob.decode("utf-8").strip() == str(x)
        else:
            arr = list(map(int, lines[1].split()))
            assert arr == vals
            got = list(map(int, ob.decode("utf-8").split()))
            assert got == answers[i - 1] == naive(vals, x)

    assert answers[0] == [10, 1, 2, 3, 4]
    assert answers[1] == [7, 5]
    assert answers[2] == [8]
    assert answers[3] == [0, 1, 2]
    assert answers[4] == [-1, -3, -2, -1]
    assert answers[5] == [5, 5, 5, 5]

    rows = []
    for i, (_, _, scale, goal, hack) in enumerate(plan, 1):
        rows.append(f"| {i} | {scale} | {goal} | {hack} |")

    readme = "\n".join([
        "# P7130 测试数据说明",
        "",
        "主造数脚本：题目根目录 `gen.py`。",
        "stdin：第一行 `n x`；$n>0$ 时第二行 $n$ 个整数；$n=0$ 时没有第二行。",
        "输出：头插后从新头沿后继走一圈的节点值。",
        "",
        r"约束：$0 \le n \le 10^4$，$-10^9 \le a_i,x \le 10^9$。",
        "",
        "| 组别 | 规模/分布 | 目标 | 卡掉的错误解 |",
        "|---|---|---|---|",
        *rows,
        "",
        "`.in` 最后一行后无换行符；`.out` 末尾恰好一个换行符。",
        "",
        "生成后自校验：链表头插结果必须等于 $[x]+vals$。",
        "",
    ])
    (DATA / "README.md").write_text(readme, encoding="utf-8")
    print("generated 10 cases")
    for i, ans in enumerate(answers, 1):
        print(i, "len", len(ans), "head", ans[:5])


if __name__ == "__main__":
    main()
