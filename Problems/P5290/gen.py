# -*- coding: utf-8 -*-
import random
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
from std import solve

DATA = ROOT / "data"
RNG = random.Random(529020260823)


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


def pack(n, fa, w, W):
  lines = [str(n)]
  if n == 1:
    lines.append("")
  else:
    lines.append(" ".join(map(str, fa)))
  lines.append(" ".join(map(str, w)))
  lines.append(str(W))
  return "\n".join(lines)


def rand_bin(n, wlo=1, whi=1000):
  fa = []
  deg = [0] * n
  avail = [0]
  pos = {0: 0}
  for i in range(1, n):
    p = avail[RNG.randrange(len(avail))]
    fa.append(p)
    deg[p] += 1
    if deg[p] == 2:
      j = pos[p]
      last = avail[-1]
      avail[j] = last
      pos[last] = j
      avail.pop()
      del pos[p]
    pos[i] = len(avail)
    avail.append(i)
  w = [RNG.randint(wlo, whi) for _ in range(n)]
  W = RNG.randint(wlo, whi)
  return fa, w, W


def chain(n, wlo=1, whi=1000):
  fa = list(range(n - 1))
  w = [RNG.randint(wlo, whi) for _ in range(n)]
  W = RNG.randint(wlo, whi)
  return fa, w, W


def brute(n, fa, w, W):
  ch = [[] for _ in range(n)]
  for i in range(1, n):
    ch[fa[i - 1]].append(i)

  def sz_of(x):
    s = 1
    for y in ch[x]:
      s += sz_of(y)
    return s

  def rec(u, start, ww):
    if not ch[u]:
      return [(1.0, {u: start})]
    if len(ch[u]) == 1:
      out = []
      for p, d in rec(ch[u][0], start + 1, ww):
        d = dict(d)
        d[u] = start
        out.append((p, d))
      return out
    a, b = ch[u]
    sza, szb = sz_of(a), sz_of(b)
    pa = ww[a] / (ww[a] + ww[b])
    pb = 1.0 - pa
    out = []
    for p, d in rec(a, start + 1, ww):
      for q, e in rec(b, start + 1 + sza, ww):
        m = dict(d)
        m.update(e)
        m[u] = start
        out.append((p * q * pa, m))
    for p, d in rec(b, start + 1, ww):
      for q, e in rec(a, start + 1 + szb, ww):
        m = dict(d)
        m.update(e)
        m[u] = start
        out.append((p * q * pb, m))
    return out

  def expect(ww):
    es = 0.0
    for p, d in rec(0, 1, ww):
      S = sum(ww[i] * (n + 1 - d[i]) for i in range(n))
      es += p * S
    return es

  best = expect(list(w))
  for x in range(n):
    ww = list(w)
    ww[x] = W
    best = max(best, expect(ww))
  return best


def main():
  cases = []
  # 1 原题样例
  cases.append(pack(5, [0, 0, 1, 1], [5, 1, 1, 1, 1], 4))
  # 2 单点：只能改自己或不改
  cases.append(pack(1, [], [5], 3))
  # 3 改写样例1：根双孩子，改根最优
  cases.append(pack(3, [0, 0], [2, 3, 4], 10))
  # 4 链，无概率，卡「只改权值」
  cases.append(pack(4, [0, 1, 2], [1, 2, 3, 4], 5))
  # 5 目标权更小，最优可能是不改
  cases.append(pack(3, [0, 0], [9, 9, 9], 1))
  # 6 小随机二叉树，可暴力对拍
  fa, w, W = rand_bin(7, 1, 20)
  cases.append(pack(7, fa, w, W))
  # 7 中等随机
  fa, w, W = rand_bin(80, 1, 1000)
  cases.append(pack(80, fa, w, W))
  # 8 hack：一侧很重，改兄弟权值会显著改概率
  cases.append(pack(6, [0, 0, 1, 1, 2], [1, 1, 100, 2, 2, 2], 1000))
  # 9 大数据链
  fa, w, W = chain(100000, 1, 1000)
  cases.append(pack(100000, fa, w, W))
  # 10 大数据：根下两棵链，权值全相同，期望为整或半整，避免多语言四舍五入对不齐
  n10 = 100000
  fa10 = [0]
  for i in range(2, n10):
    fa10.append(i - 1 if i != 50000 else 0)
  w10 = [7] * n10
  cases.append(pack(n10, fa10, w10, 7))

  assert len(cases) == 10
  for i, tin in enumerate(cases, 1):
    lines = tin.split("\n")
    n = int(lines[0])
    fa = list(map(int, lines[1].split())) if lines[1].strip() else []
    w = list(map(int, lines[2].split()))
    W = int(lines[3])
    exp = solve(n, fa, w, W)
    if n <= 7:
      b = brute(n, fa, w, W)
      if abs(b - exp) > 1e-6:
        raise RuntimeError(f"brute mismatch {i}: {exp} vs {b}")
    tout = run_std(tin)
    if not tout.endswith("\n"):
      tout += "\n"
    if abs(float(tout.strip()) - float("%.4f" % exp)) > 1.5e-4:
      raise RuntimeError(f"stdio mismatch {i}: {tout.strip()} vs {exp}")
    write_pair(i, tin, tout)
    print(f"{i} ok n={n} ans={tout.strip()}")


if __name__ == "__main__":
  main()
