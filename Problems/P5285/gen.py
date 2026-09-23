# -*- coding: utf-8 -*-
import random
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
RNG = random.Random(528520260823)


def run_std(text):
  r = subprocess.run(
    ["python", str(ROOT / "std.py")],
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


def pack(n, A, B, a):
  return f"{n} {A} {B}\n" + " ".join(map(str, a))


def rand_case(n, ahi=10**9):
  A = RNG.randint(0, ahi)
  B = RNG.randint(0, ahi)
  while B == A:
    B = RNG.randint(0, ahi)
  a = [RNG.choice([A, B, RNG.randint(0, min(ahi, 20))]) for _ in range(n)]
  if A not in a:
    a[0] = A
  if B not in a:
    a[-1] = B
  return n, A, B, a


def main():
  cases = []
  cases.append(pack(2, 1, 2, [1, 2]))
  cases.append(pack(5, 1, 2, [1, 2, 2, 2, 3]))
  cases.append(pack(3, 8, 5, [8, 5, 5]))
  cases.append(pack(4, 0, 1, [0, 0, 1, 1]))
  cases.append(pack(2, 0, 10**9, [0, 10**9]))
  cases.append(pack(*rand_case(10, 20)))
  cases.append(pack(*rand_case(100, 1000)))
  cases.append(pack(*rand_case(2000)))
  cases.append(pack(*rand_case(20000)))
  cases.append(pack(*rand_case(100000)))

  assert len(cases) == 10
  for i, tin in enumerate(cases, 1):
    tout = run_std(tin)
    if not tout.endswith("\n"):
      tout += "\n"
    write_pair(i, tin, tout)
    print(f"{i} ok out={tout.strip()}")


if __name__ == "__main__":
  main()
