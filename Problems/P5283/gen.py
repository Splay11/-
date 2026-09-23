# -*- coding: utf-8 -*-
import random
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
from std import solve

DATA = ROOT / "data"
RNG = random.Random(528320260823)


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


def pack(n, k, pairs):
  lines = [f"{n} {k}"]
  for a, b in pairs:
    lines.append(f"{a} {b}")
  return "\n".join(lines)


def rand_case(n, ahi=10**9, bhi=10**9):
  pairs = [(RNG.randint(0, ahi), RNG.randint(0, bhi)) for _ in range(n)]
  total = sum(b for _, b in pairs)
  mode = RNG.randint(0, 3)
  if mode == 0:
    k = total  # answer 0
  elif mode == 1:
    k = 0
  elif mode == 2:
    k = RNG.randint(0, total) if total > 0 else 0
  else:
    k = RNG.randint(0, 10**18)
  return n, k, pairs


def main():
  cases = []
  cases.append(pack(4, 5, [(3, 2), (5, 3), (2, 4), (5, 1)]))
  cases.append(pack(3, 6, [(4, 2), (7, 5), (1, 3)]))
  cases.append(pack(1, 0, [(0, 0)]))
  cases.append(pack(2, 10, [(1, 3), (2, 4)]))
  cases.append(pack(3, 0, [(10, 1), (20, 2), (30, 3)]))
  cases.append(pack(*rand_case(10, 20, 10)))
  cases.append(pack(*rand_case(100, 1000, 1000)))
  n, _, pairs = rand_case(2000)
  tot = sum(b for _, b in pairs)
  cases.append(pack(n, tot // 3, pairs))
  n, _, pairs = rand_case(20000)
  tot = sum(b for _, b in pairs)
  cases.append(pack(n, tot // 2, pairs))
  n, _, pairs = rand_case(100000)
  tot = sum(b for _, b in pairs)
  cases.append(pack(n, max(0, tot // 10), pairs))

  assert len(cases) == 10
  for i, tin in enumerate(cases, 1):
    lines = tin.split("\n")
    n, k = map(int, lines[0].split())
    pairs = [tuple(map(int, ln.split())) for ln in lines[1:]]
    exp = solve(n, k, pairs)
    tout = run_std(tin)
    if not tout.endswith("\n"):
      tout += "\n"
    if int(tout.strip()) != exp:
      raise RuntimeError(f"mismatch {i}")
    write_pair(i, tin, tout)
    print(f"{i} ok n={n} k={k} ans={exp}")


if __name__ == "__main__":
  main()
