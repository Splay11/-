# -*- coding: utf-8 -*-
import random
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
RNG = random.Random(528220260823)


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


def pack(n, m, grid):
  lines = [f"{n} {m}"]
  for row in grid:
    lines.append(" ".join(map(str, row)))
  return "\n".join(lines)


def rand_grid(n, m, lo=-1000, hi=1000):
  return [[RNG.randint(lo, hi) for _ in range(m)] for _ in range(n)]


def main():
  cases = []
  cases.append(pack(3, 4, [[-5, 3, 4, -1], [-1, 9, 0, 2], [-2, -6, -5, -2]]))
  cases.append(pack(2, 3, [[2, -3, 4], [1, 5, -1]]))
  cases.append(pack(1, 1, [[-7]]))
  cases.append(pack(1, 5, [[3, -2, 8, -4, 5]]))
  cases.append(pack(4, 1, [[2], [-3], [6], [-1]]))
  cases.append(pack(3, 3, [[-1, -2, -3], [-4, -5, -6], [-7, -8, -9]]))
  cases.append(pack(8, 8, rand_grid(8, 8, -20, 20)))
  cases.append(pack(30, 40, rand_grid(30, 40)))
  cases.append(pack(80, 80, rand_grid(80, 80)))
  cases.append(pack(150, 150, rand_grid(150, 150)))

  assert len(cases) == 10
  for i, tin in enumerate(cases, 1):
    tout = run_std(tin)
    if not tout.endswith("\n"):
      tout += "\n"
    write_pair(i, tin, tout)
    n, m = map(int, tin.split("\n")[0].split())
    print(f"{i} ok n={n} m={m}")


if __name__ == "__main__":
  main()
