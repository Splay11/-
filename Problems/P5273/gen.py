# -*- coding: utf-8 -*-
import random
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
from std import solve

DATA = ROOT / "data"
RNG = random.Random(527320260824)


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


def parse(tin):
  lines = tin.split("\n")
  n, m, k = map(int, lines[0].split())
  a = list(map(int, lines[1].split()))
  return n, m, k, a


def main():
  cases = []
  # 1 改写样例1：交接后最忙日可到 40
  cases.append(pack(3, 2, 1, [40, 80, 90]))
  # 2 改写样例2：天数足够，全部交接，T=0
  cases.append(pack(2, 3, 1, [10, 20]))
  # 3 改写样例3：卡「支援只拿最大的 k 个」——应拿 250+200
  cases.append(pack(3, 1, 2, [300, 250, 200]))
  # 4 改写样例4：k=0 且总和超 480
  cases.append(pack(2, 1, 0, [300, 200]))
  # 5 单卷，不能交接，答案就是这一卷
  cases.append(pack(1, 1, 0, [7]))
  # 6 k=0 的分割，卡「忽略连续段约束」
  cases.append(pack(5, 3, 0, [100, 100, 100, 100, 100]))
  # 7 必须新开一天：中间有超过 T 且 k 不够
  cases.append(pack(4, 2, 0, [200, 200, 200, 200]))
  # 8 小随机
  n = 12
  a = [RNG.randint(1, 80) for _ in range(n)]
  cases.append(pack(n, RNG.randint(3, 8), RNG.randint(0, 3), a))

  # 9 大数据：k=0，全 1，天数拉满，答案为每段长度
  n = 20000
  cases.append(pack(n, 1000, 0, [1] * n))
  # 10 大数据：k=10，值偏小保证有解，压测位集与贪心延长
  a = [RNG.randint(1, 40) for _ in range(n)]
  cases.append(pack(n, 1000, 10, a))

  assert len(cases) == 10
  for i, tin in enumerate(cases, 1):
    n, m, k, a = parse(tin)
    if not (1 <= n <= 20000 and 1 <= m <= 1000 and 0 <= k <= 10):
      raise RuntimeError(f"bound {i}")
    if len(a) != n or min(a) < 1 or max(a) > 480:
      raise RuntimeError(f"arr {i}")
    exp = solve(n, m, k, a)
    tout = run_std(tin).replace("\r\n", "\n").replace("\r", "\n")
    if not tout.endswith("\n"):
      tout += "\n"
    if int(tout.strip()) != exp:
      raise RuntimeError(f"mismatch {i}: {tout!r} vs {exp}")
    write_pair(i, tin, tout)
    print(i, exp, "ok")


if __name__ == "__main__":
  main()
