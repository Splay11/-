# -*- coding: utf-8 -*-
import random
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
from std import solve

DATA = ROOT / "data"
RNG = random.Random(526820260820)


def run_std(text):
    r = subprocess.run([sys.executable, str(ROOT / "std.py")], input=text.encode(), capture_output=True, check=True)
    return r.stdout.decode()


def write_pair(idx, tin, tout):
    DATA.mkdir(parents=True, exist_ok=True)
    if tin.endswith("\n"):
        raise RuntimeError("in trailing nl")
    if not tout.endswith("\n") or tout.endswith("\n\n"):
        raise RuntimeError("out nl")
    (DATA / f"{idx}.in").write_bytes(tin.encode())
    (DATA / f"{idx}.out").write_bytes(tout.encode())


def fmt_case(n, m, p, q, y, a, b):
    lines = [f"{n} {m} {p} {q} {y}"]
    if n:
        lines.append(" ".join(map(str, a)))
    if m:
        lines.append(" ".join(map(str, b)))
    return lines


def pack(groups):
    lines = [str(len(groups))]
    for g in groups:
        lines.extend(g)
    return "\n".join(lines)


def main():
    cases = []
    # sample-like
    cases.append(pack([
        fmt_case(1, 1, 1, 2, 9, [100], [500000000]),
        fmt_case(0, 2, 1, 1, 6, [], [999999, 999999]),
        fmt_case(1, 0, 99, 100, 3, [10], []),
        fmt_case(0, 0, 1, 1, 2, [], []),
    ]))
    cases.append(pack([fmt_case(0, 0, 1, 2, 5, [], [])]))  # only m3 half → No
    cases.append(pack([fmt_case(0, 1, 1, 1, 3, [], [1000])]))  # Yes exact
    cases.append(pack([fmt_case(2, 2, 1, 2, 8, [2, 3], [100000000, 200000000])]))
    cases.append(pack([fmt_case(0, 0, 1, 1, 0, [], [])]))  # hp=1, m3 kills
    # random small
    gs = []
    for _ in range(5):
        n = RNG.randint(0, 4)
        m = RNG.randint(0, 6)
        p = RNG.randint(1, 20)
        q = RNG.randint(p, 30)
        y = RNG.randint(0, 12)
        a = [RNG.randint(1, 50) for _ in range(n)]
        b = [RNG.randint(1, 10**9) for _ in range(m)]
        gs.append(fmt_case(n, m, p, q, y, a, b))
    cases.append(pack(gs))
    # medium
    gs = []
    for _ in range(3):
        n = RNG.randint(0, 6)
        m = RNG.randint(0, 10)
        p = RNG.randint(1, 100)
        q = RNG.randint(max(p, 1), 100)
        y = RNG.randint(0, 15)
        a = [RNG.randint(1, 1000) for _ in range(n)]
        b = [RNG.randint(1, 10**9) for _ in range(m)]
        gs.append(fmt_case(n, m, p, q, y, a, b))
    cases.append(pack(gs))
    cases.append(pack([fmt_case(3, 8, 50, 100, 18, [2, 5, 10], [RNG.randint(1, 10**9) for _ in range(8)])]))
    cases.append(pack([fmt_case(5, 12, 1, 1, 10, [RNG.randint(1, 20) for _ in range(5)], [RNG.randint(1, 10**6) for _ in range(12)])]))
    cases.append(pack([
        fmt_case(0, 3, 1, 1, 7, [], [3, 3, 3]),
        fmt_case(1, 0, 1, 1, 4, [100], []),
        fmt_case(0, 0, 3, 10, 6, [], []),
    ]))

    assert len(cases) == 10
    for i, tin in enumerate(cases, 1):
        # sanity
        data = list(map(int, tin.split()))
        it = iter(data)
        T = next(it)
        for _ in range(T):
            n = next(it); m = next(it); p = next(it); qq = next(it); y = next(it)
            a = [next(it) for _ in range(n)]
            b = [next(it) for _ in range(m)]
            solve(n, m, p, qq, y, a, b)
        tout = run_std(tin)
        if not tout.endswith("\n"):
            tout += "\n"
        write_pair(i, tin, tout)
        print(f"{i} ok")


if __name__ == "__main__":
    main()
