# -*- coding: utf-8 -*-
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from std import min_turns

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
DATA.mkdir(exist_ok=True)
rng = random.Random(5382)


def format_in(cases):
    lines = [str(len(cases))]
    for w in cases:
        lines.append(str(len(w)))
        lines.append(" ".join(str(x) for x in w))
    return "\n".join(lines)


def format_out(cases):
    return "".join(str(min_turns(w)) + "\n" for w in cases)


def dump(idx, cases, note):
    (DATA / f"{idx}.in").write_bytes(format_in(cases).encode("utf-8"))
    (DATA / f"{idx}.out").write_bytes(format_out(cases).encode("utf-8"))
    anss = [min_turns(w) for w in cases]
    print(f"case {idx}: q={len(cases)} ans={anss} note={note}")


def increasing(n):
    return list(range(n))


def all_zero(n):
    return [0] * n


def reverse_need(n):
    # 0 在最右，从左扫到头只能揭一扇，然后向左链式揭完
    return list(range(n - 1, -1, -1))


def zigzag_102(n):
    # 形如 1 0 2 或加长：中间放 0，左边放奇数需求，右边放偶数需求
    a = [0] * n
    if n == 1:
        return [0]
    mid = n // 2
    a[mid] = 0
    left = list(range(mid - 1, -1, -1))
    right = list(range(mid + 1, n))
    k = 1
    li = 0
    ri = 0
    turn = 0
    while k < n:
        if turn == 0 and li < len(left):
            a[left[li]] = k
            li += 1
        elif ri < len(right):
            a[right[ri]] = k
            ri += 1
        elif li < len(left):
            a[left[li]] = k
            li += 1
        k += 1
        turn ^= 1
    return a


def random_ok(n, rnd):
    # 保证有 0，阈值落在 [0, n-1]，多数可解
    a = [rnd.randint(0, max(0, n - 1)) for _ in range(n)]
    a[rnd.randrange(n)] = 0
    return a


def random_any(n, rnd):
    return [rnd.randint(0, n + 3) for _ in range(n)]


# 1-3 与改写样例一致
dump(1, [[0, 1, 2], [1, 0], [4]], "样例1")
dump(2, [[1, 0, 2]], "样例2 换向 2 次")
dump(3, [[0, 3, 1, 2]], "样例3 换向 1 次")

dump(
    4,
    [
        [0],
        [1],
        [0, 0, 0],
        [2, 2],
    ],
    "边界：单门 0/失败、全 0、阈值过大",
)
dump(
    5,
    [
        increasing(6),
        reverse_need(6),
        zigzag_102(5),
        [0, 2, 2],
    ],
    "递增 0 次 / 递减 1 次 / 之字 / 死锁",
)
dump(
    6,
    [
        [5, 0, 1, 2, 3, 4],
        [1, 1, 1, 0],
        [0, 9, 1],
        [3, 1, 0, 2, 4],
    ],
    "hack：0 在中间或右侧；阈值 >= m",
)
dump(7, [zigzag_102(k) for k in range(1, 8)], "短之字，卡提前结束或漏掉头")
dump(
    8,
    [random_ok(rng.randint(1, 20), rng) for _ in range(8)]
    + [random_any(rng.randint(1, 15), rng) for _ in range(2)],
    "随机小数据，含可能 -1",
)

# 9-10 大数据：q=10, m=500
big9 = [increasing(500)]
big9 += [all_zero(500)]
big9 += [reverse_need(500)]
big9 += [zigzag_102(500)]
big9 += [[0] + [500] * 499]  # 只有第一扇能揭，其余阈值 = m，全 -1
big9 += [random_ok(500, rng) for _ in range(5)]
dump(9, big9, "n=500 构造+随机")

big10 = [random_any(500, rng) for _ in range(4)]
big10 += [random_ok(500, rng) for _ in range(4)]
big10 += [zigzag_102(499) + [0]]  # 长度 500
big10 += [[i % 7 for i in range(500)]]
# 保证有 0
big10[-1][0] = 0
dump(10, big10, "n=500 混合压测")

ok = True
for i in range(1, 11):
    raw = (DATA / f"{i}.in").read_bytes().decode("utf-8")
    parts = raw.split("\n")
    q = int(parts[0])
    p = 1
    cases = []
    for _ in range(q):
        n = int(parts[p])
        w = list(map(int, parts[p + 1].split()))
        assert len(w) == n
        cases.append(w)
        p += 2
    exp = (DATA / f"{i}.out").read_text(encoding="utf-8")
    got = format_out(cases)
    if got != exp:
        print(f"MISMATCH {i}")
        ok = False
if not ok:
    raise SystemExit(1)
print("ok")
