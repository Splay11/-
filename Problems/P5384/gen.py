# -*- coding: utf-8 -*-
import random
from pathlib import Path

from std import min_time

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
DATA.mkdir(exist_ok=True)
rng = random.Random(5384)


def fmt(n, roads, portals, cap, src, dst):
    lines = [str(n) + " " + str(len(roads))]
    for u, v, d in roads:
        lines.append(str(u) + " " + str(v) + " " + str(d))
    lines.append(str(len(portals)))
    for u, v in portals:
        lines.append(str(u) + " " + str(v))
    lines.append(str(cap) + " " + str(src) + " " + str(dst))
    return "\n".join(lines)


def dump(idx, n, roads, portals, cap, src, dst, note):
    ans = min_time(n, roads, portals, cap, src, dst)
    inn = fmt(n, roads, portals, cap, src, dst)
    out = str(ans) + "\n"
    (DATA / ("%d.in" % idx)).write_bytes(inn.encode("utf-8"))
    (DATA / ("%d.out" % idx)).write_bytes(out.encode("utf-8"))
    print("case %d: n=%d m=%d p=%d cap=%d ans=%d note=%s" % (
        idx, n, len(roads), len(portals), cap, ans, note))


def rand_graph(n, m, wmax):
    roads = []
    for i in range(1, n):
        p = rng.randint(0, i - 1)
        roads.append((p, i, rng.randint(0, wmax)))
    while len(roads) < m:
        u = rng.randint(0, n - 1)
        v = rng.randint(0, n - 1)
        roads.append((u, v, rng.randint(0, wmax)))
    return roads[:m]


def rand_portals(n, p):
    res = []
    for _ in range(p):
        res.append((rng.randint(0, n - 1), rng.randint(0, n - 1)))
    return res


dump(1, 5, [(0, 1, 7), (1, 2, 7), (2, 3, 7), (3, 4, 7)], [(0, 2), (2, 4)], 2, 0, 4, "样例1 不能连坐罐笼")
dump(2, 4, [(0, 1, 9)], [], 0, 2, 2, "样例2 起点等于终点")
dump(3, 3, [(0, 1, 8)], [], 2, 0, 2, "样例3 不连通")

dump(4, 4, [(0, 1, 2), (1, 2, 6), (2, 3, 1)], [(0, 3)], 0, 0, 3, "k=0 只能走巷道")
dump(5, 3, [], [(0, 1), (1, 2)], 2, 0, 2, "hack 连坐罐笼应得 -1")
dump(6, 3, [(1, 1, 5)], [(0, 1), (1, 2)], 2, 0, 2, "hack 自环巷道隔开两次罐笼")
dump(7, 1, [], [(0, 0)], 10, 0, 0, "n=1 自环罐笼但已在终点")
dump(8, 40, rand_graph(40, 80, 1000), rand_portals(40, 6), 4, 0, 39, "随机中等")

n9 = 10000
roads9 = rand_graph(n9, 200000, 10**9)
portals9 = rand_portals(n9, 10)
dump(9, n9, roads9, portals9, 10, 0, n9 - 1, "大数据 n=10000 m=200000")

n10 = 10000
roads10 = [(i, i + 1, 10**9) for i in range(n10 - 1)]
dump(10, n10, roads10, [], 0, 0, n10 - 1, "长链满权值，卡 int 溢出")

for idx in range(1, 11):
    raw = (DATA / ("%d.in" % idx)).read_bytes().decode("utf-8")
    if raw.endswith("\n"):
        raise SystemExit(".in trailing newline: %d" % idx)
    lines = raw.split("\n")
    n, m = map(int, lines[0].split())
    roads = []
    ptr = 1
    for _ in range(m):
        u, v, d = map(int, lines[ptr].split())
        roads.append((u, v, d))
        ptr += 1
    p = int(lines[ptr])
    ptr += 1
    portals = []
    for _ in range(p):
        u, v = map(int, lines[ptr].split())
        portals.append((u, v))
        ptr += 1
    cap, src, dst = map(int, lines[ptr].split())
    got = str(min_time(n, roads, portals, cap, src, dst)) + "\n"
    want = (DATA / ("%d.out" % idx)).read_bytes().decode("utf-8")
    if got != want:
        raise SystemExit("out mismatch %d" % idx)
    if not want.endswith("\n") or want.endswith("\n\n"):
        raise SystemExit(".out newline fail %d" % idx)

print("ok")
