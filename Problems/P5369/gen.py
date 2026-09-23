# -*- coding: utf-8 -*-
import random
from itertools import permutations
from pathlib import Path

from std import MOD, count_arrangements

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
DATA.mkdir(exist_ok=True)
rng = random.Random(5369)


def format_in(d, v):
    return str(len(v)) + " " + str(d) + "\n" + " ".join(str(x) for x in v)


def format_out(ans):
    return str(ans) + "\n"


def dump(idx, d, v, note):
    ans = count_arrangements(d, v)
    (DATA / f"{idx}.in").write_bytes(format_in(d, v).encode("utf-8"))
    (DATA / f"{idx}.out").write_bytes(format_out(ans).encode("utf-8"))
    print(f"case {idx}: m={len(v)} d={d} ans={ans} note={note}")


def brute(d, v):
    n = len(v)
    cnt = 0
    for p in permutations(range(n)):
        ok = True
        for i in range(n - 1):
            if v[p[i + 1]] < v[p[i]] - d:
                ok = False
                break
        if ok:
            cnt += 1
    return cnt % MOD


def check_small(d, v):
    got = count_arrangements(d, v)
    exp = brute(d, v)
    assert got == exp, (d, v, got, exp)


dump(1, 1, [1, 2, 3], "样例1")
dump(2, 1, [8, 1], "样例2 只能升")
dump(3, 10, [4, 4, 4], "样例3 全相同 3!")

check_small(10, [2, 2, 5])
dump(4, 10, [2, 2, 5], "两箱同高，箱号可区分")

# 间隔大于 d，高度必须严格不降，互异时只有 1 种
dump(5, 1, [1, 3, 5, 7], "大间隔，答案 1")

dump(6, 1, [9, 9, 9, 9], "全相同 4!")

v7 = [rng.randint(1, 8) for _ in range(7)]
d7 = rng.randint(1, 4)
check_small(d7, v7)
dump(7, d7, v7, "n=7 与暴力对拍")

v8 = [rng.randint(1, 20) for _ in range(8)]
d8 = 2
check_small(d8, v8)
dump(8, d8, v8, "n=8 卡双向 |差|<=d")

m9 = 200000
v9 = [rng.randint(1, 1000000) for _ in range(m9)]
dump(9, rng.randint(1, 1000000), v9, "m=2e5 随机")

m10 = 200000
dump(10, 1, [1] * m10, "m=2e5 全相同，答案 m!")

print("ok")
