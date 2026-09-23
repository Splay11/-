# -*- coding: utf-8 -*-
import random
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
from std import solve

DATA = ROOT / "data"
RNG = random.Random(527520260824)


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


def pack(a):
  r = len(a)
  c = len(a[0])
  lines = [f"{r} {c}"]
  for row in a:
    lines.append(" ".join(map(str, row)))
  return "\n".join(lines)


def parse(tin):
  lines = tin.split("\n")
  r, c = map(int, lines[0].split())
  a = []
  for i in range(r):
    row = list(map(int, lines[1 + i].split()))
    if len(row) != c:
      raise RuntimeError("row")
    a.append(row)
  return r, c, a


def fmt(b):
  return "".join(" ".join(map(str, row)) + "\n" for row in b)


def main():
  cases = []
  # 1 改写样例1
  cases.append(pack([[7, 8], [9, 0], [1, 4]]))
  # 2 改写样例2：单格
  cases.append(pack([[5]]))
  # 3 改写样例3：单列变单行
  cases.append(pack([[-3], [6]]))
  # 4 单行变单列
  cases.append(pack([[8, -1, 2]]))
  # 5 含负数与 1e9
  cases.append(pack([[-1000000000, 0], [1000000000, 3]]))
  # 6 方阵
  cases.append(pack([[1, 0, 0], [0, 1, 0], [0, 0, 1]]))
  # 7 小随机
  r, c = 4, 5
  a = [[RNG.randint(-20, 20) for _ in range(c)] for _ in range(r)]
  cases.append(pack(a))
  # 8 全相同
  cases.append(pack([[7] * 6 for _ in range(3)]))
  # 9 大数据：1000×1000
  n = 1000
  a = [[(i + j) % 10 for j in range(n)] for i in range(n)]
  cases.append(pack(a))
  # 10 大数据：1000×1，卡「行列搞反」
  a = [[RNG.randint(-10**9, 10**9)] for _ in range(n)]
  cases.append(pack(a))

  assert len(cases) == 10
  for i, tin in enumerate(cases, 1):
    r, c, a = parse(tin)
    if not (1 <= r <= 1000 and 1 <= c <= 1000):
      raise RuntimeError(f"bound {i}")
    exp = solve(r, c, a)
    exp_s = fmt(exp)
    tout = run_std(tin).replace("\r\n", "\n").replace("\r", "\n")
    if not tout.endswith("\n"):
      tout += "\n"
    if tout != exp_s:
      raise RuntimeError(f"mismatch {i}")
    write_pair(i, tin, tout)
    print(i, r, c, "ok")


if __name__ == "__main__":
  main()
