# -*- coding: utf-8 -*-
import random
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
from std import solve

DATA = ROOT / "data"
RNG = random.Random(528420260823)


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


def pack(n, e, a, b):
  lines = [
    str(n),
    " ".join(map(str, e)),
    " ".join(map(str, a)),
    " ".join(map(str, b)),
  ]
  return "\n".join(lines)


def rand_case(n, ahi=10**9):
  e = [RNG.randint(1, n + 1) for _ in range(n)]
  a = [RNG.randint(0, ahi) for _ in range(n)]
  b = [RNG.randint(0, ahi) for _ in range(n)]
  return n, e, a, b


def main():
  cases = []
  cases.append(pack(3, [3, 4, 3], [2, 1, 1], [1, 3, 1]))
  cases.append(pack(4, [3, 5, 4, 6], [3, 0, 2, 1], [2, 2, 3, 1]))
  cases.append(pack(1, [1], [5], [3]))
  cases.append(pack(2, [2, 3], [0, 0], [1, 1]))
  cases.append(pack(*rand_case(8, 20)))
  cases.append(pack(*rand_case(30, 100)))
  cases.append(pack(*rand_case(200, 1000)))
  cases.append(pack(*rand_case(2000)))
  cases.append(pack(*rand_case(20000)))
  cases.append(pack(*rand_case(100000)))

  assert len(cases) == 10
  for i, tin in enumerate(cases, 1):
    lines = tin.split("\n")
    n = int(lines[0])
    e = list(map(int, lines[1].split()))
    a = list(map(int, lines[2].split()))
    b = list(map(int, lines[3].split()))
    exp = solve(n, e, a, b)
    tout = run_std(tin)
    if not tout.endswith("\n"):
      tout += "\n"
    if int(tout.strip()) != exp:
      raise RuntimeError(f"mismatch {i}")
    write_pair(i, tin, tout)
    print(f"{i} ok n={n} ans={exp}")


if __name__ == "__main__":
  main()
