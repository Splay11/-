# -*- coding: utf-8 -*-
"""P7126 造数：面试区间是否冲突。结束==下一场开始不算冲突。

stdin：第一行 n，接下来 n 行 start end。
输出：YES / NO。
`.in` 最后一行后不留换行；`.out` 末尾恰好一个换行。
"""
from __future__ import annotations

import random
import sys
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
from std import can_attend_all  # noqa: E402

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
RNG = random.Random(712620260914)

N_MAX = 10**4
T_MAX = 10**4


def brute(intervals):
    """任意两段 [s,e) 是否相交。"""
    n = len(intervals)
    for i in range(n):
        s1, e1 = intervals[i]
        for j in range(i + 1, n):
            s2, e2 = intervals[j]
            if s1 < e2 and s2 < e1:
                return False
    return True


def alt_sort_end(intervals):
    arr = sorted(intervals, key=lambda x: (x[0], x[1]))
    last = -1
    for s, e in arr:
        if s < last:
            return False
        last = e
    return True


def case_in_text(intervals):
    lines = [str(len(intervals))]
    for s, e in intervals:
        lines.append(f"{s} {e}")
    return "\n".join(lines)


def write_case(idx, intervals):
    n = len(intervals)
    assert 1 <= n <= N_MAX
    for s, e in intervals:
        assert 0 <= s < e <= T_MAX, (idx, s, e)
    (DATA / f"{idx}.in").write_bytes(case_in_text(intervals).encode("utf-8"))
    ok = can_attend_all(list(intervals))
    ans = "YES" if ok else "NO"
    with open(DATA / f"{idx}.out", "w", encoding="utf-8", newline="\n") as f:
        f.write(ans + "\n")
    return ans


def chain(k, length=1):
    """首尾相接的 k 段。"""
    arr = []
    t = 0
    for _ in range(k):
        arr.append((t, t + length))
        t += length
        if t >= T_MAX:
            break
    return arr


def main():
    DATA.mkdir(parents=True, exist_ok=True)

    rand8 = []
    t = 0
    for _ in range(8):
        length = RNG.randint(1, 5)
        gap = RNG.randint(0, 3)
        t += gap
        if t + length > T_MAX:
            break
        rand8.append((t, t + length))
        t += length
    RNG.shuffle(rand8)

    n9 = N_MAX
    arr9 = [(i, i + 1) for i in range(n9)]
    RNG.shuffle(arr9)

    arr10 = [(i, i + 1) for i in range(N_MAX)]
    arr10[1234] = (100, 250)  # 与 [100,101)...[249,250) 重叠
    RNG.shuffle(arr10)

    plan = [
        ([(1, 3), (2, 6), (8, 10), (15, 18)],
         "样例 1", "有重叠，答案 NO",
         "没检查 $1\\sim3$ 与 $2\\sim6$"),
        ([(1, 4), (4, 5)],
         "样例 2，首尾相接", "答案 YES",
         "把结束时刻等于开始时刻判成冲突"),
        ([(4, 7), (1, 4)],
         "样例 3，输入未排序", "答案 YES",
         "按输入顺序只比相邻，未排序会误判"),
        ([(0, 10000)],
         "最小规模 $n=1$", "答案 YES",
         "单场还判冲突"),
        ([(1, 10), (3, 5)],
         "完全包含", "答案 NO",
         "只判断起点落在开区间内、漏掉被包含的短区间"),
        ([(0, 2), (2, 4), (4, 6), (6, 8)],
         "多场首尾相接", "答案 YES",
         "连锁相接却输出 NO"),
        ([(5, 9), (0, 3), (3, 6)],
         "乱序且中间有重叠", "排序后 $0\\sim3,3\\sim6,5\\sim9$，答案 NO",
         "直接输出 YES"),
        (rand8,
         "小随机，若干段相接或留缝", "暴力两两判断可对拍",
         "比较写成 $\\le$ 把相接当冲突"),
        (arr9,
         "压满 $n=10^4$，每场 $[i,i+1)$，打乱顺序",
         "全部相接，答案 YES",
         "$O(n^2)$ 可能超时；不排序会乱"),
        (arr10,
         "压满 $n=10^4$，其中一场 $[100,250)$ 覆盖一长串",
         "答案 NO",
         "只看输入相邻两项，打乱后漏判"),
    ]
    assert len(plan) == 10

    answers = []
    for idx, (iv, _, _, _) in enumerate(plan, 1):
        answers.append(write_case(idx, iv))

    for i, (iv, _, _, _) in enumerate(plan, 1):
        ib = (DATA / f"{i}.in").read_bytes()
        ob = (DATA / f"{i}.out").read_bytes()
        assert not ib.endswith(b"\n") and b"\r" not in ib, f"{i}.in 换行"
        assert ob.endswith(b"\n") and not ob.endswith(b"\n\n") and b"\r" not in ob

        lines = ib.decode("utf-8").split("\n")
        n = int(lines[0])
        got_iv = [tuple(map(int, lines[j].split())) for j in range(1, n + 1)]
        assert got_iv == list(map(tuple, iv))

        got = ob.decode("utf-8").strip()
        truth = "YES" if can_attend_all(list(iv)) else "NO"
        alt = "YES" if alt_sort_end(iv) else "NO"
        assert got == truth == alt == answers[i - 1], (i, got, truth, alt)
        if i <= 8:
            bf = "YES" if brute(iv) else "NO"
            assert bf == truth, (i, bf, truth)

    assert answers[0] == "NO"
    assert answers[1] == "YES"
    assert answers[2] == "YES"
    assert answers[3] == "YES"
    assert answers[4] == "NO"
    assert answers[5] == "YES"
    assert answers[6] == "NO"
    assert answers[8] == "YES"
    assert answers[9] == "NO"

    rows = []
    for i, (_, scale, goal, hack) in enumerate(plan, 1):
        rows.append(f"| {i} | {scale} | {goal} | {hack} |")

    readme = "\n".join([
        "# P7126 测试数据说明",
        "",
        "主造数脚本：题目根目录 `gen.py`。",
        "stdin：第一行 `n`，接下来 $n$ 行 `start end`。",
        "输出：`YES` 或 `NO`。结束时刻等于下一场开始时刻不算冲突。",
        "",
        r"约束：$1 \le n \le 10^4$，$0 \le start_i < end_i \le 10^4$。",
        "",
        "| 组别 | 规模/分布 | 目标 | 卡掉的错误解 |",
        "|---|---|---|---|",
        *rows,
        "",
        "`.in` 最后一行后无换行符；`.out` 末尾恰好一个换行符。",
        "",
        "生成后自校验：排序扫描与「按起点排序后维护上一结束时刻」一致；第 $1\\sim 8$ 组再用两两暴力交叉校验。",
        "",
    ])
    (DATA / "README.md").write_text(readme, encoding="utf-8")
    print("generated 10 cases")
    for i, ans in enumerate(answers, 1):
        print(i, ans)


if __name__ == "__main__":
    main()
