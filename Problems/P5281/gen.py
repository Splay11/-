# -*- coding: utf-8 -*-
import random
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
RNG = random.Random(528120260823)


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


def pack(n, people, queries):
  lines = [str(n)]
  for wi, ai, bi in people:
    lines.append(f"{wi} {ai} {bi}")
  lines.append(str(len(queries)))
  for x in queries:
    lines.append(str(x))
  return "\n".join(lines)


def rand_people(n, hi=500):
  w = [RNG.randint(1, hi) for _ in range(n)]
  a = [RNG.randint(1, w[i]) for i in range(n)]
  b = [RNG.randint(1, hi) for _ in range(n)]
  return w, a, b


def rand_queries(q, hi=10**9):
  return [RNG.randint(0, hi) for _ in range(q)]


def main():
  cases = []
  cases.append(
    pack(
      3,
      [(10, 5, 3), (20, 8, 4), (15, 6, 2)],
      [0, 5, 10, 15, 20],
    )
  )
  w, a, b = rand_people(3, 20)
  cases.append(pack(3, list(zip(w, a, b)), rand_queries(5, 100)))
  cases.append(pack(1, [(5, 3, 2)], [0, 5, 10]))
  cases.append(
    pack(
      5,
      [(10, 5, 3), (20, 8, 4), (15, 6, 2), (8, 4, 1), (12, 7, 5)],
      [0, 100, 500, 1000, 10**9],
    )
  )
  w, a, b = rand_people(10)
  cases.append(pack(10, list(zip(w, a, b)), rand_queries(20, 1000)))
  w, a, b = rand_people(50)
  cases.append(pack(50, list(zip(w, a, b)), rand_queries(100)))
  w, a, b = rand_people(200)
  cases.append(pack(200, list(zip(w, a, b)), rand_queries(500)))
  w, a, b = rand_people(1000)
  cases.append(pack(1000, list(zip(w, a, b)), rand_queries(2000)))
  w, a, b = rand_people(3000)
  cases.append(pack(3000, list(zip(w, a, b)), rand_queries(3000)))
  w, a, b = rand_people(3500)
  cases.append(pack(3500, list(zip(w, a, b)), rand_queries(6000)))

  assert len(cases) == 10
  for i, tin in enumerate(cases, 1):
    lines = tin.split("\n")
    n = int(lines[0])
    w, a, b = [], [], []
    for j in range(n):
      wi, ai, bi = map(int, lines[j + 1].split())
      w.append(wi)
      a.append(ai)
      b.append(bi)
    q = int(lines[n + 1])
    tout = run_std(tin)
    if not tout.endswith("\n"):
      tout += "\n"
    write_pair(i, tin, tout)
    print(f"{i} ok n={n} q={q}")


if __name__ == "__main__":
  main()
