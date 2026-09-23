# -*- coding: utf-8 -*-
import random
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
from std import solve

DATA = ROOT / "data"
RNG = random.Random(526920260820)


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


def rand_arr(n):
    return [RNG.randint(-n, n) for _ in range(n)]


def main():
    cases = []
    # 1 样例
    cases.append(case_from_lists([[3, -1, 2, 0], [-2, 0, -1], [1, 2, 3, 4, 5]]))
    # 2 单点
    cases.append(case_from_lists([[5]]))
    # 3 全正
    cases.append(case_from_lists([[1, 2, 3]]))
    # 4 全负
    cases.append(case_from_lists([[-3, -2, -5]]))
    # 5 含 0
    cases.append(case_from_lists([[0, 0, 0, 1]]))
    # 6 随机小
    cases.append(case_from_lists([rand_arr(10), rand_arr(8)]))
    # 7 构造：一大若干负
    cases.append(case_from_lists([[10] + [-1] * 15]))
    # 8 中等随机
    cases.append(case_from_lists([rand_arr(50), rand_arr(40), rand_arr(30)]))
    # 9 大数据
    big1 = [RNG.randint(-1000, 1000) for _ in range(50000)]
    big2 = [RNG.randint(1, 1000) for _ in range(50000)]
    cases.append(case_from_lists([big1, big2]))
    # 10 满规模
    cases.append(case_from_lists([[RNG.randint(-200000, 200000) for _ in range(100000)],
                                   [RNG.randint(-200000, 200000) for _ in range(100000)]]))

    assert len(cases) == 10
    for i, tin in enumerate(cases, 1):
        # 校验小数据
        lines = tin.split("\n")
        t = int(lines[0])
        idx = 1
        for _ in range(t):
            n = int(lines[idx]); idx += 1
            a = list(map(int, lines[idx].split())); idx += 1
            assert len(a) == n
            solve(a)
        tout = run_std(tin)
        if not tout.endswith("\n"):
            tout += "\n"
        write_pair(i, tin, tout)
        print(f"{i}.in ok bytes={len(tin)}")


if __name__ == "__main__":
    main()
