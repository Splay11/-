# -*- coding: utf-8 -*-
"""P5416 有序数组的四个位置：10 组测例。

分层（每组 10 分，合计 100）：
- 1～8：小数据，覆盖样例、最小规模、全相等、左右越界、插入点、重复簇
- 9～10：n=1e5 上限，一段长重复 / 极值且 T 不在数组中
"""
from __future__ import annotations

import random
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
RNG = random.Random(541620260909)


def query_positions(a, T):
    n = len(a)
    left, right = 0, n
    while left < right:
        mid = (left + right) // 2
        if a[mid] < T:
            left = mid + 1
        else:
            right = mid
    lower = left

    left, right = 0, n
    while left < right:
        mid = (left + right) // 2
        if a[mid] <= T:
            left = mid + 1
        else:
            right = mid
    upper = left

    first = lower if lower < n and a[lower] == T else -1
    last = upper - 1 if upper > 0 and a[upper - 1] == T else -1
    pred = lower - 1 if lower > 0 else -1
    succ = upper if upper < n else -1
    return first, last, pred, succ


def brute_positions(a, T):
    """线性扫描对照，用于小数据自检。"""
    n = len(a)
    first = last = pred = succ = -1
    for i, x in enumerate(a):
        if x == T:
            if first < 0:
                first = i
            last = i
        if x < T:
            pred = i
        if x > T and succ < 0:
            succ = i
    return first, last, pred, succ


def write_in(path: Path, n: int, T: int, a: list[int]) -> None:
    lines = [f"{n} {T}", " ".join(str(x) for x in a)]
    # 输入末尾不要换行
    path.write_bytes("\n".join(lines).encode("utf-8"))


def write_out(path: Path, ans: tuple[int, int, int, int]) -> None:
    # 输出末尾必须有且仅有一个换行
    path.write_bytes((" ".join(str(x) for x in ans) + "\n").encode("utf-8"))


def write_config() -> None:
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


def write_readme(notes: list[str]) -> None:
    rows = [
        "| 组别 | 规模/分布 | 生成逻辑 | 卡掉的错误解 |",
        "|---|---|---|---|",
    ]
    for i, note in enumerate(notes, 1):
        rows.append(f"| {i} | {note['scale']} | {note['logic']} | {note['hack']} |")
    text = (
        "# P5416 测试数据说明\n\n"
        "下标从 $0$ 开始。四个答案依次为：$T$ 首次、$T$ 末次、严格小于 $T$ 的最大下标、严格大于 $T$ 的最小下标；不存在则 $-1$。\n\n"
        + "\n".join(rows)
        + "\n"
    )
    (DATA / "README.md").write_bytes(text.encode("utf-8"))


def sorted_unique_cluster(values: list[int]) -> list[int]:
    return sorted(values)


