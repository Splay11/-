# -*- coding: utf-8 -*-
import random
from pathlib import Path

from std import phase_contrib

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
DATA.mkdir(exist_ok=True)
rng = random.Random(5381)
MOD = 1000000007


def brute(n, v):
    ans = []
    for d in range(1, n + 1):
        s = 0
        for i in range(n):
            s += (i % d) * v[i]
        ans.append(s % MOD)
    return ans


def dump(idx, n, v, note):
    inn = str(n) + "\n" + " ".join(str(x) for x in v)
    ans = phase_contrib(n, v)
    if n <= 2000:
        b = brute(n, v)
        if b != ans:
            raise SystemExit("brute mismatch case %s" % idx)
    out = " ".join(str(x) for x in ans) + "\n"
    (DATA / ("%d.in" % idx)).write_bytes(inn.encode("utf-8"))
    (DATA / ("%d.out" % idx)).write_bytes(out.encode("utf-8"))
    print("case %d: n=%d note=%s" % (idx, n, note))


dump(1, 4, [3, 1, 4, 2], "样例1 手算")
dump(2, 1, [8], "样例2 n=1")
dump(3, 6, [2, 0, 5, 1, 0, 3], "样例3 含零")

dump(4, 1, [0], "边界 单灯亮度为 0")
dump(5, 7, [0, 0, 0, 0, 0, 0, 0], "边界 全零")
dump(6, 5, [1000000000, 0, 0, 0, 0], "hack 0 下标大值，卡 1-based")
dump(7, 12, [10**9] * 12, "hack 乘积超模数，卡未取模/int 溢出")
dump(8, 80, [rng.randint(0, 10**9) for _ in range(80)], "随机中等")

n9 = 200000
v9 = [rng.randint(0, 10**9) for _ in range(n9)]
dump(9, n9, v9, "大数据随机 n=200000")

n10 = 200000
v10 = [10**9] * n10
dump(10, n10, v10, "大数据全满值，卡 O(n^2) 与溢出")

# 生成后自校验：重算全部 .out
for idx in range(1, 11):
    raw = (DATA / ("%d.in" % idx)).read_bytes().decode("utf-8")
    if raw.endswith("\n"):
        raise SystemExit(".in trailing newline: %d" % idx)
    lines = raw.split("\n")
    n = int(lines[0])
    v = list(map(int, lines[1].split()))
    got = " ".join(str(x) for x in phase_contrib(n, v)) + "\n"
    want = (DATA / ("%d.out" % idx)).read_bytes().decode("utf-8")
    if got != want:
        raise SystemExit("out mismatch %d" % idx)
    if not want.endswith("\n") or want.endswith("\n\n"):
        raise SystemExit(".out newline rule fail %d" % idx)

print("ok")
