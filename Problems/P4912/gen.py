# -*- coding: utf-8 -*-
"""
P4912 测试数据生成器：最多一次形变后排序的最小间隔最大化。
固定种子；自校验与标程逻辑一致。
.in 最后一行末尾无换行；.out 末尾有且仅有一个换行。
"""
import os
import random
import subprocess
import sys

RNG = random.Random(491200)

SUM_N_MAX = 400000


def feasible(n, m, s, g):
    if g <= 0:
        return True
    gap = [s[i + 1] - s[i] for i in range(n - 1)]
    tot_bad = sum(1 for x in gap if x < g)
    pref_bad = [0] * (n - 1)
    for i in range(n - 1):
        pref_bad[i] = (pref_bad[i - 1] if i else 0) + (1 if gap[i] < g else 0)
    pref_max = gap[:]
    for i in range(1, n - 1):
        pref_max[i] = max(pref_max[i - 1], pref_max[i])
    suf_max = gap[:]
    for i in range(n - 3, -1, -1):
        suf_max[i] = max(suf_max[i], suf_max[i + 1])
    pref_large = [-1] * (n - 1)
    for i in range(n - 1):
        if gap[i] < g:
            pref_large[i] = max((pref_large[i - 1] if i else -1), i)
        else:
            pref_large[i] = pref_large[i - 1] if i else -1
    inf_idx = n + 5
    suf_small = [inf_idx] * (n - 1)
    for i in range(n - 2, -1, -1):
        if gap[i] < g:
            suf_small[i] = min((suf_small[i + 1] if i + 1 < n - 1 else inf_idx), i)
        else:
            suf_small[i] = suf_small[i + 1] if i + 1 < n - 1 else inf_idx

    def bad_left(k):
        return pref_bad[k - 2] if k >= 2 else 0

    def bad_right(k):
        return 0 if k >= n - 1 else tot_bad - pref_bad[k]

    def bad_bridge(k):
        if 0 < k < n - 1 and s[k + 1] - s[k - 1] < g:
            return 1
        return 0

    for k in range(n):
        bl = bad_left(k)
        br = bad_right(k)
        bb = bad_bridge(k)
        tb = bl + br + bb
        if tb > 1:
            continue
        first_t = s[0] if k != 0 else s[1]
        last_t = s[n - 1] if k != n - 1 else s[n - 2]
        if tb == 0:
            if first_t >= g + 1:
                return True
            if last_t <= m - g:
                return True
            mx = -1
            if k >= 2:
                mx = max(mx, pref_max[k - 2])
            if k + 1 <= n - 2:
                mx = max(mx, suf_max[k + 1])
            if 0 < k < n - 1:
                mx = max(mx, s[k + 1] - s[k - 1])
            if mx >= 2 * g:
                return True
            continue
        u = v = None
        if bb == 1 and bl == 0 and br == 0:
            u, v = s[k - 1], s[k + 1]
        elif bl == 1 and br == 0 and bb == 0:
            idx = pref_large[k - 2]
            u, v = s[idx], s[idx + 1]
        elif br == 1 and bl == 0 and bb == 0:
            idx = suf_small[k + 1]
            if idx > n - 2:
                continue
            u, v = s[idx], s[idx + 1]
        else:
            continue
        if v - u < 2 * g:
            continue
        L = max(1, u + g)
        R = min(m, v - g)
        if L <= R:
            return True
    return False


def solve_one(n, m, a):
    s = sorted(a)
    lo, hi = 0, m
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if feasible(n, m, s, mid):
            lo = mid
        else:
            hi = mid - 1
    return lo


def solve_input_text(inp: str):
    lines = inp.strip().splitlines()
    idx = 0
    t = int(lines[idx])
    idx += 1
    outs = []
    for _ in range(t):
        n, m = map(int, lines[idx].split())
        idx += 1
        a = list(map(int, lines[idx].split()))
        idx += 1
        outs.append(str(solve_one(n, m, a)))
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
    return """3
3 10
1 2 8
4 7
1 1 1 7
2 100
30 70"""


def gen2_n2_max_gap():
    # 基础：n=2 时答案为 max(m-a[1], a[0]-1) 形态
    return """1
2 1000000000
1 1000000000"""


def gen3_all_equal():
    # 边界：全相等，一次形变也难抬升最小间隔（大量重复 0 间隔）
    n = 5000
    m = 10**9
    a = [1] * n
    return "\n".join(["1", f"{n} {m}", " ".join(map(str, a))])


def gen4_hack_greedy_no_change():
    # hack：不做形变时最小间隔很小，但改一个内点可显著抬高答案
    return """1
5 20
1 2 3 4 19"""


def gen5_small_random():
    parts = []
    cases = []
    total_n = 0
    while len(cases) < 50 and total_n + 8 <= SUM_N_MAX:
        n = RNG.randint(2, 8)
        if total_n + n > SUM_N_MAX:
            break
        m = RNG.randint(2, 500)
        a = [RNG.randint(1, m) for _ in range(n)]
        cases.append((n, m, a))
        total_n += n
    parts.append(str(len(cases)))
    for n, m, a in cases:
        parts.append(f"{n} {m}")
        parts.append(" ".join(map(str, a)))
    return "\n".join(parts)


