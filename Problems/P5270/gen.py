# -*- coding: utf-8 -*-
import random
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
from std import solve

DATA = ROOT / "data"
RNG = random.Random(527020260820)


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


def case_from_lists(groups):
    lines = [str(len(groups))]
    for a in groups:
        lines.append(str(len(a)))
        lines.append(" ".join(map(str, a)))
    return "\n".join(lines)


def rand_arr(n, lo=1, hi=10**9):
    return [RNG.randint(lo, hi) for _ in range(n)]


def main():
    cases = []
    cases.append(case_from_lists([[1, 2, 3, 4], [1, 2], [1, 5, 10]]))
    cases.append(case_from_lists([[1]]))
    cases.append(case_from_lists([[5, 5, 5, 5]]))
    cases.append(case_from_lists([[1, 3]]))  # 奇数和 -> -1
    cases.append(case_from_lists([[9, 1, 2, 8]]))
    cases.append(case_from_lists([rand_arr(7, 1, 20), rand_arr(8, 1, 20)]))
    cases.append(case_from_lists([[10**9] * 10]))
    cases.append(case_from_lists([rand_arr(100, 1, 1000)] * 3))
    # 9
    groups = []
    rem = 100000
    while rem > 0:
        n = min(rem, RNG.randint(1, 5000))
        groups.append(rand_arr(n))
        rem -= n
    cases.append(case_from_lists(groups))
    # 10：满 sum n，数值用较小位数以控制文件体积
    cases.append(case_from_lists([[RNG.randint(1, 10**6) for _ in range(250000)],
                                   [RNG.randint(1, 10**6) for _ in range(250000)]]))

    assert len(cases) == 10
    for i, tin in enumerate(cases, 1):
        tout = run_std(tin)
        if not tout.endswith("\n"):
            tout += "\n"
        write_pair(i, tin, tout)
        print(f"{i}.in ok bytes={len(tin)}")


if __name__ == "__main__":
    main()
