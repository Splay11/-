# -*- coding: utf-8 -*-
"""P7167 造数：森林兔子最少数量。"""
from __future__ import annotations

import random
import sys
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
from std import solve  # noqa: E402

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
RNG = random.Random(716720260915)
N_MAX = 1000
A_MAX = 999


def one_color(answers):
    """假解：相同回答全算一种颜色。"""
    cnt = {}
    for x in answers:
        cnt[x] = cnt.get(x, 0) + 1
    ans = 0
    for x, c in cnt.items():
        ans += x + 1
    return ans


def write_case(idx, answers):
    n = len(answers)
    assert 1 <= n <= N_MAX
    for x in answers:
        assert 0 <= x < 1000
    ans = solve(answers)
    inp = f"{n}\n" + " ".join(str(x) for x in answers)
    (DATA / f"{idx}.in").write_bytes(inp.encode("utf-8"))
    with open(DATA / f"{idx}.out", "w", encoding="utf-8", newline="\n") as f:
        f.write(str(ans) + "\n")
    return ans


def main():
    DATA.mkdir(parents=True, exist_ok=True)
    overflow_group = [4] * 6  # 两组容量 5，最少 10
    zeros = [0] * 5
    big = [RNG.randint(0, 30) for _ in range(N_MAX)]
    all_same = [999] * N_MAX  # 组大小 1000，1000 只正好一组，答案 1000

    plan = [
        ([1, 1, 2], "样例 1", "5", "把 1 和 2 混成一组"),
        ([10, 10, 10], "样例 2，一组 11 只", "11", "输出 33"),
        ([0], "一只兔子回答 0", "1", "输出 0"),
        (zeros, "5 只都回答 0，各一种颜色", "5", "当成一组输出 1"),
        (overflow_group, "6 只回答 4，需要两组", "10", "只开一组得到 5"),
        ([2, 2, 2], "3 只回答 2，刚好一组", "3", "输出 6"),
        ([1, 1, 1], "3 只回答 1，两组容量 2", "4", "当成一组得到 2"),
        ([RNG.randint(0, 10) for _ in range(40)], "中等随机", "贪心计数", "相同回答不拆组"),
        (big, "压满 n=1000", "O(n)", "暴力枚举颜色分配"),
        (all_same, "压满全是 999", "1000", "输出 1000*1000"),
    ]
    assert one_color(overflow_group) == 5
    assert solve(overflow_group) == 10

    answers, metas = [], []
    for i, (arr, _, _, _) in enumerate(plan, 1):
        metas.append(arr)
        answers.append(write_case(i, arr))
    assert answers[0] == 5 and answers[1] == 11 and answers[3] == 5
    assert answers[4] == 10 and answers[9] == 1000

    for i, arr in enumerate(metas, 1):
        ib = (DATA / f"{i}.in").read_bytes()
        ob = (DATA / f"{i}.out").read_bytes()
        assert not ib.endswith(b"\n") and b"\r" not in ib
        assert ob.endswith(b"\n") and not ob.endswith(b"\n\n")
        assert ib.decode("utf-8") == f"{len(arr)}\n" + " ".join(str(x) for x in arr)

    rows = [f"| {i} | {p[1]} | {p[2]} | {p[3]} |" for i, p in enumerate(plan, 1)]
    (DATA / "README.md").write_text(
        "\n".join([
            "# P7167 测试数据说明",
            "",
            r"主造数脚本：题目根目录 `gen.py`。约束 $1\le n\le 1000$，$0\le answers_i<1000$。",
            "",
            "| 组别 | 规模/分布 | 目标 | 卡掉的错误解 |",
            "|---|---|---|---|",
            *rows,
            "",
            "`.in` 最后一行后无换行符；`.out` 末尾恰好一个换行符。",
            "",
        ]),
        encoding="utf-8",
    )
    print("generated 10 cases")
    for i, a in enumerate(answers, 1):
        print(i, a, "n", len(metas[i - 1]))


if __name__ == "__main__":
    main()
