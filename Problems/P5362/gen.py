# -*- coding: utf-8 -*-
import random
from pathlib import Path

from std import min_swaps

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
DATA.mkdir(exist_ok=True)
rng = random.Random(5362)


def format_in(m, d):
    return f"{m}\n{d}"


def format_out(ans):
    return str(ans) + "\n"


def write_in(path, text):
    path.write_bytes(text.encode("utf-8"))


def write_out(path, text):
    path.write_bytes(text.encode("utf-8"))


def dump(idx, m, d, note):
    ans = min_swaps(d)
    write_in(DATA / f"{idx}.in", format_in(m, d))
    write_out(DATA / f"{idx}.out", format_out(ans))
    print(f"case {idx}: m={m} ans={ans} note={note}")


def rand_balanced(m):
    chars = ["0"] * m + ["1"] * m
    rng.shuffle(chars)
    return "".join(chars)


def slow(d):
    n = len(d) // 2
    p = [i for i, c in enumerate(d) if c == "0"]
    pd = p + [x + 2 * n for x in p]
    ans = 10**18
    for start in (0, 1):
        for s0 in range(n):
            for r in range(n):
                c = 0
                for i in range(n):
                    c += abs(pd[s0 + i] - (start + 2 * (r + i)))
                if c < ans:
                    ans = c
    return ans


# 1-3 样例
dump(1, 2, "1100", "样例1")
dump(2, 3, "110100", "样例2 跨首尾")
dump(3, 1, "10", "样例3 已交错")

# 4 另一种已交错
dump(4, 4, "01010101", "已是 01 交错")

# 5 全 0 随后全 1，线性公式会偏大
dump(5, 6, "000000111111", "两团，卡不绕环")

# 6 全 1 随后全 0
dump(6, 5, "1111100000", "反向两团")

# 7 中等随机，与 O(m^2) 对拍
d7 = rand_balanced(25)
assert min_swaps(d7) == slow(d7)
dump(7, 25, d7, "中等随机对拍")

# 8 交错再翻一小段
dump(8, 8, "0101010110101010", "局部打乱")

# 9 大数据两团
m9 = 200000
d9 = "0" * m9 + "1" * m9
dump(9, m9, d9, "m=2e5 两团")

# 10 大数据随机
m10 = 200000
d10 = rand_balanced(m10)
dump(10, m10, d10, "m=2e5 随机")

for i in range(1, 11):
    raw = (DATA / f"{i}.in").read_text(encoding="utf-8")
    lines = raw.split("\n")
    m = int(lines[0])
    d = lines[1]
    assert len(d) == 2 * m
    assert d.count("0") == m
    got = format_out(min_swaps(d))
    exp = (DATA / f"{i}.out").read_bytes().decode("utf-8")
    assert got == exp, i
    inn = (DATA / f"{i}.in").read_bytes()
    assert not inn.endswith(b"\n"), i
    out = (DATA / f"{i}.out").read_bytes()
    assert out.endswith(b"\n") and not out.endswith(b"\n\n"), i

print("gen ok")
