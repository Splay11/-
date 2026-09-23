# -*- coding: utf-8 -*-
import random
from pathlib import Path

from std import is_prime, smallest_odd_prime_factor

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
DATA.mkdir(exist_ok=True)
rng = random.Random(5379)


def next_prime(x):
    if x < 2:
        x = 2
    if x % 2 == 0:
        x += 1
    while not is_prime(x):
        x += 2
    return x


def dump(idx, xs, note):
    q = len(xs)
    inn = str(q) + "\n" + "\n".join(str(x) for x in xs)
    ans = [smallest_odd_prime_factor(x) for x in xs]
    out = "\n".join(str(a) for a in ans) + "\n"
    (DATA / ("%d.in" % idx)).write_bytes(inn.encode("utf-8"))
    (DATA / ("%d.out" % idx)).write_bytes(out.encode("utf-8"))
    print("case %d: q=%d note=%s" % (idx, q, note))


dump(1, [21, 8, 25, 77], "样例1")
dump(2, [16], "样例2 2 的幂")
dump(3, [9, 14], "样例3")

dump(4, [2, 4, 8, 32, 1024], "若干 2 的幂，全 -1")
dump(5, [3, 5, 7, 11, 97], "小奇素数自身")
dump(6, [6, 10, 15, 27, 49, 121], "含 2 或平方")
dump(7, [100000000000000], "hack 上限 10^14 = 2^14 * 5^14")

p_big = next_prime(10**14 - 100)
dump(8, [p_big, p_big * 2, 9 * (10**12)], "大素数 / 偶数倍 / 3 开头的大数")

xs9 = [rng.randint(2, 10**9) for _ in range(100)]
dump(9, xs9, "q=100 中等随机")

xs10 = []
for i in range(50):
    xs10.append(1 << rng.randint(1, 40))
for i in range(50):
    xs10.append(next_prime(10**13 + rng.randint(0, 10**6) * 2 + 1))
dump(10, xs10, "q=100 一半 2 的幂一半大素数")

for idx in range(1, 11):
    raw = (DATA / ("%d.in" % idx)).read_bytes().decode("utf-8")
    if raw.endswith("\n"):
        raise SystemExit(".in trailing newline %d" % idx)
    lines = raw.split("\n")
    q = int(lines[0])
    xs = [int(lines[i]) for i in range(1, q + 1)]
    got = "\n".join(str(smallest_odd_prime_factor(x)) for x in xs) + "\n"
    want = (DATA / ("%d.out" % idx)).read_bytes().decode("utf-8")
    if got != want:
        raise SystemExit("out mismatch %d" % idx)
    if not want.endswith("\n") or want.endswith("\n\n"):
        raise SystemExit("out newline fail %d" % idx)

print("ok")