def gen6_two_clusters():
    # 构造：两簇很近，中间大空洞；检测桥接间隔与删点
    return """1
6 1000
1 2 3 500 501 502"""


def gen7_almost_arithmetic():
    # 构造：近似等差，答案与 floor((m-1)/(n-1)) 相关
    n = 2000
    m = 10**9
    step = 500000
    start = RNG.randint(1, 100000)
    a = [start + i * step for i in range(n)]
    return "\n".join(["1", f"{n} {m}", " ".join(map(str, a))])


def gen8_many_duplicates():
    # 构造：大量重复值 + 一个离群点
    n = 8000
    m = 10**9
    a = [5] * (n - 1) + [10**8]
    RNG.shuffle(a)
    return "\n".join(["1", f"{n} {m}", " ".join(map(str, a))])


def gen9_single_large_n():
    # 压力：单组 n 逼近 2e5，m 大，随机
    n = 200000
    m = 10**9
    a = [RNG.randint(1, m) for _ in range(n)]
    return "\n".join(["1", f"{n} {m}", " ".join(map(str, a))])


def gen10_many_groups():
    # 压力：多组小 n，sum n 逼近上限
    cases = []
    total = 0
    while total < SUM_N_MAX:
        rest = SUM_N_MAX - total
        if rest < 2:
            break
        hi = min(9, rest)
        if hi < 2:
            break
        n = RNG.randint(2, hi)
        m = RNG.randint(2, 10**9)
        a = [RNG.randint(1, m) for _ in range(n)]
        cases.append((n, m, a))
        total += n
    parts = [str(len(cases))]
    for n, m, a in cases:
        parts.append(f"{n} {m}")
        parts.append(" ".join(map(str, a)))
    return "\n".join(parts)


def main():
    root = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(root, "data")
    os.makedirs(data_dir, exist_ok=True)

    generators = [
        ("题面样例；格式与多组行为", gen1_sample),
        ("基础：n=2 且 m 极大", gen2_n2_max_gap),
        ("边界：全 1 长序列", gen3_all_equal),
        ("hack：必须形变才能抬高最小间隔", gen4_hack_greedy_no_change),
        ("多组随机小 n，便于本地暴力对拍", gen5_small_random),
        ("构造：两簇 + 大间隔", gen6_two_clusters),
        ("构造：大步长近似等差", gen7_almost_arithmetic),
        ("构造：大量重复 + 离群", gen8_many_duplicates),
        ("压力：单组 n=2e5", gen9_single_large_n),
        ("压力：多组 sum n≈4e5", gen10_many_groups),
    ]

    for i, (note, gen) in enumerate(generators, start=1):
        inp = gen()
        out = solve_input_text(inp)
        write_in(os.path.join(data_dir, f"{i}.in"), inp)
        write_out(os.path.join(data_dir, f"{i}.out"), out)

    for i in range(1, 11):
        p_in = os.path.join(data_dir, f"{i}.in")
        p_out = os.path.join(data_dir, f"{i}.out")
        with open(p_in, "rb") as f:
            raw = f.read()
        if raw.endswith(b"\n"):
            raise SystemExit(f"fail: {i}.in should not end with newline")
        with open(p_out, "rb") as f:
            rout = f.read()
        if not rout.endswith(b"\n") or rout.endswith(b"\n\n"):
            raise SystemExit(f"fail: {i}.out newline rule")
        got = solve_input_text(raw.decode("utf-8"))
        with open(p_out, "r", encoding="utf-8") as f:
            disk = f.read()
        if got != disk:
            raise SystemExit(f"fail: mismatch case {i}")

    cpp = os.path.join(root, "std.cpp")
    if os.path.isfile(cpp):
        if sys.platform == "win32":
            exe = os.path.join(root, "_std_check.exe")
            r = subprocess.run(
                ["g++", "-std=c++17", "-O2", cpp, "-o", exe],
                cwd=root,
                capture_output=True,
                text=True,
            )
            if r.returncode != 0:
                print(r.stderr, file=sys.stderr)
                raise SystemExit("g++ failed")
            for i in range(1, 11):
                pi = os.path.join(data_dir, f"{i}.in")
                po = os.path.join(data_dir, f"{i}.out")
                r2 = subprocess.run(
                    [exe],
                    input=open(pi, "rb").read(),
                    capture_output=True,
                    cwd=root,
                )
                if r2.returncode != 0:
                    raise SystemExit(f"std run fail {i}")
                got_cpp = r2.stdout.decode("utf-8").replace("\r\n", "\n")
                disk = open(po, "r", encoding="utf-8").read().replace("\r\n", "\n")
                if got_cpp != disk:
                    raise SystemExit(f"cpp mismatch {i}")

    print("gen ok: 10 pairs, self-check passed")


if __name__ == "__main__":
    main()
