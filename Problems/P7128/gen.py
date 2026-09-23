# -*- coding: utf-8 -*-
"""P7128 造数：单链表向右旋转 k 位。

stdin：第一行 n k；n>0 时第二行 n 个整数。n=0 时第二行可省略。
输出：旋转后的序列；空链表输出空行。
`.in` 最后一行后不留换行；`.out` 末尾恰好一个换行。
"""
from __future__ import annotations

import random
import sys
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
from std import rotate_vals  # noqa: E402

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
RNG = random.Random(712820260914)

N_MAX = 500
V_LO, V_HI = -100, 100
K_MAX = 2 * 10**9


def naive(vals, k):
    n = len(vals)
    if n == 0:
        return []
    k %= n
    if k == 0:
        return list(vals)
    return list(vals[-k:] + vals[:-k])


def case_in_text(n, k, vals):
    if n == 0:
        return f"{n} {k}"
    return f"{n} {k}\n" + " ".join(map(str, vals))


def write_case(idx, k, vals):
    n = len(vals)
    assert 0 <= n <= N_MAX
    assert 0 <= k <= K_MAX
    assert all(V_LO <= v <= V_HI for v in vals)
    (DATA / f"{idx}.in").write_bytes(case_in_text(n, k, vals).encode("utf-8"))
    ans = rotate_vals(vals, k) if n else []
    expect = naive(vals, k)
    assert ans == expect, (idx, ans[:8], expect[:8])
    with open(DATA / f"{idx}.out", "w", encoding="utf-8", newline="\n") as f:
        if not ans:
            f.write("\n")
        else:
            f.write(" ".join(map(str, ans)) + "\n")
    return ans


def main():
    DATA.mkdir(parents=True, exist_ok=True)

    rand8 = [RNG.randint(V_LO, V_HI) for _ in range(11)]
    k8 = RNG.randint(0, 40)
    big9 = [(i % 201) - 100 for i in range(N_MAX)]
    assert len(big9) == N_MAX
    big10 = [RNG.randint(V_LO, V_HI) for _ in range(N_MAX)]

    plan = [
        (2, [1, 2, 3, 4, 5],
         "样例 1", "右旋 $2$ 得到 $4\\ 5\\ 1\\ 2\\ 3$",
         "做成左旋会得到 $3\\ 4\\ 5\\ 1\\ 2$"),
        (4, [0, 1, 2],
         "样例 2，$k>n$", "$4\\bmod 3=1$，得到 $2\\ 0\\ 1$",
         "不对 $n$ 取模，或取模用错"),
        (5, [],
         "空链表 $n=0$，无第二行", "输出空行",
         "去读第二行导致 RE；或输出 $0$"),
        (100, [7],
         "单节点，任意 $k$", "仍是 $7$",
         "取模除零"),
        (0, [1, 2, 3, 4],
         "$k=0$ 不旋转", "原序列",
         "仍然移动节点"),
        (6, [1, 2, 3],
         "$k$ 是 $n$ 的倍数", "回到原序列 $1\\ 2\\ 3$",
         "没取模转了 $6$ 次但断链"),
        (1, [-5, -4, -3],
         "右旋 $1$，含负数", "$-3\\ -5\\ -4$",
         "符号弄丢"),
        (k8, rand8,
         "小随机 $n=11$", "切片拼接与链表旋转对拍",
         "新尾 $next$ 没置空导致多输出"),
        (K_MAX, big9,
         "压满 $n=500$，$k=2\\times 10^9$",
         "$k\\bmod n=0$，输出原序列",
         "真的循环 $k$ 次会 TLE"),
        (K_MAX - 1, big10,
         "压满 $n=500$，$k=2\\times 10^9-1$，余数非 $0$",
         "先取模再旋",
         "int 溢出存 $k$，或左旋"),
    ]
    assert len(plan) == 10

    answers = []
    for idx, (k, vals, _, _, _) in enumerate(plan, 1):
        answers.append(write_case(idx, k, vals))

    for i, (k, vals, _, _, _) in enumerate(plan, 1):
        ib = (DATA / f"{i}.in").read_bytes()
        ob = (DATA / f"{i}.out").read_bytes()
        assert not ib.endswith(b"\n") and b"\r" not in ib, f"{i}.in"
        assert ob.endswith(b"\n") and not ob.endswith(b"\n\n") and b"\r" not in ob
        text = ib.decode("utf-8")
        lines = text.split("\n")
        hn, hk = map(int, lines[0].split())
        assert hn == len(vals) and hk == k
        if hn == 0:
            assert len(lines) == 1
            assert ob == b"\n"
        else:
            arr = list(map(int, lines[1].split()))
            assert arr == vals
            got = list(map(int, ob.decode("utf-8").split()))
            assert got == answers[i - 1] == naive(vals, k)

    assert answers[0] == [4, 5, 1, 2, 3]
    assert answers[1] == [2, 0, 1]
    assert answers[2] == []
    assert answers[3] == [7]
    assert answers[4] == [1, 2, 3, 4]
    assert answers[5] == [1, 2, 3]

    rows = []
    for i, (_, _, scale, goal, hack) in enumerate(plan, 1):
        rows.append(f"| {i} | {scale} | {goal} | {hack} |")

    readme = "\n".join([
        "# P7128 测试数据说明",
        "",
        "主造数脚本：题目根目录 `gen.py`。",
        "stdin：第一行 `n k`；$n>0$ 时第二行 $n$ 个整数；$n=0$ 时没有第二行。",
        "输出：右旋后的节点值；空链表为单独空行。",
        "",
        r"约束：$0 \le n \le 500$，$-100 \le a_i \le 100$，$0 \le k \le 2\times 10^9$。",
        "",
        "| 组别 | 规模/分布 | 目标 | 卡掉的错误解 |",
        "|---|---|---|---|",
        *rows,
        "",
        "`.in` 最后一行后无换行符；`.out` 末尾恰好一个换行符。",
        "",
        "生成后自校验：链表旋转结果必须等于 $vals[-k:]+vals[:-k]$（先 $k\\bmod n$）。",
        "",
    ])
    (DATA / "README.md").write_text(readme, encoding="utf-8")
    print("generated 10 cases")
    for i, ans in enumerate(answers, 1):
        print(i, "len", len(ans), "head", ans[:5] if ans else [])


if __name__ == "__main__":
    main()
