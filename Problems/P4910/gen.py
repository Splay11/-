# -*- coding: utf-8 -*-
"""
P4910 测试数据生成器：平稳段最大长度。
固定种子；生成后自校验与 std 逻辑一致。
.in 最后一行末尾无换行；.out 末尾有且仅有一个换行。
"""
import os
import random

RNG = random.Random(491001)

SUM_N_MAX = 200000


def max_stable_len(n, d, a):
    ans = 1
    cur = 1
    for i in range(1, n):
        if abs(a[i] - a[i - 1]) <= d:
            cur += 1
        else:
            cur = 1
        if cur > ans:
            ans = cur
    return ans


def solve_input_text(inp: str):
    lines = inp.strip().splitlines()
    idx = 0
    t = int(lines[idx])
    idx += 1
    outs = []
    for _ in range(t):
        n, d = map(int, lines[idx].split())
        idx += 1
        a = list(map(int, lines[idx].split()))
        idx += 1
        outs.append(str(max_stable_len(n, d, a)))
    return "\n".join(outs) + "\n"


def write_in(path: str, text: str):
    text = text.rstrip("\n")
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)


def write_out(path: str, text: str):
    if not text.endswith("\n"):
        text += "\n"
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)


def gen1_sample():
    # 样例形态：与题面示例一致
    return """2
5 2
3 4 7 6 7
1 0
100"""


def gen2_minimal():
    return """1
1 0
0"""


def gen3_all_equal():
    # 边界：d=0 且全相等，整段连通
    n = 5000
    v = RNG.randint(-10**9, 10**9)
    a = [v] * n
    return "\n".join(["1", f"{n} 0", " ".join(map(str, a))])


def gen4_d0_alternating():
    # hack：d=0 时只有相邻相等才能连；交替值答案恒为 1
    n = 8000
    a = []
    for i in range(n):
        a.append(0 if i % 2 == 0 else 1)
    return "\n".join(["1", f"{n} 0", " ".join(map(str, a))])


def gen5_small_random():
    parts = []
    total_n = 0
    cases = []
    while len(cases) < 40 and total_n + 50 <= SUM_N_MAX:
        n = RNG.randint(1, 50)
        if total_n + n > SUM_N_MAX:
            break
        d = RNG.randint(0, 10**6)
        a = [RNG.randint(-10**6, 10**6) for _ in range(n)]
        cases.append((n, d, a))
        total_n += n
    parts.append(str(len(cases)))
    for n, d, a in cases:
        parts.append(f"{n} {d}")
        parts.append(" ".join(map(str, a)))
    return "\n".join(parts)


def gen6_staircase():
    # 构造：步长 1，d=1，全长连通
    n = 60000
    start = RNG.randint(-5 * 10**8, 5 * 10**8)
    a = [start + i for i in range(n)]
    return "\n".join(["1", f"{n} 1", " ".join(map(str, a))])


def gen7_two_runs():
    # 构造：前半连通、后半连通，中间一次大跳断掉
    n1, n2 = 30000, 30000
    n = n1 + n2
    d = 1
    left = [100 + i for i in range(n1)]
    gap = 1000000000
    first_right = left[-1] + gap
    right = [first_right + i for i in range(n2)]
    a = left + right
    return "\n".join(["1", f"{n} {d}", " ".join(map(str, a))])


def gen8_large_d():
    # 任意相邻差都不超过极大 d，整段
    n = 40000
    a = [RNG.randint(-10**9, 10**9) for _ in range(n)]
    return "\n".join(["1", f"{n} {10**9}", " ".join(map(str, a))])


def gen9_single_large_n():
    # 压力：单组 n 拉满量级（与题面 sum n 上限一致）
    n = SUM_N_MAX
    d = RNG.randint(0, 10**6)
    a = []
    x = RNG.randint(-10**8, 10**8)
    for _ in range(n):
        a.append(x)
        step = RNG.randint(-d, d)
        x += step
    return "\n".join(["1", f"{n} {d}", " ".join(map(str, a))])


def gen10_many_groups():
    # 压力：多组小 n，总和逼近上限
    cases = []
    total = 0
    while total < SUM_N_MAX:
        rest = SUM_N_MAX - total
        n = RNG.randint(1, min(7, rest))
        if n == 0:
            break
        d = RNG.randint(0, 10**9)
        a = [RNG.randint(-10**9, 10**9) for _ in range(n)]
        cases.append((n, d, a))
        total += n
    parts = [str(len(cases))]
    for n, d, a in cases:
        parts.append(f"{n} {d}")
        parts.append(" ".join(map(str, a)))
    return "\n".join(parts)


def main():
    root = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(root, "data")
    os.makedirs(data_dir, exist_ok=True)

    generators = [
        ("题面样例复现；格式与边界行为检查", gen1_sample),
        ("最小规模 n=1", gen2_minimal),
        ("d=0 全相等，最长为整段", gen3_all_equal),
        ("hack：d=0 交替序列，错误合并/非连续段会错", gen4_d0_alternating),
        ("多组随机小 n，暴力对拍友好", gen5_small_random),
        ("构造单调步长 1，d=1 全长", gen6_staircase),
        ("构造中间断裂，检测两侧最长段", gen7_two_runs),
        ("d 极大，整数组为一段", gen8_large_d),
        ("单组大 n≈2e5，相邻在阈值内随机游走", gen9_single_large_n),
        ("大量小测试点，sum n 压力", gen10_many_groups),
    ]

    for i, (note, gen) in enumerate(generators, start=1):
        inp = gen()
        out = solve_input_text(inp)
        write_in(os.path.join(data_dir, f"{i}.in"), inp)
        write_out(os.path.join(data_dir, f"{i}.out"), out)

    # 自校验
    for i in range(1, 11):
        p_in = os.path.join(data_dir, f"{i}.in")
        p_out = os.path.join(data_dir, f"{i}.out")
        with open(p_in, "rb") as f:
            raw = f.read()
        if raw.endswith(b"\n"):
            raise SystemExit(f"fail: {i}.in should not end with newline byte")
        with open(p_out, "rb") as f:
            rawo = f.read()
        if not rawo.endswith(b"\n") or rawo.endswith(b"\n\n"):
            raise SystemExit(f"fail: {i}.out newline rule, got {rawo[-3:]!r}")
        with open(p_in, "r", encoding="utf-8") as f:
            text_in = f.read()
        recomputed = solve_input_text(text_in)
        with open(p_out, "r", encoding="utf-8") as f:
            text_out = f.read()
        if recomputed != text_out:
            raise SystemExit(f"fail: group {i} out mismatch")

    readme = os.path.join(data_dir, "README.md")
    lines = ["# P4910 测试数据说明\n", "\n", "| 编号 | 设计意图 |\n", "|---|---|\n"]
    for i, (note, _) in enumerate(generators, start=1):
        lines.append(f"| {i} | {note} |\n")
    with open(readme, "w", encoding="utf-8", newline="\n") as f:
        f.writelines(lines)

    print("generated 1..10.in/.out and README.md; self-check ok")


if __name__ == "__main__":
    main()
