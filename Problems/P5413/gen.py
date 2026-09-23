# -*- coding: utf-8 -*-
"""P5413 基站干扰指数：10 组测例。

分层（每组 10 分，合计 100）：
- 1～8：小数据，覆盖样例、最小规模、单调序列、全相等、k=1、窗口内外 NGE
- 9～10：n=1e5 上限，卡 O(nk) 暴力与 int 溢出 / 漏取模
"""
from __future__ import annotations

import random
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
RNG = random.Random(541320260909)
MOD = 10**9 + 7


def total_interference(power: list[int], k: int) -> int:
    n = len(power)
    nge_left = [-1] * n
    stack: list[int] = []
    for i in range(n):
        while stack and power[stack[-1]] <= power[i]:
            stack.pop()
        if stack:
            nge_left[i] = stack[-1]
        stack.append(i)

    nge_right = [-1] * n
    stack = []
    for i in range(n):
        while stack and power[stack[-1]] < power[i]:
            nge_right[stack.pop()] = i
        stack.append(i)

    ans = 0
    for i in range(n):
        left = nge_left[i]
        if left != -1 and i - left <= k:
            ans = (ans + power[i] * (i - left)) % MOD
        right = nge_right[i]
        if right != -1 and right - i <= k:
            ans = (ans + power[i] * (right - i)) % MOD
    return ans


def brute_interference(power: list[int], k: int) -> int:
    """每个位置向左右各扫最多 k 步，用于小数据对照。"""
    n = len(power)
    ans = 0
    for i in range(n):
        for j in range(i - 1, max(-1, i - k - 1), -1):
            if power[j] > power[i]:
                ans = (ans + power[i] * (i - j)) % MOD
                break
        for j in range(i + 1, min(n, i + k + 1)):
            if power[j] > power[i]:
                ans = (ans + power[i] * (j - i)) % MOD
                break
    return ans


def write_in(path: Path, power: list[int], k: int) -> None:
    lines = [" ".join(str(x) for x in power), str(k)]
    # 输入末尾不要换行
    path.write_bytes("\n".join(lines).encode("utf-8"))


def write_out(path: Path, ans: int) -> None:
    # 输出末尾必须有且仅有一个换行
    path.write_bytes((str(ans) + "\n").encode("utf-8"))


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


def write_readme(notes: list[dict]) -> None:
    rows = [
        "| 组别 | 规模/分布 | 生成逻辑 | 卡掉的错误解 |",
        "|---|---|---|---|",
    ]
    for i, note in enumerate(notes, 1):
        rows.append(f"| {i} | {note['scale']} | {note['logic']} | {note['hack']} |")
    text = (
        "# P5413 测试数据说明\n\n"
        "第一行是数组 $a$，第二行是 $t$。每个位置取左右最近严格更大元素，"
        "距离超过 $t$ 则该侧贡献为 $0$，总和对 $10^9+7$ 取模。\n\n"
        + "\n".join(rows)
        + "\n"
    )
    (DATA / "README.md").write_bytes(text.encode("utf-8"))


