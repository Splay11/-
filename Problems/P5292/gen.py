# -*- coding: utf-8 -*-
import random
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
from std import solve

DATA = ROOT / "data"
RNG = random.Random(529220260823)


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


def pack(n, m, k, a):
  return f"{n} {m} {k}\n" + " ".join(map(str, a))


def main():
  cases = []
  # 1 原题样例
  cases.append(pack(5, 4, 3, [1, 2, 1, 2, 1]))
  # 2 改写样例：窗口为 2
  cases.append(pack(4, 2, 2, [3, 1, 1, 3]))
  # 3 单点
  cases.append(pack(1, 10, 1, [5]))
  # 4 不能施工
  cases.append(pack(3, 0, 2, [4, 2, 8]))
  # 5 k=1，每次只能抬一段，卡「每次覆盖整段」
  cases.append(pack(4, 3, 1, [2, 0, 2, 0]))
  # 6 k>=n，一次就能盖完全程，答案是 min+m
  cases.append(pack(3, 5, 10, [1, 0, 1]))
  # 7 小随机
  n = 12
  a = [RNG.randint(0, 20) for _ in range(n)]
  cases.append(pack(n, RNG.randint(0, 30), RNG.randint(1, n), a))
  # 8 中间低谷，必须重叠覆盖
  cases.append(pack(7, 8, 3, [9, 8, 0, 0, 0, 7, 9]))
  # 9 大数据随机（n 取可读入上限 1e5，题面写 1e9 与第二行矛盾）
  n = 100000
  a = [RNG.randint(0, 10**9) for _ in range(n)]
  cases.append(pack(n, 10**9, RNG.randint(1, n), a))
  # 10 大数据：k=1 且高度接近上限，卡 int 溢出与错误覆盖
  a = [10**9] * n
  for i in range(0, n, 3):
    a[i] = 10**9 - 5
  cases.append(pack(n, 10**9, 1, a))

  assert len(cases) == 10
  for i, tin in enumerate(cases, 1):
    lines = tin.split("\n")
    n, m, k = map(int, lines[0].split())
    a = list(map(int, lines[1].split()))
    if len(a) != n:
      raise RuntimeError(f"len {i}")
    exp = solve(n, m, k, a)
    tout = run_std(tin)
    if not tout.endswith("\n"):
      tout += "\n"
    if int(tout.strip()) != exp:
      raise RuntimeError(f"stdio mismatch {i}")
    write_pair(i, tin, tout)
    print(f"{i} ok n={n} m={m} k={k} ans={exp}")


if __name__ == "__main__":
  main()
