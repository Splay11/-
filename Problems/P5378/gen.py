# -*- coding: utf-8 -*-
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from std import ans, count_str

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
DATA.mkdir(exist_ok=True)
rng = random.Random(5378)


def format_in(ms):
    return str(len(ms)) + "\n" + "\n".join(str(x) for x in ms)


def format_out(ms):
    return "".join(str(count_str(x)) + "\n" for x in ms)


def dump(idx, ms, note):
    (DATA / f"{idx}.in").write_bytes(format_in(ms).encode("utf-8"))
    (DATA / f"{idx}.out").write_bytes(format_out(ms).encode("utf-8"))
    print(f"case {idx}: q={len(ms)} note={note}")


dump(1, [1, 3, 5], "样例1")
dump(2, [6, 8], "样例2")
dump(3, [7], "样例3")
dump(4, [1, 1, 2, 3, 4], "小长度，卡 26^n 与 26^n-26")
dump(5, [9, 10, 11, 12], "刚过模数附近的中等长度")
dump(6, [13, 20, 26, 27], "hack：把三连也禁掉；或只减整串相同")
dump(7, list(range(1, 16)), "1..15 全覆盖")
dump(8, [rng.randint(1, 80) for _ in range(30)], "随机中小")

# 9-10 大数据 q=200000
ms9 = [(i % 200000) + 1 for i in range(200000)]
dump(9, ms9, "q=200000 扫遍所有长度")

ms10 = [200000] * 50000 + [1] * 50000 + [4] * 50000
ms10 += [rng.randint(1, 200000) for _ in range(50000)]
dump(10, ms10, "q=200000 极值+随机")

ok = True
for i in range(1, 11):
    raw = (DATA / f"{i}.in").read_bytes().decode("utf-8")
    parts = raw.split("\n")
    q = int(parts[0])
    ms = [int(parts[j]) for j in range(1, q + 1)]
    if format_out(ms) != (DATA / f"{i}.out").read_text(encoding="utf-8"):
        print("MISMATCH", i)
        ok = False
if not ok:
    raise SystemExit(1)
print("ok")
