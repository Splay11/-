# -*- coding: utf-8 -*-
import random
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
from std import solve

DATA = ROOT / "data"
RNG = random.Random(528620260823)


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


def pack(n, k, a):
  return f"{n} {k}\n" + " ".join(map(str, a))


def brute(n, k, a):
  best = n
  for mask in range(1 << n):
    on = [a[i] for i in range(n) if (mask >> i) & 1]
    ok = True
    for i in range(len(on)):
      for j in range(i + 1, len(on)):
        if on[i] + on[j] == k:
          ok = False
          break
      if not ok:
        break
    if ok:
      best = min(best, n - len(on))
  return best


def rand_vals(n, lo, hi):
  return [RNG.randint(lo, hi) for _ in range(n)]


def make_pairs(n, k, n_pairs, self_pair=False, uneven=False):
  a = []
  used = set()
  pairs = []
  tries = 0
  while len(pairs) < n_pairs and tries < 20000:
    tries += 1
    x = RNG.randint(1, k - 1)
    y = k - x
    if y < 1 or y > 10**9:
      continue
    if x == y:
      continue
    key = (min(x, y), max(x, y))
    if key in used:
      continue
    used.add(key)
    pairs.append((x, y))
  remain = n
  for x, y in pairs:
    if remain <= 0:
      break
    if uneven:
      cx = 1
      cy = max(1, remain // max(1, len(pairs) - len(a) // 2 + 1))
      cy = min(cy, remain - 1) if remain > 1 else 1
    else:
      cx = RNG.randint(1, 3)
      cy = RNG.randint(1, 3)
    take = min(remain, cx + cy)
    if take <= 1:
      a.append(x)
      remain -= 1
      continue
    left = min(cx, take - 1)
    right = take - left
    a.extend([x] * left)
    a.extend([y] * right)
    remain -= take
  if self_pair and k % 2 == 0 and remain > 0:
    half = k // 2
    if 1 <= half <= 10**9:
      c = remain if remain <= 4 else RNG.randint(2, min(remain, remain // 2 + 2))
      c = min(c, remain)
      a.extend([half] * c)
      remain -= c
  while remain > 0:
    v = RNG.randint(1, 10**9)
    if k - v != v and (k - v < 1 or k - v not in used and RNG.random() < 0.7):
      a.append(v)
      remain -= 1
    else:
      a.append(RNG.randint(1, max(1, min(10**9, k))))
      remain -= 1
  RNG.shuffle(a)
  return a[:n]


def main():
  cases = []

  # 1 原题样例1：单按钮，答案 0
  cases.append(pack(1, 1, [2021]))
  # 2 原题样例2：两组交叉冲突
  cases.append(pack(7, 10, [2, 8, 7, 3, 2, 7, 1]))
  # 3 自身配对 2x=k，卡「漏掉同类相加」或「删光 / 只删一半」
  cases.append(pack(6, 10, [5, 5, 5, 5, 1, 9]))
  # 4 无冲突：全部大于 k 或无法配对
  cases.append(pack(5, 3, [4, 5, 6, 7, 8]))
  # 5 频次极不均匀：一侧 1 个、一侧很多
  cases.append(pack(8, 20, [3, 17, 3, 3, 3, 3, 3, 1]))
  # 6 小随机，可与暴力对拍
  cases.append(pack(12, 30, rand_vals(12, 1, 25)))
  # 7 多组独立冲突对 + 自身对
  a7 = make_pairs(40, 100, n_pairs=8, self_pair=True, uneven=True)
  cases.append(pack(len(a7), 100, a7))
  # 8 重复值 + 多个互补对，卡双边重复计数
  cases.append(pack(16, 50, [10, 40, 10, 40, 20, 30, 25, 25, 25, 1, 49, 15, 35, 8, 8, 42]))
  # 9 大数据随机
  n9, k9 = 100000, 10**9
  a9 = make_pairs(n9, k9, n_pairs=80, self_pair=False, uneven=False)
  cases.append(pack(n9, k9, a9))
  # 10 大数据构造：大量互补对 + 2x=k 海量重复
  n10, k10 = 100000, 10**9
  a10 = []
  # 自身对：50000 个 5e8
  half = k10 // 2
  a10.extend([half] * 50000)
  # 若干不均匀互补对
  left = 50000
  pair_id = 1
  while left > 0 and pair_id < 200:
    x = pair_id
    y = k10 - x
    if x == y:
      pair_id += 1
      continue
    cx = 1
    cy = min(left - 1, 200 + pair_id)
    if left <= 1:
      a10.append(x)
      left -= 1
      break
    a10.extend([x] * cx)
    a10.extend([y] * cy)
    left -= cx + cy
    pair_id += 1
  while len(a10) < n10:
    a10.append(RNG.randint(1, 10**9))
  a10 = a10[:n10]
  RNG.shuffle(a10)
  cases.append(pack(n10, k10, a10))

  assert len(cases) == 10
  for i, tin in enumerate(cases, 1):
    lines = tin.split("\n")
    n, k = map(int, lines[0].split())
    a = list(map(int, lines[1].split()))
    if len(a) != n:
      raise RuntimeError(f"len mismatch {i}")
    exp = solve(n, k, a)
    if n <= 16:
      b = brute(n, k, a)
      if b != exp:
        raise RuntimeError(f"brute mismatch {i}: std={exp} brute={b}")
    tout = run_std(tin)
    if not tout.endswith("\n"):
      tout += "\n"
    if int(tout.strip()) != exp:
      raise RuntimeError(f"stdio mismatch {i}")
    write_pair(i, tin, tout)
    print(f"{i} ok n={n} ans={exp}")


if __name__ == "__main__":
  main()
