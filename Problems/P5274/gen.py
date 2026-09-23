# -*- coding: utf-8 -*-
import random
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
from std import solve

DATA = ROOT / "data"
RNG = random.Random(527420260824)


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
  lines = [f"{n} {len(edges)}"]
  for u, v in edges:
    lines.append(f"{u} {v}")
  return "\n".join(lines)


def parse(tin):
  lines = tin.split("\n")
  n, m = map(int, lines[0].split())
  edges = []
  for i in range(m):
    u, v = map(int, lines[1 + i].split())
    edges.append((u, v))
  return n, edges


def fmt(arr):
  return "".join(f"{i} {d}\n" for d, i in arr)


def main():
  cases = []
  # 1 改写样例1
  cases.append(pack(6, [(1, 2), (1, 3), (2, 4), (3, 4), (4, 5), (3, 6)]))
  # 2 改写样例2：1 号孤立
  cases.append(pack(4, [(2, 3)]))
  # 3 改写样例3：同层须按编号，边序先 3 后 2
  cases.append(pack(3, [(1, 3), (1, 2)]))
  # 4 单点
  cases.append(pack(1, []))
  # 5 自环+重边，卡「当有向图」
  cases.append(pack(3, [(1, 1), (1, 2), (1, 2), (2, 3), (3, 2)]))
  # 6 链
  cases.append(pack(5, [(1, 2), (2, 3), (3, 4), (4, 5)]))
  # 7 星形：同层点多，卡 BFS 入队顺序
  cases.append(pack(6, [(1, 5), (1, 2), (1, 6), (1, 3)]))
  # 8 小随机 + 一个不连通块
  n = 12
  edges = []
  for i in range(1, 8):
    if i > 1:
      edges.append((RNG.randint(1, i - 1), i))
  edges.append((9, 10))
  edges.append((10, 11))
  edges.append((11, 12))
  cases.append(pack(n, edges))

  # 9 大数据：长链
  n = 100000
  edges = [(i, i + 1) for i in range(1, n)]
  cases.append(pack(n, edges))
  # 10 大数据：从 1 连出很多点，卡同层排序与输出规模
  edges = [(1, i) for i in range(2, n + 1)]
  cases.append(pack(n, edges))

  assert len(cases) == 10
  for i, tin in enumerate(cases, 1):
    n, edges = parse(tin)
    if not (1 <= n <= 100000 and len(edges) <= 100000):
      raise RuntimeError(f"bound {i}")
    for u, v in edges:
      if not (1 <= u <= n and 1 <= v <= n):
        raise RuntimeError(f"edge {i}")
    exp = solve(n, edges)
    exp_s = fmt(exp)
    tout = run_std(tin).replace("\r\n", "\n").replace("\r", "\n")
    if not tout.endswith("\n"):
      tout += "\n"
    if tout != exp_s:
      raise RuntimeError(f"mismatch {i}")
    write_pair(i, tin, tout)
    print(i, len(exp), "ok")


if __name__ == "__main__":
  main()
