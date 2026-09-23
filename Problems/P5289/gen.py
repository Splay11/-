# -*- coding: utf-8 -*-
import random
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
from std import solve

DATA = ROOT / "data"
RNG = random.Random(528920260823)


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


def pack(n, edges):
  lines = [str(n)]
  for u, v, w in edges:
    lines.append(f"{u} {v} {w}")
  return "\n".join(lines)


def rand_tree(n, wlo=0, whi=10**9):
  edges = []
  for i in range(2, n + 1):
    p = RNG.randint(1, i - 1)
    w = RNG.randint(wlo, whi)
    if RNG.random() < 0.5:
      edges.append((p, i, w))
    else:
      edges.append((i, p, w))
  RNG.shuffle(edges)
  return edges


def star(n, wlo=1, whi=100):
  edges = []
  for i in range(2, n + 1):
    edges.append((1, i, RNG.randint(wlo, whi)))
  return edges


def chain(n, wlo=1, whi=100):
  return [(i, i + 1, RNG.randint(wlo, whi)) for i in range(1, n)]


def main():
  cases = []
  # 1 原题样例1
  cases.append(pack(3, [(1, 2, 3), (2, 3, 4)]))
  # 2 原题样例2
  cases.append(pack(5, [(5, 3, 60), (4, 3, 63), (2, 1, 97), (3, 1, 14)]))
  # 3 单点
  cases.append(pack(1, []))
  # 4 改写样例：链+分支
  cases.append(pack(4, [(1, 2, 1), (1, 3, 2), (3, 4, 3)]))
  # 5 hack：直径不经过 1，卡「减去树直径」
  cases.append(pack(4, [(1, 2, 1), (2, 3, 100), (2, 4, 100)]))
  # 6 星形
  cases.append(pack(8, star(8, 1, 20)))
  # 7 小随机树
  cases.append(pack(30, rand_tree(30, 0, 1000)))
  # 8 中等链，权值较大
  cases.append(pack(200, chain(200, 10**8, 10**9)))
  # 9 大数据随机树
  cases.append(pack(100000, rand_tree(100000, 0, 10**9)))
  # 10 大数据星形 + 大边权，卡 int 溢出和「只加一遍边权」
  cases.append(pack(100000, star(100000, 10**9, 10**9)))

  assert len(cases) == 10
  for i, tin in enumerate(cases, 1):
    lines = tin.split("\n")
    n = int(lines[0])
    edges = []
    for ln in lines[1:]:
      if not ln:
        continue
      u, v, w = map(int, ln.split())
      edges.append((u, v, w))
    if len(edges) != n - 1:
      raise RuntimeError(f"edge count {i}")
    exp = solve(n, edges)
    tout = run_std(tin)
    if not tout.endswith("\n"):
      tout += "\n"
    if int(tout.strip()) != exp:
      raise RuntimeError(f"stdio mismatch {i}")
    write_pair(i, tin, tout)
    print(f"{i} ok n={n} ans={exp}")


if __name__ == "__main__":
  main()
