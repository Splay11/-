# -*- coding: utf-8 -*-
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from std import max_pairs

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
DATA.mkdir(exist_ok=True)
rng = random.Random(5387)


def format_in(m, t, v):
    return str(m) + " " + str(t) + "\n" + " ".join(str(x) for x in v)


def format_out(t, v):
    pairs = max_pairs(t, v)
    lines = [str(len(pairs))]
    for x, y in pairs:
        lines.append(str(x) + " " + str(y))
    return "\n".join(lines) + "\n"


def dump(idx, t, v, note):
    m = len(v)
    (DATA / f"{idx}.in").write_bytes(format_in(m, t, v).encode("utf-8"))
    (DATA / f"{idx}.out").write_bytes(format_out(t, v).encode("utf-8"))
    print(f"case {idx}: m={m} t={t} c={len(max_pairs(t, v))} note={note}")


dump(1, 2, [7, 8, 9, 1, 2, 3], "样例1")
dump(2, 3, [5], "样例2 单件")
dump(3, 4, [2, 4, 6, 8], "样例3 全偶类")
dump(4, 2, [1, 3], "两奇类不能互配")
dump(5, 1, [1, 3, 5, 7, 9], "全偶类奇数个，余 1")
dump(6, 3, [2, 2, 2, 2], "t 奇且全偶数，全是奇类，0 档")
dump(7, 5, [1] * 10 + [2] * 3, "奇类多于偶类")
dump(8, rng.randint(1, 20), [rng.randint(1, 20) for _ in range(40)], "随机小")

n9 = 1000000
dump(9, 2, [1] * n9, "n=1e6 全奇类 t 偶，0 档")
dump(10, 1, [rng.randint(1, 1000000) for _ in range(n9)], "n=1e6 随机")

ok = True
for i in range(1, 11):
    raw = (DATA / f"{i}.in").read_bytes().decode("utf-8")
    head, body = raw.split("\n", 1)
    mm, tt = map(int, head.split())
    vv = list(map(int, body.split()))
    if len(vv) != mm:
        print("LEN", i)
        ok = False
    got = format_out(tt, vv)
    exp = (DATA / f"{i}.out").read_bytes().decode("utf-8")
    if got != exp:
        print("MISMATCH", i)
        ok = False
if not ok:
    raise SystemExit(1)
print("ok")
