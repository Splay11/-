# -*- coding: utf-8 -*-
import random
from pathlib import Path

from std import count_pairs

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
DATA.mkdir(exist_ok=True)
rng = random.Random(5383)


def brute(n, t, w):
    ans = 0
    for i in range(n):
        for j in range(i + 1, n):
            if (w[i] + w[j]) % t == 0:
                ans += 1
    return ans


def dump(idx, n, t, w, note):
    inn = str(n) + " " + str(t) + "\n" + " ".join(str(x) for x in w)
    ans = count_pairs(n, t, w)
    if n <= 2000:
        b = brute(n, t, w)
        if b != ans:
            raise SystemExit("brute mismatch case %s" % idx)
    out = str(ans) + "\n"
    (DATA / ("%d.in" % idx)).write_bytes(inn.encode("utf-8"))
    (DATA / ("%d.out" % idx)).write_bytes(out.encode("utf-8"))
    print("case %d: n=%d t=%d ans=%d note=%s" % (idx, n, t, ans, note))


dump(1, 5, 4, [1, 3, 5, 7, 8], "样例1 互补余数")
dump(2, 3, 7, [0, 7, 14], "样例2 全是余数 0")
dump(3, 6, 4, [2, 2, 2, 6, 10, 14], "样例3 全是 t/2")

dump(4, 2, 1, [0, 0], "边界 n=2 t=1")
dump(5, 8, 5, [0] * 8, "全零，C(8,2)")
dump(6, 9, 6, [3] * 9, "hack 只含 t/2，卡漏偶数自配")
dump(7, 10, 5, [1, 1, 1, 1, 4, 4, 4, 2, 3, 0], "hack 卡 r 与 t-r 算重")
dump(8, 200, 97, [rng.randint(0, 10**9) for _ in range(200)], "随机中等，可暴力对拍")

n9 = 100000
t9 = 100000
v9 = [rng.randint(0, 10**9) for _ in range(n9)]
dump(9, n9, t9, v9, "大数据随机 n=t=100000")

n10 = 100000
t10 = 1
v10 = [10**9] * n10
dump(10, n10, t10, v10, "t=1 全配对，答案 C(n,2) 卡 int 溢出")

for idx in range(1, 11):
    raw = (DATA / ("%d.in" % idx)).read_bytes().decode("utf-8")
    if raw.endswith("\n"):
        raise SystemExit(".in trailing newline: %d" % idx)
    lines = raw.split("\n")
    n, t = map(int, lines[0].split())
    w = list(map(int, lines[1].split()))
    got = str(count_pairs(n, t, w)) + "\n"
    want = (DATA / ("%d.out" % idx)).read_bytes().decode("utf-8")
    if got != want:
        raise SystemExit("out mismatch %d" % idx)
    if not want.endswith("\n") or want.endswith("\n\n"):
        raise SystemExit(".out newline rule fail %d" % idx)

print("ok")
