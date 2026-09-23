# -*- coding: utf-8 -*-
import random
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
from std import solve

DATA = ROOT / "data"
RNG = random.Random(527120260820)


def run_std(text: str) -> str:
    r = subprocess.run(
        [sys.executable, str(ROOT / "std.py")],
        input=text.encode(),
        capture_output=True,
        check=True,
    )
    return r.stdout.decode()


def write_pair(idx, tin, tout):
    DATA.mkdir(parents=True, exist_ok=True)
    if tin.endswith("\n"):
        raise RuntimeError(f"{idx}.in trailing newline")
    if not tout.endswith("\n") or tout.endswith("\n\n"):
        raise RuntimeError(f"{idx}.out bad newline")
    (DATA / f"{idx}.in").write_bytes(tin.encode())
    (DATA / f"{idx}.out").write_bytes(tout.encode())


def fmt_case(items):
    # items: list of (n, k, p)
    lines = [str(len(items))]
    for n, k, p in items:
        lines.append(f"{n} {k}")
        lines.append(" ".join(map(str, p)))
    return "\n".join(lines)


def rand_perm(n):
    p = list(range(1, n + 1))
    RNG.shuffle(p)
    return p


def main():
    cases = []
    cases.append(fmt_case([
        (5, 3, [3, 1, 2, 5, 4]),
        (4, 10, [4, 3, 2, 1]),
        (5, 0, [5, 1, 2, 3, 4]),
    ]))
    cases.append(fmt_case([(1, 5, [1])]))
    cases.append(fmt_case([(3, 0, [1, 2, 3])]))
    cases.append(fmt_case([(3, 100, [3, 2, 1])]))
    cases.append(fmt_case([(6, 2, [2, 1, 4, 3, 6, 5])]))
    cases.append(fmt_case([(10, 5, rand_perm(10)), (8, 1, rand_perm(8))]))
    cases.append(fmt_case([(15, 0, rand_perm(15))]))
    cases.append(fmt_case([(20, 50, rand_perm(20)), (12, 1000000000, list(range(12, 0, -1)))]))
    # 9: several medium
    items = []
    rem = 400
    while rem > 0:
        n = min(rem, RNG.randint(1, 80))
        items.append((n, RNG.randint(0, 10**9), rand_perm(n)))
        rem -= n
    cases.append(fmt_case(items))
    # 10: near sum n = 1000
    items = []
    rem = 1000
    while rem > 0:
        n = min(rem, RNG.randint(50, 200) if rem > 50 else rem)
        items.append((n, RNG.randint(0, 10**9), rand_perm(n)))
        rem -= n
    cases.append(fmt_case(items))

    assert len(cases) == 10
    for i, tin in enumerate(cases, 1):
        # 校验
        lines = tin.split("\n")
        t = int(lines[0])
        idx = 1
        for _ in range(t):
            n, k = map(int, lines[idx].split()); idx += 1
            p = list(map(int, lines[idx].split())); idx += 1
            assert sorted(p) == list(range(1, n + 1))
            solve(p, k)
        tout = run_std(tin)
        if not tout.endswith("\n"):
            tout += "\n"
        write_pair(i, tin, tout)
        print(f"{i}.in ok bytes={len(tin)}")


if __name__ == "__main__":
    main()
