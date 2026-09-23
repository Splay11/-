# -*- coding: utf-8 -*-
import random
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
RNG = random.Random(528720260823)


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


def pack(n, s, directed, undirected, a, b, dests):
  lines = [f"{n} {len(directed)} {len(undirected)} {s}"]
  for e in directed:
    lines.append(f"{e[0]} {e[1]} {e[2]}")
  for e in undirected:
    lines.append(f"{e[0]} {e[1]} {e[2]}")
  lines.append(f"{a} {b} {len(dests)}")
  lines.append(" ".join(map(str, dests)))
  return "\n".join(lines)


def rand_graph(n, extra_d=0, extra_u=0, wmax=100):
  undirected = []
  for i in range(1, n):
    undirected.append((i, i + 1, RNG.randint(0, wmax)))
  undirected.append((n, 1, RNG.randint(0, wmax)))
  directed = []
  for _ in range(extra_d):
    u = RNG.randint(1, n)
    v = RNG.randint(1, n)
    directed.append((u, v, RNG.randint(0, wmax)))
  for _ in range(extra_u):
    u = RNG.randint(1, n)
    v = RNG.randint(1, n)
    undirected.append((u, v, RNG.randint(0, wmax)))
  s = RNG.randint(1, n)
  q = RNG.randint(1, 10)
  dests = [RNG.randint(1, n) for _ in range(q)]
  a = RNG.randint(1, 20)
  b = RNG.randint(1, 20)
  return pack(n, s, directed, undirected, a, b, dests)


def main():
  cases = []
  cases.append(
    pack(3, 1, [], [(1, 2, 3), (3, 2, 6), (1, 3, 9)], 6, 3, [1, 2, 3])
  )
  cases.append(
    pack(
      6,
      2,
      [(1, 2, 1), (4, 1, 2), (3, 5, 2), (2, 3, 1)],
      [(6, 3, 1), (4, 5, 1), (1, 3, 3), (2, 4, 2)],
      2,
      3,
      [1, 4, 6, 6, 2],
    )
  )
  cases.append(pack(4, 1, [], [(1, 2, 1), (2, 3, 1), (3, 4, 1), (4, 1, 1)], 3, 1, [2, 4, 3]))
  cases.append(pack(3, 2, [], [(1, 2, 2), (2, 3, 2), (3, 1, 2)], 5, 4, [3, 3]))
  cases.append(rand_graph(8, 4, 3, 20))
  cases.append(rand_graph(20, 10, 8, 50))
  cases.append(rand_graph(80, 40, 20))
  cases.append(rand_graph(400, 200, 100))
  cases.append(rand_graph(3000, 1500, 800))
  cases.append(rand_graph(20000, 8000, 4000, 100000))

  assert len(cases) == 10
  for i, tin in enumerate(cases, 1):
    tout = run_std(tin)
    if not tout.endswith("\n"):
      tout += "\n"
    write_pair(i, tin, tout)
    n = tin.split("\n")[0].split()[0]
    print(f"{i} ok n={n} ans={tout.strip()}")


if __name__ == "__main__":
  main()
