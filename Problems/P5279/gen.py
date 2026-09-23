# -*- coding: utf-8 -*-
import random
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
from std import solve

DATA = ROOT / "data"
RNG = random.Random(527920260824)


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


def pack(m, a):
  n = len(a)
  return f"{n} {m}\n" + " ".join(map(str, a))


def parse(tin):
  lines = tin.split("\n")
  n, m = map(int, lines[0].split())
  a = list(map(int, lines[1].split()))
  if len(a) != n:
    raise RuntimeError("len")
  return n, m, a


def main():
  cases = []
  # 1 改写样例1：并列最长取左边
  cases.append(pack(10, [0, 2, 4, 7, 0]))
  # 2 改写样例2：单点
  cases.append(pack(5, [3]))
  # 3 改写样例3：交界处更长
  cases.append(pack(9, [2, 2, 2, 5, 8, 2]))
  # 4 全相等，变化量 0
  cases.append(pack(7, [4, 4, 4, 4]))
  # 5 负差取模
  cases.append(pack(5, [1, 0, 4, 3]))
  # 6 两段等长，卡「用 >= 会取右边」
  cases.append(pack(100, [0, 1, 2, 0, 2, 4]))
  # 7 原题形态但数字全换：绕模
  cases.append(pack(11, [2, 5, 8, 0, 3, 6, 10, 1]))
  # 8 小随机
  m = 13
  a = [RNG.randint(0, m - 1) for _ in range(20)]
  cases.append(pack(m, a))

  # 9 大数据：一整段匀差
  n = 200000
  m = 1000000000
  d = 123456789
  a = [0]
  for _ in range(n - 1):
    a.append((a[-1] + d) % m)
  cases.append(pack(m, a))
  # 10 大数据：很多短段，卡 O(n^2) 和并列取右
  a = []
  x = 0
  for i in range(n):
    a.append(x)
    x = (x + 1 + (i % 3)) % 10007
  cases.append(pack(10007, a))

  assert len(cases) == 10
  for i, tin in enumerate(cases, 1):
    n, m, a = parse(tin)
    if not (1 <= n <= 200000 and 2 <= m <= 10**9):
      raise RuntimeError(f"bound {i}")
    if min(a) < 0 or max(a) >= m:
      raise RuntimeError(f"val {i}")
    exp = solve(n, m, a)
    tout = run_std(tin).replace("\r\n", "\n").replace("\r", "\n")
    if not tout.endswith("\n"):
      tout += "\n"
    got = tuple(map(int, tout.split()))
    if got != exp:
      raise RuntimeError(f"mismatch {i}: {got} vs {exp}")
    write_pair(i, tin, tout)
    print(i, exp, "ok")


if __name__ == "__main__":
  main()
