# -*- coding: utf-8 -*-
"""P5301 数据生成。
组别说明：
1 改写样例1；2 改写样例2；3 n=1 永远为 0；4 负数+最小 n=2；
5 全相等后改一个（卡「相等也当差」）；6 ±1e9 卡 int 溢出；
7 大量重复值；8 多段小数据（卡不重置树状数组）；
9 中等压力；10 接近 Σ(k+q) 上限。
"""
import random
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
RNG = random.Random(530120260825)


def brute_s(a):
  s = 0
  n = len(a)
  for i in range(n):
    for j in range(i + 1, n):
      s += abs(a[i] - a[j])
  return s


def brute_one(a, ops):
  arr = list(a)
  out = []
  for op in ops:
    if op[0] == 2:
      out.append(brute_s(arr))
    else:
      arr[op[1] - 1] = op[2]
  return out


def run_std(text):
  r = subprocess.run(
    ["python", str(ROOT / "std.py")],
    input=text.encode(),
    capture_output=True,
    check=True,
  )
  return r.stdout.decode().replace("\r\n", "\n")


def write_pair(idx, tin, tout):
  DATA.mkdir(parents=True, exist_ok=True)
  if tin.endswith("\n"):
    raise RuntimeError("in trailing nl")
  if not tout.endswith("\n") or tout.endswith("\n\n"):
    raise RuntimeError("out nl")
  (DATA / f"{idx}.in").write_bytes(tin.encode())
  (DATA / f"{idx}.out").write_bytes(tout.encode())


def emit_case(n, a, ops):
  lines = [f"{n} {len(ops)}", " ".join(map(str, a))]
  for op in ops:
    lines.append(" ".join(map(str, op)))
  return "\n".join(lines)


def pack_tests(tests):
  # tests: list of (n, a, ops)
  chunks = [str(len(tests))]
  for n, a, ops in tests:
    chunks.append(emit_case(n, a, ops))
  return "\n".join(chunks)


def rand_ops(n, q, lo, hi, query_ratio=0.4):
  ops = []
  for _ in range(q):
    if RNG.random() < query_ratio:
      ops.append((2,))
    else:
      ops.append((1, RNG.randint(1, n), RNG.randint(lo, hi)))
  if not any(op[0] == 2 for op in ops):
    ops[-1] = (2,)
  return ops


def main():
  cases = []

  # 1 改写样例1
  cases.append(pack_tests([
    (3, [0, 5, 2], [(2,), (1, 3, 9), (2,), (1, 1, 5), (2,)]),
  ]))

  # 2 改写样例2
  cases.append(pack_tests([
    (2, [7, 7], [(2,), (1, 2, 3), (2,)]),
  ]))

  # 3 基础：n=1，查询始终为 0
  cases.append(pack_tests([
    (1, [42], [(2,), (1, 1, -9), (2,), (1, 1, 0), (2,)]),
  ]))

  # 4 边界：负数、n=2
  cases.append(pack_tests([
    (2, [-8, 3], [(2,), (1, 1, -3), (2,), (1, 2, -3), (2,)]),
  ]))

  # 5 hack：全相等，再改一个；卡「漏掉相等对贡献为 0」或改错下标
  cases.append(pack_tests([
    (5, [4, 4, 4, 4, 4], [(2,), (1, 4, 10), (2,), (1, 4, 4), (2,)]),
  ]))

  # 6 hack：极值卡 32 位溢出。n=80 时 |S| 可达约 80^2/2 * 2e9
  a6 = [1000000000 if i % 2 == 0 else -1000000000 for i in range(80)]
  ops6 = [(2,)]
  ops6 += [(1, i + 1, -a6[i]) for i in range(0, 80, 7)]
  ops6 += [(2,), (1, 1, 0), (2,)]
  cases.append(pack_tests([(80, a6, ops6)]))

  # 7 构造：大量重复 + 簇状值
  a7 = [1] * 15 + [2] * 15 + [9] * 10
  ops7 = rand_ops(40, 60, 1, 9, 0.5)
  cases.append(pack_tests([(40, a7, ops7)]))

  # 8 多段小数据：卡每组不重建 BIT / 不清空答案
  tests8 = []
  for g in range(12):
    n = RNG.randint(1, 8)
    a = [RNG.randint(-20, 20) for _ in range(n)]
    ops = rand_ops(n, RNG.randint(2, 10), -20, 20, 0.5)
    tests8.append((n, a, ops))
  cases.append(pack_tests(tests8))

  # 9 中等压力
  n9, q9 = 8000, 8000
  a9 = [RNG.randint(-10**9, 10**9) for _ in range(n9)]
  ops9 = rand_ops(n9, q9, -10**9, 10**9, 0.35)
  cases.append(pack_tests([(n9, a9, ops9)]))

  # 10 大数据：控制行数，保证 PyPy/Java 在 2s 内；仍远大于暴力 O(kq)
  n10, q10 = 20000, 15000
  a10 = [RNG.randint(-10**9, 10**9) for _ in range(n10)]
  ops10 = rand_ops(n10, q10, -10**9, 10**9, 0.4)
  cases.append(pack_tests([(n10, a10, ops10)]))

  assert len(cases) == 10

  # 小数据与暴力对拍
  for idx in range(1, 9):
    tin = cases[idx - 1]
    lines = tin.split("\n")
    it = iter(lines)
    G = int(next(it))
    brute_out = []
    for _ in range(G):
      n, q = map(int, next(it).split())
      a = list(map(int, next(it).split()))
      ops = []
      for _ in range(q):
        ops.append(tuple(map(int, next(it).split())))
      brute_out.extend(brute_one(a, ops))
    std_out = [int(x) for x in run_std(tin).split()]
    if std_out != brute_out:
      raise RuntimeError(f"brute mismatch case {idx}: {std_out[:10]} vs {brute_out[:10]}")

  for i, tin in enumerate(cases, 1):
    print(f"generating {i} ...")
    tout = run_std(tin)
    if not tout.endswith("\n"):
      tout += "\n"
    # 去掉输出文件多余空行
    while tout.endswith("\n\n"):
      tout = tout[:-1]
    write_pair(i, tin, tout)
    print(f"{i} ok lines_in={tin.count(chr(10))+1} out_n={tout.count(chr(10))}")

  # 生成后自校验：再跑一遍 std
  for i in range(1, 11):
    tin = (DATA / f"{i}.in").read_text(encoding="utf-8")
    expected = (DATA / f"{i}.out").read_text(encoding="utf-8")
    got = run_std(tin)
    if not got.endswith("\n"):
      got += "\n"
    if got != expected:
      raise RuntimeError(f"recheck fail {i}")
  print("all recheck ok")


if __name__ == "__main__":
  main()
