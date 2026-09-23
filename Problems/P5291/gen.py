# -*- coding: utf-8 -*-
import random
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
from std import solve

DATA = ROOT / "data"
RNG = random.Random(529120260823)


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
  return f"{len(a)}\n" + " ".join(map(str, a))


def brute(a):
  n = len(a)
  best = n + 1
  for mask in range(1 << n):
    b = a[:]
    cnt = 0
    for i in range(n):
      if (mask >> i) & 1:
        cnt += 1
        for j in range(i, n):
          b[j] ^= 1
    if all(x == 1 for x in b):
      best = min(best, cnt)
  return best


def main():
  cases = []
  # 1 原题样例
  cases.append(pack([1, 0]))
  # 2 单点已亮
  cases.append(pack([1]))
  # 3 单点是灭
  cases.append(pack([0]))
  # 4 改写样例：必须按三次
  cases.append(pack([0, 1, 0]))
  # 5 全灭：按一次最左即可
  cases.append(pack([0, 0, 0, 0, 0]))
  # 6 全亮：零次
  cases.append(pack([1, 1, 1, 1]))
  # 7 交替，卡「只数 0 的个数」
  cases.append(pack([1, 0, 1, 0, 1, 0]))
  # 8 小随机，可暴力
  cases.append(pack([RNG.randint(0, 1) for _ in range(12)]))
  # 9 大数据随机
  cases.append(pack([RNG.randint(0, 1) for _ in range(100000)]))
  # 10 大数据：前半 0 后半交替，卡复杂度与错误贪心
  a10 = [0] * 50000 + [i % 2 for i in range(50000)]
  cases.append(pack(a10))

  assert len(cases) == 10
  for i, tin in enumerate(cases, 1):
    lines = tin.split("\n")
    n = int(lines[0])
    a = list(map(int, lines[1].split()))
    exp = solve(n, a)
    if n <= 12:
      b = brute(a)
      if b != exp:
        raise RuntimeError(f"brute mismatch {i}: {exp} vs {b}")
    tout = run_std(tin)
    if not tout.endswith("\n"):
      tout += "\n"
    if int(tout.strip()) != exp:
      raise RuntimeError(f"stdio mismatch {i}")
    write_pair(i, tin, tout)
    print(f"{i} ok n={n} ans={exp}")


if __name__ == "__main__":
  main()
