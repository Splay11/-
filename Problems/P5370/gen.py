# -*- coding: utf-8 -*-
import random
from itertools import combinations
from pathlib import Path

from std import min_range

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
DATA.mkdir(exist_ok=True)
rng = random.Random(5370)


def format_in(v):
    return str(len(v)) + "\n" + " ".join(str(x) for x in v)


def format_out(ans):
    return str(ans) + "\n"


def dump(idx, v, note):
    ans = min_range(v)
    (DATA / f"{idx}.in").write_bytes(format_in(v).encode("utf-8"))
    (DATA / f"{idx}.out").write_bytes(format_out(ans).encode("utf-8"))
    print(f"case {idx}: m={len(v)} ans={ans} note={note}")


def brute(v):
    n = len(v)
    s = [0] * (n + 1)
    for i in range(n):
        s[i + 1] = s[i] + v[i]
    ans = 10 ** 18
    for i, j, k in combinations(range(1, n), 3):
        a = s[i]
        b = s[j] - s[i]
        c = s[k] - s[j]
        d = s[n] - s[k]
        mx = max(a, b, c, d)
        mn = min(a, b, c, d)
        if mx - mn < ans:
            ans = mx - mn
    return ans


def check_small(v):
    got = min_range(v)
    exp = brute(v)
    assert got == exp, (v, got, exp)


dump(1, [4, 5, 1, 2, 8], "样例1")
dump(2, [1, 1, 1, 1], "样例2 四节相同")
dump(3, [9, 1, 1, 1, 1], "样例3 左端特大")
dump(4, [3, 2, 4, 1, 2], "原题样例，答案 2")

v5 = [1, 2, 3, 3, 2, 1]
check_small(v5)
dump(5, v5, "对称，答案 0")

dump(6, [10 ** 9, 10 ** 9, 10 ** 9, 10 ** 9], "四节满值，卡 32 位")

v7 = [rng.randint(1, 15) for _ in range(10)]
check_small(v7)
dump(7, v7, "n=10 与暴力对拍")

v8 = [rng.randint(1, 30) for _ in range(12)]
check_small(v8)
dump(8, v8, "n=12 卡按长度均分")

v9 = [rng.randint(1, 10 ** 9) for _ in range(100000)]
dump(9, v9, "m=1e5 随机")

v10 = [1] * 99999 + [10 ** 9]
dump(10, v10, "m=1e5 右端特大")

print("ok")
