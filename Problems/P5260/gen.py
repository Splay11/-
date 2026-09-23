# -*- coding: utf-8 -*-
import random
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
from std import solve

DATA = ROOT / "data"
RNG = random.Random(526020260820)


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


def pack(groups):
    lines = [str(len(groups))]
    for a in groups:
        lines.append(str(len(a)))
        lines.append(" ".join(map(str, a)))
    return "\n".join(lines)


def main():
    cases = []
    cases.append(pack([[1, 4, 0, 3, 1]]))
    cases.append(pack([[-1, 2, 3], [1, 2, 2, 4]]))
    cases.append(pack([[1]]))
    cases.append(pack([[0], [2], [4]]))
    cases.append(pack([[1, 1, 1, 1]]))
    cases.append(pack([[RNG.randint(-100, 100) for _ in range(20)] for _ in range(5)]))
    cases.append(pack([[100] * 50, [-100] * 50]))
    # many length-1 ones
    cases.append(pack([[1 if RNG.random() < 0.3 else RNG.randint(-5, 5) for _ in range(200)]]))
    # big（控制规模，保证 py.py3 也能过）
    groups = []
    rem = 40000
    while rem > 0:
        n = min(rem, RNG.randint(1, 2000))
        groups.append([RNG.randint(-100, 100) for _ in range(n)])
        rem -= n
    cases.append(pack(groups))
    cases.append(pack([[RNG.randint(-100, 100) for _ in range(25000)],
                        [RNG.randint(-100, 100) for _ in range(25000)]]))

    assert len(cases) == 10
    for i, tin in enumerate(cases, 1):
        # verify small
        lines = tin.split("\n")
        t = int(lines[0]); idx = 1
        for _ in range(t):
            n = int(lines[idx]); idx += 1
            a = list(map(int, lines[idx].split())); idx += 1
            assert solve(a) >= 0
        tout = run_std(tin)
        if not tout.endswith("\n"):
            tout += "\n"
        write_pair(i, tin, tout)
        print(f"{i} ok {len(tin)}")


if __name__ == "__main__":
    main()
