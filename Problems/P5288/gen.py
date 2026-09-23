# -*- coding: utf-8 -*-
import heapq
import random
import subprocess
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
from std import solve

DATA = ROOT / "data"
RNG = random.Random(528820260823)


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


def pack(s, m):
  return f"{len(s)}\n{s}\n{m}"


def simulate(s, m):
  """堆模拟：每轮取最多 m+1 个不同剩余任务，用于核对公式。"""
  freq = [-c for c in Counter(s).values()]
  heapq.heapify(freq)
  time = 0
  while freq:
    used = []
    slots = m + 1
    for _ in range(slots):
      if freq:
        c = heapq.heappop(freq)
        time += 1
        if c + 1 < 0:
          used.append(c + 1)
      else:
        if used:
          time += 1
        else:
          break
    for c in used:
      heapq.heappush(freq, c)
  return time


def rand_s(n, alphabet="ABCDEFGHIJKLMNOPQRSTUVWXYZ"):
  return "".join(RNG.choice(alphabet) for _ in range(n))


def main():
  cases = []
  # 1 原题样例
  cases.append(pack("AB", 2))
  # 2 改写样例1：单张
  cases.append(pack("Z", 5))
  # 3 改写样例2：两类并列最高频，必须空转
  cases.append(pack("CCCDDD", 3))
  # 4 冷却为 0，答案等于长度
  cases.append(pack("EEEEE", 0))
  # 5 单一类型拉满冷却，卡「直接输出 n」
  cases.append(pack("AAAA", 2))
  # 6 种类足够填满空档，答案仍是 n
  cases.append(pack("WWWXYZUVW", 1))
  # 7 小随机
  cases.append(pack(rand_s(20, "ABCDEFGH"), 4))
  # 8 hack：并列最高频种类数 > 1，卡「框架末尾只加 1」
  cases.append(pack("AAAABBBB", 3))
  # 9 大数据随机
  cases.append(pack(rand_s(10000), 37))
  # 10 大数据：一种占优 + 冷却上限
  cases.append(pack("A" * 8000 + rand_s(2000, "BCDEFGHIJKLMNOPQRSTUVWXYZ"), 100))

  assert len(cases) == 10
  for i, tin in enumerate(cases, 1):
    lines = tin.split("\n")
    n = int(lines[0])
    s = lines[1]
    m = int(lines[2])
    if len(s) != n:
      raise RuntimeError(f"len mismatch {i}")
    exp = solve(n, s, m)
    sim = simulate(s, m)
    if sim != exp:
      raise RuntimeError(f"sim mismatch {i}: std={exp} sim={sim}")
    tout = run_std(tin)
    if not tout.endswith("\n"):
      tout += "\n"
    if int(tout.strip()) != exp:
      raise RuntimeError(f"stdio mismatch {i}")
    write_pair(i, tin, tout)
    print(f"{i} ok n={n} m={m} ans={exp}")


if __name__ == "__main__":
  main()
