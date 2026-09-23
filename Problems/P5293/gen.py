# -*- coding: utf-8 -*-
import random
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
from std import solve

DATA = ROOT / "data"
RNG = random.Random(529320260823)


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


def pack(n, F, p, edges):
  lines = [f"{n} {len(edges)} {F}", " ".join(map(str, p))]
  for e in edges:
    lines.append(" ".join(map(str, e)))
  return "\n".join(lines)


def rand_graph(n, m, F, connect=True):
  p = [RNG.randint(0, 100) for _ in range(n)]
  edges = []
  seen = set()
  if connect:
    for i in range(1, n):
      c = RNG.randint(1, min(F, 100))
      t = RNG.randint(1, 1000)
      edges.append((i, i + 1, c, t))
      seen.add((i, i + 1))
  while len(edges) < m:
    u = RNG.randint(1, n)
    v = RNG.randint(1, n)
    if u == v:
      continue
    a, b = min(u, v), max(u, v)
    if (a, b) in seen:
      continue
    seen.add((a, b))
    c = RNG.randint(1, 100)
    t = RNG.randint(1, 1000)
    edges.append((u, v, c, t))
  RNG.shuffle(edges)
  return p, edges


def main():
  cases = []
  # 1 原题样例（按「出发满箱」应为 18，原题面写 31 与规则不符）
  cases.append(pack(3, 10, [5, 3, 4], [(1, 2, 5, 10), (2, 3, 4, 8), (1, 3, 12, 100)]))
  # 2 改写样例：中途在便宜站充电
  cases.append(pack(4, 5, [2, 1, 9, 3], [(1, 2, 3, 4), (2, 3, 3, 5), (3, 4, 2, 6)]))
  # 3 耗能超过容量，不可达
  cases.append(pack(2, 3, [1, 1], [(1, 2, 4, 10)]))
  # 4 出发满电刚好够，不必加油
  cases.append(pack(2, 5, [10, 1], [(1, 2, 2, 7)]))
  # 5 起点充电耗时为 0
  cases.append(pack(3, 4, [0, 5, 1], [(1, 2, 2, 3), (2, 3, 2, 4)]))
  # 6 无边，不可达
  cases.append(pack(3, 10, [1, 1, 1], [(1, 2, 1, 1)]))
  # 7 小随机连通
  p, e = rand_graph(8, 15, 20)
  cases.append(pack(8, 20, p, e))
  # 8 必须绕去便宜补给站
  cases.append(pack(5, 6, [9, 9, 1, 9, 9], [(1, 2, 4, 3), (2, 5, 4, 100), (2, 3, 2, 2), (3, 4, 2, 2), (4, 5, 2, 2)]))
  # 9 大数据连通随机
  p, e = rand_graph(1000, 10000, 100)
  cases.append(pack(1000, 100, p, e))
  # 10 大数据：链上偶发超容量边 + 高加油费
  n = 1000
  p = [RNG.randint(50, 100) for _ in range(n)]
  p[0] = 0
  p[n // 2] = 1
  e = []
  for i in range(1, n):
    e.append((i, i + 1, RNG.randint(1, 40), RNG.randint(1, 1000)))
  for _ in range(9000):
    u = RNG.randint(1, n)
    v = RNG.randint(1, n)
    if u != v:
      e.append((u, v, RNG.randint(60, 100), RNG.randint(1, 50)))
  cases.append(pack(n, 100, p, e[:10000]))

  assert len(cases) == 10
  for i, tin in enumerate(cases, 1):
    lines = tin.split("\n")
    n, m, F = map(int, lines[0].split())
    p = [0] + list(map(int, lines[1].split()))
    edges = [tuple(map(int, ln.split())) for ln in lines[2:]]
    if len(edges) != m:
      raise RuntimeError(f"m mismatch {i}")
    exp = solve(n, F, p, edges)
    tout = run_std(tin)
    if not tout.endswith("\n"):
      tout += "\n"
    if int(tout.strip()) != exp:
      raise RuntimeError(f"stdio mismatch {i}")
    write_pair(i, tin, tout)
    print(f"{i} ok n={n} m={m} F={F} ans={exp}")


if __name__ == "__main__":
  main()
