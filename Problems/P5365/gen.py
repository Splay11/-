# -*- coding: utf-8 -*-
import random
from pathlib import Path

from std import max_boats

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
DATA.mkdir(exist_ok=True)
rng = random.Random(5365)


def format_in(groups):
    lines = [str(len(groups))]
    for a, b in groups:
        lines.append(str(len(a)))
        lines.append(" ".join(str(x) for x in a))
        lines.append(" ".join(str(x) for x in b))
    return "\n".join(lines)


def format_out(ans):
    return "\n".join(str(x) for x in ans) + "\n"


def dump(idx, groups, note):
    ans = [max_boats(a, b) for a, b in groups]
    (DATA / f"{idx}.in").write_bytes(format_in(groups).encode("utf-8"))
    (DATA / f"{idx}.out").write_bytes(format_out(ans).encode("utf-8"))
    print(f"case {idx}: q={len(groups)} m0={len(groups[0][0])} ans0={ans[0]} note={note}")


def brute(a, b):
    n = len(a)
    best = 0
    for mask in range(1 << n):
        idx = [i for i in range(n) if mask >> i & 1]
        ok = True
        for i in range(len(idx)):
            for j in range(i + 1, len(idx)):
                p1, q1 = a[idx[i]], b[idx[i]]
                p2, q2 = a[idx[j]], b[idx[j]]
                if p1 > p2:
                    p1, q1, p2, q2 = p2, q2, p1, q1
                if p1 == p2 or q1 >= q2:
                    ok = False
                    break
            if not ok:
                break
        if ok:
            best = max(best, len(idx))
    return best


dump(1, [([2, 5, 8, 12], [4, 15, 7, 14])], "样例1")
dump(2, [([4, 4, 9], [8, 6, 12])], "样例2 同起点")
dump(3, [([10], [10])], "样例3 单艇")
dump(4, [([7, 7, 7, 7], [1, 9, 3, 5])], "全同起点，答案 1")
dump(5, [([1, 2, 3, 4, 5], [2, 4, 6, 8, 10])], "两端都递增")
dump(6, [([1, 2, 3, 4, 5], [10, 8, 6, 4, 2])], "终点递减，答案 1")

a7 = [rng.randint(1, 20) for _ in range(10)]
b7 = [rng.randint(1, 20) for _ in range(10)]
assert max_boats(a7, b7) == brute(a7, b7)
dump(7, [(a7, b7)], "n=10 与暴力对拍")

groups8 = []
for _ in range(5):
    n = rng.randint(8, 12)
    groups8.append(([rng.randint(1, 30) for _ in range(n)], [rng.randint(1, 30) for _ in range(n)]))
    assert max_boats(*groups8[-1]) == brute(*groups8[-1])
dump(8, groups8, "多份小单对拍")

m9 = 200000
a9 = list(range(1, m9 + 1))
b9 = list(range(1, m9 + 1))
dump(9, [(a9, b9)], "m=2e5 递增")

m10 = 200000
a10 = list(range(1, m10 + 1))
b10 = list(range(m10, 0, -1))
dump(10, [(a10, b10)], "m=2e5 终点递减")

for i in range(1, 11):
    raw = (DATA / f"{i}.in").read_text(encoding="utf-8")
    lines = raw.split("\n")
    q = int(lines[0])
    ptr = 1
    got_list = []
    for _ in range(q):
        m = int(lines[ptr]); ptr += 1
        a = list(map(int, lines[ptr].split())); ptr += 1
        b = list(map(int, lines[ptr].split())); ptr += 1
        got_list.append(max_boats(a, b))
    got = format_out(got_list)
    exp = (DATA / f"{i}.out").read_bytes().decode("utf-8")
    assert got == exp, i
    inn = (DATA / f"{i}.in").read_bytes()
    assert not inn.endswith(b"\n"), i
    out = (DATA / f"{i}.out").read_bytes()
    assert out.endswith(b"\n") and not out.endswith(b"\n\n"), i

print("gen ok")