def build_cases():
    cases = []
    notes = []

    # 1 样例1：T 有重复
    a = [1, 2, 2, 2, 4]
    T = 2
    cases.append((T, a))
    notes.append(
        {
            "scale": "n=5，样例1",
            "logic": "数组 [1,2,2,2,4]，T=2，覆盖一段重复值的两端邻居",
            "hack": "1-indexed 输出；把 last 写成 first+1",
        }
    )

    # 2 样例2：T 不存在
    a = [1, 2, 4, 5]
    T = 3
    cases.append((T, a))
    notes.append(
        {
            "scale": "n=4，样例2",
            "logic": "T=3 夹在 2 与 4 之间，数组中不出现",
            "hack": "T 不存在时把 first/last 写成插入点而不是 -1",
        }
    )

    # 3 n=1 且命中
    a = [7]
    T = 7
    cases.append((T, a))
    notes.append(
        {
            "scale": "n=1，命中",
            "logic": "单元素等于 T",
            "hack": "pred/succ 误写成 0；first/last 写成 1",
        }
    )

    # 4 n=1 且 T 更小
    a = [7]
    T = -10
    cases.append((T, a))
    notes.append(
        {
            "scale": "n=1，T 小于唯一元素",
            "logic": "没有小于 T 的下标，succ 应为 0",
            "hack": "pred 写成 0；succ 写成 1 或 n",
        }
    )

    # 5 全部等于 T
    a = [5] * 12
    T = 5
    cases.append((T, a))
    notes.append(
        {
            "scale": "n=12，全相等",
            "logic": "每个元素都是 T，first=0，last=n-1，左右邻居都不存在",
            "hack": "pred 写成 -1 以外的值；succ 输出 n",
        }
    )

    # 6 T 大于全部，含负数
    a = [-1000000000, -3, -3, 0, 8, 8, 9]
    T = 1000000000
    cases.append((T, a))
    notes.append(
        {
            "scale": "n=7，含负数与值域边界",
            "logic": "T 大于全部元素，first/last/succ 均为 -1，pred=n-1",
            "hack": "succ 输出 n；整数比较时把 1e9 当越界",
        }
    )

    # 7 T 不存在但夹在两段重复之间
    a = [-2, -2, -2, 4, 4, 4, 4, 9, 9]
    T = 0
    cases.append((T, a))
    notes.append(
        {
            "scale": "n=9，两段重复夹空档",
            "logic": "T=0 不出现，pred 落在 -2 段末尾，succ 落在 4 段开头",
            "hack": "把 < 写成 <=，pred 会落到 4 段；lower/upper 搞反",
        }
    )

    # 8 随机小数据：多簇重复，T 命中其中一簇
    vals = []
    base = -50
    for _ in range(8):
        run = RNG.randint(1, 4)
        vals.extend([base] * run)
        base += RNG.randint(1, 12)
    T = vals[len(vals) // 2]
    cases.append((T, vals))
    notes.append(
        {
            "scale": f"n={len(vals)}，随机重复簇",
            "logic": "八段随机长度的重复簇，T 取中间某个已有值",
            "hack": "重复值时二分左右边界写错，last 不等于整段右端",
        }
    )

    # 9 大数据：中间超长重复段
    n = 10**5
    left_run = [0] * 1234
    mid_run = [7] * 80000
    right_run = [100] * (n - len(left_run) - len(mid_run))
    a = left_run + mid_run + right_run
    T = 7
    cases.append((T, a))
    notes.append(
        {
            "scale": "n=100000，中间 80000 个 7",
            "logic": "T 命中超长重复段，first/last 跨度很大",
            "hack": "只找到第一个就当 last；或线性扫错写成 first+1",
        }
    )

    # 10 大数据：T 不在数组，值域拉满
    n = 10**5
    a = list(range(-50000, 50000))
    T = 10**9
    cases.append((T, a))
    notes.append(
        {
            "scale": "n=100000，T=1e9 不在数组",
            "logic": "严格递增填满约 [-5e4,5e4)，T 大于全部",
            "hack": "succ 输出 n；T 不存在时 first 写成 n 或 0",
        }
    )

    return cases, notes


def main():
    DATA.mkdir(parents=True, exist_ok=True)
    cases, notes = build_cases()
    if len(cases) != 10:
        raise SystemExit(f"需要 10 组，实际 {len(cases)}")

    for i, (T, a) in enumerate(cases, 1):
        n = len(a)
        if n < 1 or n > 10**5:
            raise SystemExit(f"第 {i} 组 n={n} 超出约束")
        if a != sorted(a):
            raise SystemExit(f"第 {i} 组不是非递减")
        for x in a + [T]:
            if x < -(10**9) or x > 10**9:
                raise SystemExit(f"第 {i} 组值越界: {x}")

        ans = query_positions(a, T)
        if n <= 2000:
            brute = brute_positions(a, T)
            if ans != brute:
                raise SystemExit(f"第 {i} 组二分与暴力不一致: {ans} vs {brute}")

        write_in(DATA / f"{i}.in", n, T, a)
        write_out(DATA / f"{i}.out", ans)

    write_config()
    write_readme(notes)

    # 生成后自校验：重新读入并用解题逻辑比对
    for i in range(1, 11):
        in_path = DATA / f"{i}.in"
        out_path = DATA / f"{i}.out"
        raw = in_path.read_bytes().decode("utf-8")
        if raw.endswith("\n"):
            raise SystemExit(f"{i}.in 末尾多了换行")
        lines = raw.split("\n")
        n, T = map(int, lines[0].split())
        a = list(map(int, lines[1].split()))
        if len(a) != n:
            raise SystemExit(f"{i}.in 长度与 n 不符")
        got = query_positions(a, T)
        expected = tuple(map(int, out_path.read_text(encoding="utf-8").strip().split()))
        if got != expected:
            raise SystemExit(f"{i}.out 不一致: {got} vs {expected}")
        out_bytes = out_path.read_bytes()
        if not out_bytes.endswith(b"\n") or out_bytes.endswith(b"\n\n"):
            raise SystemExit(f"{i}.out 换行不符合「有且仅有一个换行」")

    print("已生成 10 组测例并完成自校验")


if __name__ == "__main__":
    main()
