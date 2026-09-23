# -*- coding: utf-8 -*-
import random
from pathlib import Path

from std import max_pairs

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
DATA.mkdir(exist_ok=True)
rng = random.Random(5364)


def format_in(m, d, v):
    return f"{m} {d}\n" + " ".join(str(x) for x in v)


def format_out(pairs):
    lines = [str(len(pairs))]
    for x, y in pairs:
        lines.append(f"{x} {y}")
    return "\n".join(lines) + "\n"


def dump(idx, d, v, note):
    m = len(v)
    pairs = max_pairs(d, v)
    (DATA / f"{idx}.in").write_bytes(format_in(m, d, v).encode("utf-8"))
    (DATA / f"{idx}.out").write_bytes(format_out(pairs).encode("utf-8"))
    print(f"case {idx}: m={m} d={d} p={len(pairs)} note={note}")


dump(1, 4, [1, 2, 3, 5, 7, 8], "样例1")
dump(2, 2, [1, 3, 5, 7], "样例2 全奇数")
dump(3, 1, [3, 5], "样例3 两奇数")
dump(4, 6, [2], "单件")
dump(5, 3, [2, 4], "k 奇、两偶数，不能配")
dump(6, 8, [2, 4, 6, 8], "全偶数可互配")
dump(7, 1, [1] * 40 + [2] * 15, "中等混合")
dump(8, 2, [rng.randint(1, 100000) for _ in range(50)], "小随机")
dump(9, 99999, [rng.randint(1, 100000) for _ in range(100000)], "m=1e5 随机")
dump(10, 2, [1] * 100000, "m=1e5 全奇数 k 偶，零对")

for i in range(1, 11):
    raw = (DATA / f"{i}.in").read_text(encoding="utf-8")
    lines = raw.split("\n")
    m, d = map(int, lines[0].split())
    v = list(map(int, lines[1].split()))
    got = format_out(max_pairs(d, v))
    exp = (DATA / f"{i}.out").read_bytes().decode("utf-8")
    assert got == exp, i
    inn = (DATA / f"{i}.in").read_bytes()
    assert not inn.endswith(b"\n"), i
    out = (DATA / f"{i}.out").read_bytes()
    assert out.endswith(b"\n") and not out.endswith(b"\n\n"), i

print("gen ok")
