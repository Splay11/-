# -*- coding: utf-8 -*-
import random
from pathlib import Path

from std import MOD, SegTree, encode

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
DATA.mkdir(exist_ok=True)
rng = random.Random(5375)


def brute_query(a, l, r):
    val = 0
    for i in range(r, l - 1, -1):
        fv, fl = encode(a[i])
        val = (val * pow(3, fl, MOD) + fv) % MOD
    return val


def run_ops(a, ops):
    st = SegTree(a[:])
    b = a[:]
    out = []
    for op in ops:
        if op[0] == 1:
            l, r = op[1] - 1, op[2] - 1
            got = st.query(l, r)
            if len(a) <= 12:
                exp = brute_query(b, l, r)
                assert got == exp, (b, op, got, exp)
            out.append(got)
        else:
            idx, x = op[1] - 1, op[2]
            b[idx] = x
            st.update(idx, x)
    return out


def format_in(a, ops):
    lines = [str(len(a)) + " " + str(len(ops)), " ".join(str(x) for x in a)]
    for op in ops:
        lines.append(" ".join(str(x) for x in op))
    return "\n".join(lines)


def format_out(ans):
    if not ans:
        return "0\n"
    return "\n".join(str(x) for x in ans) + "\n"


def dump(idx, a, ops, note):
    ans = run_ops(a, ops)
    raw_in = format_in(a, ops)
    (DATA / f"{idx}.in").write_bytes(raw_in.encode("utf-8"))
    (DATA / f"{idx}.out").write_bytes(format_out(ans).encode("utf-8"))
    print(f"case {idx}: m={len(a)} q={len(ops)} nout={len(ans)} note={note}")


dump(1, [1, 5, 0, 8], [[1, 1, 4], [1, 2, 4], [1, 1, 1]], "样例1")
dump(2, [0], [[1, 1, 1], [2, 1, 3], [1, 1, 1]], "样例2 零与改写")
dump(3, [2, 3, 7], [[1, 1, 3], [1, 2, 2]], "样例3 整段 102")

a4 = [0, 0, 0, 0]
dump(4, a4, [[1, 1, 4], [2, 2, 1], [1, 1, 2]], "全 0")

a5 = [1, 2, 3, 4, 5]
ops5 = [[1, 1, 5], [1, 3, 3], [2, 1, 100], [1, 1, 5]]
dump(5, a5, ops5, "小数组改左端")

a6 = [10 ** 9]
dump(6, a6, [[1, 1, 1]], "单点满值")

a7 = [rng.randint(0, 50) for _ in range(8)]
ops7 = []
for _ in range(15):
    if rng.random() < 0.6:
        l = rng.randint(1, 8)
        r = rng.randint(l, 8)
        ops7.append([1, l, r])
    else:
        ops7.append([2, rng.randint(1, 8), rng.randint(0, 50)])
dump(7, a7, ops7, "n=8 与暴力对拍")

a8 = [rng.randint(0, 200) for _ in range(10)]
ops8 = []
for _ in range(20):
    l = rng.randint(1, 10)
    r = rng.randint(l, 10)
    ops8.append([1, l, r])
dump(8, a8, ops8, "只询问，卡正向拼接")

m9 = 100000
a9 = [rng.randint(0, 10 ** 9) for _ in range(m9)]
ops9 = []
for i in range(m9):
    if i % 2 == 0:
        l = rng.randint(1, m9)
        r = rng.randint(l, m9)
        ops9.append([1, l, r])
    else:
        ops9.append([2, rng.randint(1, m9), rng.randint(0, 10 ** 9)])
dump(9, a9, ops9, "m=q=1e5 随机")

m10 = 100000
a10 = [0] * m10
ops10 = [[1, 1, m10], [2, 1, 10 ** 9], [1, 1, m10], [1, m10, m10]]
# 再补满操作数
for i in range(m10 - 4):
    ops10.append([1, 1, min(i + 1, m10)])
dump(10, a10, ops10, "m=1e5 全 0 再改左端，卡前导零")

print("ok")
