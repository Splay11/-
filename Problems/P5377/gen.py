# -*- coding: utf-8 -*-
import random
from pathlib import Path

from std import max_accept

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
DATA.mkdir(exist_ok=True)
rng = random.Random(5377)


def dump(idx, n, b, v, note):
    inn = str(n) + " " + str(b) + "\n" + " ".join(str(x) for x in v)
    ans = max_accept(n, b, v)
    (DATA / ("%d.in" % idx)).write_bytes(inn.encode("utf-8"))
    (DATA / ("%d.out" % idx)).write_bytes((str(ans) + "\n").encode("utf-8"))
    print("case %d: n=%d b=%d ans=%d note=%s" % (idx, n, b, ans, note))


dump(1, 4, 20, [3, 1, 4, 2], "样例1")
dump(2, 1, 5, [5], "样例2 n=1 恰好")
dump(3, 3, 9, [4, 1, 1], "样例3 前缀不可行")

dump(4, 2, 1, [5, 5], "谁都批不了，答案 0")
dump(5, 3, 100, [1, 1, 1], "全都能批")
dump(6, 3, 9, [4, 1, 1], "hack 按天序贪心拿第一个会得到 0")
dump(7, 5, 20, [3, 10, 10, 6, 6], "hack 按日耗排序会先拿长驻低日耗")
dump(8, 20, 500, [rng.randint(1, 100) for _ in range(20)], "随机中等")

v9 = [rng.randint(1, 10000) for _ in range(100)]
dump(9, 100, 1000000, v9, "n=100 随机满范围")

v10 = [10000] * 100
dump(10, 100, 1000000, v10, "n=100 日耗拉满")

for idx in range(1, 11):
    raw = (DATA / ("%d.in" % idx)).read_bytes().decode("utf-8")
    if raw.endswith("\n"):
        raise SystemExit(".in trailing newline %d" % idx)
    lines = raw.split("\n")
    n, b = map(int, lines[0].split())
    v = list(map(int, lines[1].split()))
    got = str(max_accept(n, b, v)) + "\n"
    want = (DATA / ("%d.out" % idx)).read_bytes().decode("utf-8")
    if got != want:
        raise SystemExit("out mismatch %d" % idx)
    if not want.endswith("\n") or want.endswith("\n\n"):
        raise SystemExit("out newline fail %d" % idx)

print("ok")
