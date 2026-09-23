# -*- coding: utf-8 -*-
"""P5557 工位等量连搬：10 组测例。"""
from __future__ import annotations

import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
from std import count_runs, solve_cases  # noqa: E402

DATA = ROOT / "data"
RNG = random.Random(555720260922)


def write_in(path: Path, cases: list[list[int]]) -> None:
    lines = [str(len(cases))]
    for xs in cases:
        lines.append(str(len(xs)) + " " + " ".join(str(x) for x in xs))
    # 最后一行后面不加换行
    path.write_bytes("\n".join(lines).encode("utf-8"))


def write_out(path: Path, ans: list[int]) -> None:
    path.write_bytes((" ".join(str(x) for x in ans) + "\n").encode("utf-8"))


def distinct_wrong(xs: list[int]) -> int:
    # 把全局不同取值个数当成答案，会漏掉隔开的同值段
    return len(set(xs))


def forget_last_wrong(xs: list[int]) -> int:
    # 只统计变化次数，漏掉第一段
    return sum(1 for i in range(1, len(xs)) if xs[i] != xs[i - 1])


def collapse_better(xs: list[int]) -> int:
    # 允许中间段消失后左右贴合。这里用一种确定策略：反复删掉两侧同值的中间段
    runs = []
    for x in xs:
        if runs and runs[-1][0] == x:
            runs[-1][1] += 1
        else:
            runs.append([x, 1])
    ops = 0
    changed = True
    while changed:
        changed = False
        i = 1
        while i < len(runs) - 1:
            if runs[i - 1][0] == runs[i + 1][0]:
                ops += 1
                runs[i - 1][1] += runs[i + 1][1]
                del runs[i:i + 2]
                changed = True
                break
            i += 1
    ops += len(runs)
    return ops


def dump_case(idx: int, cases: list[list[int]]) -> list[int]:
    ans = solve_cases(cases)
    write_in(DATA / f"{idx}.in", cases)
    write_out(DATA / f"{idx}.out", ans)
    return ans


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)

    # 1 样例 1：多段与整行同值
    s1 = [[4, 4, 4, 1, 1, 9, 9], [8, 8, 8, 8]]
    # 2 样例 2：同值被隔开，不能并段
    s2 = [[5, 5, 7, 7, 5, 5]]
    # 3 基础：单工位、全不同、全相同、两段
    s3 = [[7], [1, 2, 3], [9, 9, 9, 9], [2, 2, 2, 5, 5]]
    # 4 边界：最小值、最大值、交替打满段数
    s4 = [[1], [100000], [1, 100000, 1, 100000, 1, 100000, 1, 100000]]
    # 5 小随机
    s5 = []
    for _ in range(6):
        m = RNG.randint(5, 40)
        s5.append([RNG.randint(1, 8) for _ in range(m)])
    # 6 构造：严格递增、全相同、变化落在两端
    s6 = [
        list(range(1, 31)),
        [100000] * 50,
        [3] * 20 + [4],
        [4] + [3] * 20,
    ]
    # 7 针对性：交替与成对重复，全局去重会偏小
    s7 = [[1, 2] * 100, [1, 1, 2, 2] * 50]
    # 8 针对性：漏最后一段；中间删掉后左右会贴合的错解
    s8 = [[4, 4, 4, 4, 4, 1], [1, 1, 1, 1, 2], [3, 3, 1, 1, 3, 3, 3]]
    # 9 大数据：询问数与工位数拉满，交替迫使段数等于 m
    s9 = [[1, 2] * 50000 for _ in range(10)]
    # 10 大数据：值域上界 + 可被“贴合”错解压短的周期
    block = [100000, 100000, 1]
    s10 = [(block * 33333 + [100000]) for _ in range(10)]

    groups = [s1, s2, s3, s4, s5, s6, s7, s8, s9, s10]
    previews = []
    for i, cases in enumerate(groups, 1):
        ans = dump_case(i, cases)
        previews.append(ans[:8])
        for xs, one in zip(cases, ans):
            assert count_runs(xs) == one
            assert 1 <= len(xs) <= 100000
            assert all(1 <= x <= 100000 for x in xs)
        assert 1 <= len(cases) <= 10

    # 样例手算
    assert previews[0] == [3, 1]
    assert previews[1] == [3]
    assert previews[2] == [1, 3, 1, 2]
    assert previews[3] == [1, 1, 8]
    # 去重错解
    assert distinct_wrong(s2[0]) != count_runs(s2[0])
    assert distinct_wrong(s4[2]) != count_runs(s4[2])
    assert distinct_wrong(s7[0]) != count_runs(s7[0])
    assert distinct_wrong(s9[0]) != count_runs(s9[0])
    # 漏第一段
    assert forget_last_wrong(s8[0]) != count_runs(s8[0])
    assert forget_last_wrong(s6[2]) != count_runs(s6[2])
    # 清空后左右贴合
    assert collapse_better(s8[2]) != count_runs(s8[2])
    assert collapse_better(s10[0]) != count_runs(s10[0])
    assert count_runs(s9[0]) == 100000
    assert count_runs(s10[0]) == 66667

    # 用标程重读全部 .in，核对 .out
    for i in range(1, 11):
        text = (DATA / f"{i}.in").read_bytes()
        assert not text.endswith(b"\n")
        lines = text.decode("utf-8").split("\n")
        q = int(lines[0])
        cases = []
        for line in lines[1:]:
            row = list(map(int, line.split()))
            cases.append(row[1:1 + row[0]])
        assert len(cases) == q
        expect = solve_cases(cases)
        out = (DATA / f"{i}.out").read_bytes()
        assert out.endswith(b"\n") and not out.endswith(b"\n\n")
        got = list(map(int, out.decode("utf-8").strip().split()))
        assert got == expect, (i, got[:5], expect[:5])

    print("ok")
    for i, ans in enumerate(previews, 1):
        print(i, ans)


if __name__ == "__main__":
    main()
