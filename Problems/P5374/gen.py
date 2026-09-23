# -*- coding: utf-8 -*-
import random
from pathlib import Path

from std import can_reach

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
DATA.mkdir(exist_ok=True)
rng = random.Random(5374)


def format_in(n, s, t, a):
    return str(n) + " " + str(s) + " " + str(t) + "\n" + " ".join(str(x) for x in a)


def format_out(ok):
    return ("Yes" if ok else "No") + "\n"


def dump(idx, n, s, t, a, note):
    ok = can_reach(n, s, t, a)
    (DATA / f"{idx}.in").write_bytes(format_in(n, s, t, a).encode("utf-8"))
    (DATA / f"{idx}.out").write_bytes(format_out(ok).encode("utf-8"))
    print(f"case {idx}: n={n} s={s} t={t} ans={'Yes' if ok else 'No'} note={note}")


dump(1, 3, 3, 2, [1, 1, 1], "样例1 Yes")
dump(2, 2, 5, 3, [3, 2], "样例2 两货位奇数浪费")
dump(3, 3, 1, 2, [1, 0, 0], "样例3 已到位走一来回")

dump(4, 1, 10, 0, [10], "单货位 t=0")
dump(5, 1, 10, 1, [10], "单货位无法搬运")
dump(6, 3, 1, 1, [1, 0, 0], "已到位无法只多 1 步")
dump(7, 3, 0, 2, [0, 0, 0], "没货却要搬")
dump(8, 4, 6, 4, [2, 2, 1, 1], "最少次数刚好")

n9 = 100000
s9 = 1000000000
a9 = [0] * n9
# 把 s9 件拆到各货位，1 号留一部分
a9[0] = 1
remain = s9 - 1
a9[1] = remain
dump(9, n9, s9, remain, a9, "n=1e5 最少次数")

n10 = 100000
s10 = 0
a10 = [0] * n10
dump(10, n10, s10, 10 ** 18, a10, "n=1e5 空库 t 极大")

print("ok")
