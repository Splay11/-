# -*- coding: utf-8 -*-
"""P5498：1-2 样例约 20%；3-10 为 n=m=D=1e5 的查询压测。"""
from __future__ import print_function

import os
import random

DIR = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(DIR, "data")
NMAX = 100000
MMAX = 100000


def write_in(path, lines):
    text = "\n".join(lines)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)


def dump_case(n, m, d, k, w, qs):
    lines = ["%d %d %d %d" % (n, m, d, k)]
    lines.append(" ".join(str(x) for x in w))
    for x in qs:
        lines.append(str(x))
    return lines


def sample1():
    return 5, 4, 2, 1, [10, 8, 9, 5, 7], [3, 5, 4, 1]


def sample2():
    return 4, 3, 3, 0, [6, 6, 4, 6], [4, 2, 1]


def heavy_qs(rng, n, m, lo):
    return [rng.randint(lo, n) for _ in range(m)]


def main():
    os.makedirs(DATA, exist_ok=True)
    rng = random.Random(54982)
    cases = [
        sample1(),
        sample2(),
        (NMAX, MMAX, NMAX, rng.randint(0, 10 ** 6),
         [rng.randint(1, 10 ** 9) for _ in range(NMAX)],
         heavy_qs(rng, NMAX, MMAX, NMAX - NMAX // 20)),
        (NMAX, MMAX, NMAX, 0, [7] * NMAX, [NMAX] * MMAX),
        (NMAX, MMAX, NMAX, 10 ** 9,
         [rng.randint(1, 10 ** 9) for _ in range(NMAX)],
         [NMAX] * MMAX),
        (NMAX, MMAX, NMAX, 1,
         [10 ** 9] * (NMAX // 2) + [1] * (NMAX - NMAX // 2),
         [NMAX] * MMAX),
        (NMAX, MMAX, NMAX - 2000, 0,
         [1] * 1999 + [10 ** 9] * (NMAX - 1999),
         [NMAX] * MMAX),
        (NMAX, MMAX, NMAX, 1, list(range(NMAX, 0, -1)),
         heavy_qs(rng, NMAX, MMAX, NMAX - 10)),
        (NMAX, MMAX, NMAX, rng.randint(0, 1000),
         [rng.randint(1, 10 ** 6) for _ in range(NMAX)],
         [NMAX] * MMAX),
        (NMAX, MMAX, NMAX, 0,
         [rng.randint(1, 10 ** 9) for _ in range(NMAX)],
         [NMAX] * MMAX),
    ]
    for i, (n, m, d, k, w, qs) in enumerate(cases, 1):
        assert len(w) == n and len(qs) == m
        path = os.path.join(DATA, "%d.in" % i)
        write_in(path, dump_case(n, m, d, k, w, qs))
        print("wrote", path, "n=%d m=%d D=%d" % (n, m, d))


if __name__ == "__main__":
    main()
