# -*- coding: utf-8 -*-
import random
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
from std import solve

DATA = ROOT / "data"
RNG = random.Random(527720260822)


def run_std(text):
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
    raise RuntimeError("in trailing nl")
  if not tout.endswith("\n") or tout.endswith("\n\n"):
    raise RuntimeError("out nl")
  (DATA / f"{idx}.in").write_bytes(tin.encode())
  (DATA / f"{idx}.out").write_bytes(tout.encode())


def pack(n, m, b, ops):
  lines = [f"{n} {m}", " ".join(map(str, b))]
  for x, y in ops:
    lines.append(f"{x} {y}")
  return "\n".join(lines)


def rand_case(n, m, hi=10**9):
  b = [RNG.randint(1, hi) for _ in range(n)]
  ops = [(RNG.randint(1, n), RNG.randint(1, hi)) for _ in range(m)]
  return n, m, b, ops


def main():
  cases = []
  cases.append(pack(5, 3, [1, 3, 6, 10, 15], [(3, 8), (1, 2), (5, 20)]))
  n, m, b, ops = rand_case(4, 2, 20)
  cases.append(pack(n, m, b, ops))
  cases.append(pack(3, 3, [1, 5, 9], [(1, 4), (2, 7), (3, 12)]))
  cases.append(pack(6, 5, [2, 5, 9, 12, 18, 25], [(2, 15), (4, 30), (1, 1), (6, 40), (3, 10)]))
  cases.append(pack(*rand_case(10, 10, 1000)))
  cases.append(pack(*rand_case(50, 50, 10**6)))
  cases.append(pack(*rand_case(500, 500, 10**9)))
  cases.append(pack(*rand_case(2000, 2000, 10**9)))
  cases.append(pack(*rand_case(12000, 12000, 10**9)))
  cases.append(pack(*rand_case(20000, 20000, 10**9)))

  assert len(cases) == 10
  for i, tin in enumerate(cases, 1):
    lines = tin.split("\n")
    n, m = map(int, lines[0].split())
    b = list(map(int, lines[1].split()))
    ops = [tuple(map(int, ln.split())) for ln in lines[2:]]
    solve(n, b.copy(), ops)
    tout = run_std(tin)
    if not tout.endswith("\n"):
      tout += "\n"
    write_pair(i, tin, tout)
    print(f"{i} ok n={n} m={m}")


if __name__ == "__main__":
  main()