def build_cases():
    cases = []
    notes = []

    # 1 样例1（二级题面）
    power = [9, 4, 7, 2, 8, 1, 6]
    k = 4
    cases.append((power, k))
    notes.append(
        {
            "scale": "m=7，样例1",
            "logic": "数组 [9,4,7,2,8,1,6]，t=4，最近更大与窗口边界都出现",
            "hack": "在窗口里取最大值而不是第一个更大；相等也当成更大",
        }
    )

    # 2 样例2：t=2，更远处的更大不能用，且有相等值
    power = [8, 3, 3, 12, 5]
    k = 2
    cases.append((power, k))
    notes.append(
        {
            "scale": "m=5，样例2",
            "logic": "t=2，下标 0 右侧真正的更大元素 12 距离为 3，不能计入；相邻 3 相等不算更大",
            "hack": "忽略 t，直接用全局 NGE；把相等当成严格更大",
        }
    )

    # 3 n=1
    power = [123]
    k = 1
    cases.append((power, k))
    notes.append(
        {
            "scale": "n=1，最小值",
            "logic": "只有一座基站，左右都无邻居，答案为 0",
            "hack": "越界访问；把 k 当成下标",
        }
    )

    # 4 严格递减
    power = [9, 8, 7, 6, 5, 4, 3, 2]
    k = 8
    cases.append((power, k))
    notes.append(
        {
            "scale": "n=8，严格递减",
            "logic": "每个位置左侧最近更大就是左邻，右侧没有更大",
            "hack": "左右方向扫反；把距离写成下标本身",
        }
    )

    # 5 严格递增
    power = [1, 2, 3, 4, 5, 6, 7, 8]
    k = 8
    cases.append((power, k))
    notes.append(
        {
            "scale": "n=8，严格递增",
            "logic": "每个位置右侧最近更大就是右邻，左侧没有更大",
            "hack": "左侧误用 <= 找到自己；右侧跳过紧邻去找更远的最大值",
        }
    )

    # 6 全相等
    power = [7] * 10
    k = 10
    cases.append((power, k))
    notes.append(
        {
            "scale": "n=10，全相等",
            "logic": "严格大于不成立，所有贡献必须为 0",
            "hack": "把 > 写成 >=，会把相邻相等当成干扰源",
        }
    )

    # 7 k=1 且含重复
    power = [5, 6, 6, 4, 9, 1, 8, 8, 2, 10, 3, 3, 7, 11, 12]
    k = 1
    cases.append((power, k))
    notes.append(
        {
            "scale": "n=15，k=1",
            "logic": "只看左右紧邻；重复值不能作为严格更大",
            "hack": "k=1 时仍向远处搜索；相邻相等被计入",
        }
    )

    # 8 最近更大在窗口外 / 窗口内第一个更大不是最大值
    power = [5, 6, 10, 4, 1, 1, 1, 1, 20, 3, 8, 2, 9, 7, 15, 6, 6, 12, 1, 30]
    k = 2
    cases.append((power, k))
    notes.append(
        {
            "scale": "n=20，k=2",
            "logic": "下标 0 的第一个更大是 6 而不是更远的 10；若干位置的 NGE 落在 k 之外",
            "hack": "窗口内取最大值；忽略 k 直接用 NGE",
        }
    )

    # 9 大数据：递减，卡 O(nk)
    n = 10**5
    power = list(range(n, 0, -1))
    k = n
    cases.append((power, k))
    notes.append(
        {
            "scale": "n=100000，严格递减，k=n",
            "logic": "每个位置向右扫描会走完整段，暴力 O(nk) 超时",
            "hack": "每个位置向左右各扫 k 步的朴素解",
        }
    )

    # 10 大数据：大值 + 取模 + 溢出
    n = 10**5
    power = [10**9 - (i % 17) for i in range(n)]
    k = n
    cases.append((power, k))
    notes.append(
        {
            "scale": "n=100000，值接近 1e9，k=n",
            "logic": "乘积达 1e14，总和超过 MOD，必须 64 位并取模",
            "hack": "用 int 乘距离溢出；忘记对 1e9+7 取模",
        }
    )

    return cases, notes


def main():
    DATA.mkdir(parents=True, exist_ok=True)
    cases, notes = build_cases()
    if len(cases) != 10:
        raise SystemExit(f"需要 10 组，实际 {len(cases)}")

    for i, (power, k) in enumerate(cases, 1):
        n = len(power)
        if n < 1 or n > 10**5:
            raise SystemExit(f"第 {i} 组 n={n} 超出约束")
        if k < 1 or k > n:
            raise SystemExit(f"第 {i} 组 k={k} 超出约束")
        for x in power:
            if x < 1 or x > 10**9:
                raise SystemExit(f"第 {i} 组值越界: {x}")

        ans = total_interference(power, k)
        if n <= 2000:
            brute = brute_interference(power, k)
            if ans != brute:
                raise SystemExit(f"第 {i} 组单调栈与暴力不一致: {ans} vs {brute}")

        write_in(DATA / f"{i}.in", power, k)
        write_out(DATA / f"{i}.out", ans)

    write_config()
    write_readme(notes)

    for i in range(1, 11):
        in_path = DATA / f"{i}.in"
        out_path = DATA / f"{i}.out"
        raw = in_path.read_bytes().decode("utf-8")
        if raw.endswith("\n"):
            raise SystemExit(f"{i}.in 末尾多了换行")
        lines = raw.split("\n")
        if len(lines) != 2:
            raise SystemExit(f"{i}.in 行数不是 2")
        power = list(map(int, lines[0].split()))
        k = int(lines[1])
        got = total_interference(power, k)
        expected = int(out_path.read_text(encoding="utf-8").strip())
        if got != expected:
            raise SystemExit(f"{i}.out 不一致: {got} vs {expected}")
        out_bytes = out_path.read_bytes()
        if not out_bytes.endswith(b"\n") or out_bytes.endswith(b"\n\n"):
            raise SystemExit(f"{i}.out 换行不符合「有且仅有一个换行」")

    print("已生成 10 组测例并完成自校验")


if __name__ == "__main__":
    main()
